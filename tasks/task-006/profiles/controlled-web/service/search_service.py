#!/usr/bin/env python3
"""Controlled-Web Search Service for Task 006.

Provides two tools:
  search_corpus <query>   — search the corpus by keyword; returns JSON array
  fetch_document <doc_id> — fetch full document content by ID; returns JSON object

Loads search-index.json into memory at startup. Tokenizes queries by lowercase
splitting. Returns top 20 results by term frequency score.

Stdlib only — Python 3.10+.
"""

import json
import sys
from pathlib import Path

SERVICE_DIR = Path(__file__).resolve().parent
PRIVATE_DIR = SERVICE_DIR / "private"
INDEX_PATH = PRIVATE_DIR / "search-index.json"
CORPUS_DIR = PRIVATE_DIR / "corpus"
MANIFEST_PATH = PRIVATE_DIR / "corpus-manifest.json"


class SearchService:
    def __init__(self):
        self.index: dict[str, list[dict]] = {}
        self.manifest: list[dict] = []
        self._load()

    def _load(self) -> None:
        if not INDEX_PATH.is_file():
            die(f"search-index.json not found at {INDEX_PATH}")
        if not MANIFEST_PATH.is_file():
            die(f"corpus-manifest.json not found at {MANIFEST_PATH}")

        with open(INDEX_PATH, encoding="utf-8") as f:
            self.index = json.load(f)
        with open(MANIFEST_PATH, encoding="utf-8") as f:
            manifest_data = json.load(f)
            self.manifest = manifest_data.get("documents", [])

    def _manifest_lookup(self, doc_id: str) -> dict | None:
        for doc in self.manifest:
            if doc["doc_id"] == doc_id:
                return doc
        return None

    def search(self, query: str) -> list[dict]:
        """Return top 20 matching documents with snippets and scores."""
        if not query or not query.strip():
            return []

        tokens = query.lower().split()
        scores: dict[str, float] = {}

        for token in tokens:
            token_clean = "".join(c for c in token if c.isalnum())
            if not token_clean or len(token_clean) < 2:
                continue
            entries = self.index.get(token_clean, [])
            for entry in entries:
                doc_id = entry["doc_id"]
                scores[doc_id] = scores.get(doc_id, 0.0) + entry["score"]

        # Sort by score descending, top 20
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:20]

        results = []
        for doc_id, score in ranked:
            meta = self._manifest_lookup(doc_id)
            if meta is None:
                continue
            # Read snippet from corpus file (first 300 chars of body)
            corpus_file = CORPUS_DIR / f"{doc_id}.md"
            snippet = ""
            if corpus_file.is_file():
                content = corpus_file.read_text(encoding="utf-8")
                # Skip frontmatter (between --- markers)
                parts = content.split("---", 2)
                body = parts[2].strip() if len(parts) >= 3 else content
                snippet = body[:300]

            results.append({
                "doc_id": doc_id,
                "title": meta["title"],
                "snippet": snippet,
                "score": round(score, 2),
            })

        return results

    def fetch(self, doc_id: str) -> dict | None:
        """Return full document content and metadata, or None if not found."""
        meta = self._manifest_lookup(doc_id)
        if meta is None:
            return None

        corpus_file = CORPUS_DIR / f"{doc_id}.md"
        if not corpus_file.is_file():
            return None

        content = corpus_file.read_text(encoding="utf-8")
        # Extract body (skip frontmatter)
        parts = content.split("---", 2)
        body = parts[2].strip() if len(parts) >= 3 else content

        return {
            "doc_id": doc_id,
            "title": meta["title"],
            "source": meta["source"],
            "dimension": meta["dimension"],
            "canonical_url": meta["canonical_url"],
            "snapshot_date": meta["snapshot_date"],
            "content_hash": meta["content_hash"],
            "publisher": meta["publisher"],
            "authority_tier": meta["authority_tier"],
            "tags": meta.get("tags", []),
            "content": body,
        }


def die(msg: str) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: search_service.py <command> [args...]", file=sys.stderr)
        print("Commands: search_corpus <query>, fetch_document <doc_id>", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    svc = SearchService()

    if command == "search_corpus":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        results = svc.search(query)
        print(json.dumps(results, indent=2, ensure_ascii=False))

    elif command == "fetch_document":
        if len(sys.argv) < 3:
            die("fetch_document requires a doc_id argument")
        doc_id = sys.argv[2]
        doc = svc.fetch(doc_id)
        if doc is None:
            print(json.dumps({"error": "NOT_FOUND", "doc_id": doc_id}))
            sys.exit(1)
        print(json.dumps(doc, indent=2, ensure_ascii=False))

    else:
        die(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
