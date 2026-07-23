#!/usr/bin/env python3
import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

def _parse_contract(path):
    contract = {}
    section = None       # current top-level key whose value is a dict
    subsection = None    # current sub-key inside a section dict

    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            line = raw.rstrip("\n")
            stripped = line.strip()

            # skip blanks and comments
            if not stripped or stripped.startswith("#"):
                continue

            # ---- top-level key ----
            if not line.startswith(" "):
                if ":" in stripped:
                    key, _, val = stripped.partition(":")
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if val:
                        contract[key] = val       # scalar  (e.g. version)
                        section = None
                        subsection = None
                    else:
                        section = key
                        contract[section] = {}    # will become dict or list
                        subsection = None
                continue

            # ---- indented 2 spaces ----
            if line.startswith("  ") and not line.startswith("    "):
                if stripped.startswith("- "):
                    # list item inside a simple top-level list  (default_excludes)
                    val = stripped[2:].strip().strip("\"'")
                    if isinstance(contract.get(section), list):
                        contract[section].append(val)
                    else:
                        contract[section] = [val]
                    continue

                if ":" in stripped:
                    subkey = stripped.rstrip(":")
                    after = stripped.split(":", 1)[1].strip()
                    if after == "[]":
                        contract[section][subkey] = []
                    else:
                        contract[section][subkey] = []
                    subsection = subkey
                    continue

            # ---- indented 4 spaces ----
            if line.startswith("    ") and stripped.startswith("- "):
                val = stripped[2:].strip().strip("\"'")
                if section and subsection:
                    target = contract[section].get(subsection)
                    if isinstance(target, list):
                        target.append(val)
                continue

    return contract

def _glob_match(path, pattern):
    if "/" not in pattern and "**" not in pattern:
        return fnmatch.fnmatch(os.path.basename(path), pattern)

    if "**" in pattern:
        # Convert glob with ** to regex: ** matches zero or more path components
        import re
        escaped = re.escape(pattern)
        # Un-escape ** and * (re.escape escapes *, but we want glob semantics)
        escaped = escaped.replace(r"\*\*", ".*")   # ** → any characters (including /)
        escaped = escaped.replace(r"\*", "[^/]*")   # *  → any non-/ characters
        return bool(re.match("^" + escaped + "$", path))

    return fnmatch.fnmatch(path, pattern)


def _matches_any(path, patterns):
    return any(_glob_match(path, p) for p in patterns)


def _tracked_files(repo_root):
    files = set()
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        result = None

    if result is not None:
        files.update(line.strip() for line in result.stdout.strip().split("\n") if line.strip())

    for dirpath, dirnames, filenames in os.walk(repo_root):
        if ".git" in dirnames:
            dirnames.remove(".git")
        for fn in filenames:
            abs_p = os.path.join(dirpath, fn)
            rel_p = os.path.relpath(abs_p, repo_root)
            if rel_p == ".git":
                continue
            files.add(rel_p)

    return sorted(files)


def _source_commit(repo_root):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            cwd=repo_root,
            check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNAVAILABLE"
    return result.stdout.strip() or "UNAVAILABLE"


def _declared_task_ids(repo_root):
    manifest_path = os.path.join(repo_root, "skill.json")
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)

    declared = []
    seen = set()
    for task in manifest.get("tasks", []):
        task_id = task.get("id") if isinstance(task, dict) else task
        if not task_id or task_id in seen:
            print(f"Error: duplicate or missing task id in skill.json: {task_id}", file=sys.stderr)
            sys.exit(1)
        task_dir = os.path.join(repo_root, "tasks", task_id)
        if not os.path.isdir(task_dir):
            print(f"Error: declared task missing on disk: {task_id}", file=sys.stderr)
            sys.exit(1)
        declared.append(task_id)
        seen.add(task_id)
    return set(declared)


def _task_id_for_path(fpath):
    parts = fpath.split("/", 2)
    if len(parts) >= 2 and parts[0] == "tasks":
        return parts[1]
    return None

def _classify(tracked, contract, declared_task_ids):
    excludes = contract.get("default_excludes", [])

    agent_inc  = contract.get("agent_package",   {}).get("include", [])
    agent_exc  = contract.get("agent_package",   {}).get("exclude", [])
    rexp_inc   = contract.get("runtime_exposed", {}).get("include", [])
    rexp_exc   = contract.get("runtime_exposed", {}).get("exclude", [])
    rpriv_inc  = contract.get("runtime_private", {}).get("include", [])
    rpriv_exc  = contract.get("runtime_private", {}).get("exclude", [])
    eval_inc   = contract.get("evaluator_only",  {}).get("include", [])
    eval_exc   = contract.get("evaluator_only",  {}).get("exclude", [])

    # union of every include pattern — used to detect truly unclassified files
    all_include = agent_inc + rexp_inc + rpriv_inc + eval_inc

    classified = {"agent": [], "runtime_exposed": [], "runtime_private": [],
                  "evaluator": []}
    unclassified = []

    for fpath in tracked:
        task_id = _task_id_for_path(fpath)
        if task_id is not None and task_id not in declared_task_ids:
            continue

        # 1. default excludes
        if _matches_any(fpath, excludes):
            continue

        # 2. must be classified by at least one view
        if not _matches_any(fpath, all_include):
            unclassified.append(fpath)
            continue

        # 3. assign to specific views (a file may belong to several)
        if _matches_any(fpath, agent_inc) and not _matches_any(fpath, agent_exc):
            classified["agent"].append(fpath)
        if _matches_any(fpath, rexp_inc) and not _matches_any(fpath, rexp_exc):
            classified["runtime_exposed"].append(fpath)
        if _matches_any(fpath, rpriv_inc) and not _matches_any(fpath, rpriv_exc):
            classified["runtime_private"].append(fpath)
        if _matches_any(fpath, eval_inc) and not _matches_any(fpath, eval_exc):
            classified["evaluator"].append(fpath)

    return classified, unclassified


def _runtime_for_task(classified, task_id):
    """Return runtime-exposed + runtime-private files scoped to *task_id*."""
    prefix = f"tasks/{task_id}/"

    def _in_task(fpath):
        return fpath.startswith(prefix)

    exposed = [f for f in classified["runtime_exposed"] if _in_task(f)]
    private = [f for f in classified["runtime_private"] if _in_task(f)]
    return sorted(set(exposed + private))

def _sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as fh:
        while chunk := fh.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _package_digest(manifest_entries):
    payload = "".join(
        sorted(f"{entry['path']}:{entry['sha256']}" for entry in manifest_entries),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _build(files, repo_root, output_dir, build_target):
    os.makedirs(output_dir, exist_ok=True)
    manifest_entries = []

    for rel in sorted(files):
        src = os.path.join(repo_root, rel)
        dst = os.path.join(output_dir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        manifest_entries.append({"path": rel, "sha256": _sha256(src)})

    manifest = {
        "build_target": build_target,
        "source_commit": _source_commit(repo_root),
        "package_digest": _package_digest(manifest_entries),
        "files": manifest_entries,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    mpath = os.path.join(output_dir, "package-manifest.json")
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")

    return len(files)

def main():
    ap = argparse.ArgumentParser(
        prog="build-distribution.py",
        description="Build distribution packages from classification contract",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""examples:
  python3 scripts/build-distribution.py --target agent --output /tmp/pkg
  python3 scripts/build-distribution.py --target runtime --task task-004 --output /tmp/rt
  python3 scripts/build-distribution.py --target evaluator --output /tmp/ev""",
    )
    ap.add_argument("--target", required=True,
                    choices=["agent", "runtime", "evaluator"],
                    help="build target")
    ap.add_argument("--task", default=None,
                    help="task id, required when --target=runtime  (e.g. task-004)")
    ap.add_argument("--output", required=True,
                    help="output directory")
    args = ap.parse_args()

    if args.target == "runtime" and not args.task:
        ap.error("--task is required when --target is runtime")

    # repo root = project root (parent of scripts/)
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    contract_path = os.path.join(repo_root, "contracts", "distribution-contract.yaml")
    if not os.path.isfile(contract_path):
        print(f"Error: contract not found — {contract_path}", file=sys.stderr)
        sys.exit(1)

    contract = _parse_contract(contract_path)
    tracked = _tracked_files(repo_root)
    declared_task_ids = _declared_task_ids(repo_root)
    classified, unclassified = _classify(tracked, contract, declared_task_ids)

    if unclassified:
        for fp in sorted(unclassified):
            print(f"Unclassified file: {fp}", file=sys.stderr)
        print(f"Error: {len(unclassified)} file(s) not classified in any view. "
              "Update contracts/distribution-contract.yaml.", file=sys.stderr)
        sys.exit(1)

    # select files for the requested target
    if args.target == "agent":
        files = sorted(classified["agent"])
        build_target = "agent"
    elif args.target == "evaluator":
        files = sorted(classified["evaluator"])
        build_target = "evaluator"
    else:  # runtime
        files = _runtime_for_task(classified, args.task)
        build_target = f"runtime-{args.task}"

    n = _build(files, repo_root, args.output, build_target)
    print(f"Built {build_target} package: {n} files → {args.output}")


if __name__ == "__main__":
    main()
