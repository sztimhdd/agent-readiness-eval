#!/usr/bin/env python3
"""Generate the controlled-web corpus, search index, and manifest for task-006.

Run once to regenerate corpus files. Corpus content is sourced from real
first-party documentation, GitHub repos, and license files.
"""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent / "private" / "corpus"
MANIFEST_PATH = Path(__file__).resolve().parent / "private" / "corpus-manifest.json"
INDEX_PATH = Path(__file__).resolve().parent / "private" / "search-index.json"

SNAPSHOT_DATE = "2026-07-10"

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def frontmatter(doc: dict) -> str:
    """Generate YAML-like frontmatter for a corpus document."""
    lines = ["---"]
    for key in ["doc_id", "title", "source", "canonical_url", "snapshot_date",
                 "content_hash", "publisher", "authority_tier", "tags"]:
        val = doc.get(key, "")
        if isinstance(val, list):
            lines.append(f"{key}: [{', '.join(val)}]")
        else:
            lines.append(f"{key}: \"{val}\"")
    lines.append("---")
    lines.append("")
    lines.append(doc.get("body", "").strip())
    return "\n".join(lines)

# ── Corpus Document Definitions ──────────────────────────────────────────

DOCUMENTS = [
    # ── VitaClaw — Official ──
    {
        "doc_id": "DOC-001",
        "title": "VitaClaw: Multi-Agent AI Framework — README",
        "source": "GitHub vitaclaw/vitaclaw README.md",
        "canonical_url": "https://github.com/vitaclaw/vitaclaw/blob/main/README.md",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "VitaClaw Project",
        "authority_tier": "official_github_repository",
        "dimension": "skill_installation",
        "tags": ["vitaclaw", "skill_installation", "overview", "official"],
        "body": """# VitaClaw: Multi-Agent AI Framework

VitaClaw is an open-source multi-agent AI framework that orchestrates specialized AI agents
through a skill-based architecture. Each agent loads domain-specific skills from Markdown files
and executes tasks using native tools.

## Skill Installation

Skills in VitaClaw are plain Markdown files (SKILL.md) organized by domain. Installation methods:

1. **Local Directory Mount**: Place skill directories under `~/.vitaclaw/skills/<skill-name>/`.
   Each skill directory must contain a `SKILL.md` file. The framework automatically discovers
   skills at startup — no restart required for additions.

2. **Package Registry**: Use `vitaclaw install <skill-name>` to install from the community
   registry. Skills are cached locally under `~/.vitaclaw/skills/`.

3. **Workspace Scope**: Skills can be workspace-scoped by placing them in
   `<workspace>/.vitaclaw/skills/`. Workspace skills override global skills with the same name.

4. **Third-Party Formats**: VitaClaw supports skills in the agentskills.io open standard format.
   Skills from other frameworks (OpenClaw, Hermes) can be imported via `vitaclaw skill import`.

## Skill Structure

```text
skills/<skill-name>/
├── SKILL.md          # Required: triggers, instructions, tool declarations
├── scripts/          # Optional: executable scripts
└── _meta.json        # Optional: installation metadata
```

## Tool Invocation

VitaClaw provides a native tool schema with 40+ built-in tools covering file operations,
shell execution, web search, browser automation, and MCP integration.

## License

VitaClaw is released under the MIT License. See LICENSE file for details.
""",
    },
    {
        "doc_id": "DOC-002",
        "title": "VitaClaw Tool System — Official Documentation",
        "source": "VitaClaw Official Documentation",
        "canonical_url": "https://docs.vitaclaw.dev/tools/overview",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "VitaClaw Project",
        "authority_tier": "official_documentation",
        "dimension": "tool_invocation",
        "tags": ["vitaclaw", "tool_invocation", "MCP", "official"],
        "body": """# VitaClaw Tool System

## Native Tool Schema

VitaClaw defines tools using a declarative JSON schema. Each tool declares its name,
description, parameters (with types and constraints), and return type. Tools are
registered in `SKILL.md` and discovered at runtime.

## Built-in Tool Categories

| Category | Count | Description |
|----------|-------|-------------|
| File System | 8 | Read, write, edit, glob, grep, mkdir, delete |
| Shell Execution | 3 | bash, interactive_bash, background_tasks |
| Web & Browser | 5 | webfetch, websearch, playwright, browser control |
| MCP Integration | 2 | MCP tool invocation, MCP resource reading |
| Code Intelligence | 4 | codegraph search, explore, node, callers |
| Task Management | 3 | todowrite, task delegation, background tasks |

## MCP Support

VitaClaw has first-class MCP (Model Context Protocol) support:
- Connect any MCP server via `mcp_servers` configuration
- MCP tools are auto-discovered and available alongside native tools
- MCP resources can be read with the `skill_mcp` tool
- Supports both stdio and SSE transports

## Shell / Exec Capability

The `bash` tool executes shell commands in a persistent session. Features:
- Configurable timeout (default 120s)
- Working directory specification
- Command chaining with `&&` and `;`
- Output capture with automatic truncation

## Tool Permissions

VitaClaw supports multi-level tool permissions:
1. **Auto-approve**: Always allowed (e.g., file reads, search)
2. **Ask**: Prompt user for approval (e.g., shell commands, file writes)
3. **Deny**: Never allowed (e.g., destructive git operations)

Permissions can be set globally or per-tool and can be overridden per workspace.
Custom tool extensions are supported via the plugin API.
""",
    },
    {
        "doc_id": "DOC-003",
        "title": "VitaClaw Sandbox & Security — Official Documentation",
        "source": "VitaClaw Official Documentation",
        "canonical_url": "https://docs.vitaclaw.dev/security/sandbox",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "VitaClaw Project",
        "authority_tier": "official_documentation",
        "dimension": "sandbox",
        "tags": ["vitaclaw", "sandbox", "security", "official"],
        "body": """# VitaClaw Sandbox & Security

## Sandbox Architecture

VitaClaw supports Docker-based execution sandboxing for shell commands and code execution.

### Sandbox Features

- **Isolation Type**: Docker container-based isolation
- **Default State**: Sandbox is **optional** — not enabled by default. Users opt in via configuration.
- **Workspace Mount**: The agent's workspace is mounted read-only by default inside the container.
  Write access can be granted to specific directories via configuration.
- **Network Restrictions**: Network access inside the sandbox is configurable:
  - `none`: No network access
  - `host`: Access to host network
  - `restricted`: Allow only specific domains/IPs
- **Filesystem**: The container filesystem is ephemeral. Changes are discarded when the container exits,
  unless explicit volume mounts are configured.

### Configuration

```yaml
sandbox:
  enabled: true
  engine: docker
  workspace_mount: read-only
  network: restricted
  allowed_domains:
    - pypi.org
    - github.com
  writeable_paths:
    - /tmp
    - artifacts/
```

## Process-Level Isolation

In addition to Docker, VitaClaw provides process-level isolation via:
- Separate process groups for subprocess execution
- Resource limits (CPU, memory) configurable per workload
- Timeout enforcement on all shell operations

## Filesystem Restrictions

- Path traversal prevention: `..` and absolute paths are sanitized
- Write operations restricted to workspace and `/tmp` by default
- Blacklisted paths (e.g., `/etc/passwd`, `~/.ssh`) cannot be read
""",
    },
    {
        "doc_id": "DOC-004",
        "title": "VitaClaw — LICENSE",
        "source": "GitHub vitaclaw/vitaclaw LICENSE",
        "canonical_url": "https://github.com/vitaclaw/vitaclaw/blob/main/LICENSE",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "VitaClaw Project",
        "authority_tier": "official_github_repository",
        "dimension": "licensing",
        "tags": ["vitaclaw", "licensing", "MIT", "official"],
        "body": """# MIT License — VitaClaw

Copyright (c) 2024-2026 VitaClaw Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**License details:**
- License Type: MIT
- License File: LICENSE at repository root
- Version/Commit at Retrieval: main branch, commit a3f8c21
- Per-Component Licensing: All components under the same MIT license.
  No dual licensing or per-module license differences.
""",
    },
    {
        "doc_id": "DOC-005",
        "title": "VitaClaw Deployment Guide — Offline Installation",
        "source": "VitaClaw Official Documentation",
        "canonical_url": "https://docs.vitaclaw.dev/deployment/offline",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "VitaClaw Project",
        "authority_tier": "official_documentation",
        "dimension": "offline_deployment",
        "tags": ["vitaclaw", "offline_deployment", "deployment", "official"],
        "body": """# VitaClaw Offline Deployment

## Core Harness Offline Operation

VitaClaw supports offline operation with pre-staged dependencies. The core harness
(agent loop, skill loader, tool system) operates without network access once
dependencies are installed.

## Pre-Staging Requirements

For complete offline operation, the following must be pre-staged:

1. **Python Dependencies**: Install all pip packages before going offline.
   Use `pip download -r requirements.txt -d ./offline-packages/` to cache.

2. **Docker Images**: Pre-pull any Docker images used by the sandbox.
   Use `docker pull <image> && docker save <image> -o offline-images.tar`.

3. **Model Inference**: VitaClaw uses cloud API providers by default (OpenAI, Anthropic).
   For fully offline operation, configure a local model endpoint:
   - Local LLM: Use ollama, vLLM, or llama.cpp with OpenAI-compatible API
   - Set `model_provider: local` and `model_endpoint: http://localhost:11434/v1`

## Skill Installation Network Requirements

- **Initial Install**: Network required for `vitaclaw install <skill>` from registry
- **Post-Install Offline**: Once a skill is cached in `~/.vitaclaw/skills/`, it can be
  loaded without network
- **Local Directory Mount**: Skills installed via directory mount require no network at any stage

## Feature Degradation Offline

| Feature | Online | Offline |
|---------|--------|---------|
| Core agent loop | ✓ | ✓ |
| Skill loading | ✓ | ✓ (pre-cached) |
| File operations | ✓ | ✓ |
| Shell execution | ✓ | ✓ |
| Web search | ✓ | ✗ |
| Browser automation | ✓ | ✗ |
| MCP tools (local) | ✓ | ✓ |
| MCP tools (remote) | ✓ | ✗ |
| Skill registry | ✓ | ✗ |

## Distinction: Initial Install vs Post-Install

- **Initial Install**: Network required for package download and Docker image pull
- **Post-Install Offline**: Full agent functionality (minus web/browser tools) works without network
""",
    },

    # ── OpenClaw — Official ──
    {
        "doc_id": "DOC-006",
        "title": "OpenClaw: Personal AI Assistant — README",
        "source": "GitHub openclaw/openclaw README.md",
        "canonical_url": "https://github.com/openclaw/openclaw/blob/main/README.md",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "OpenClaw",
        "authority_tier": "official_github_repository",
        "dimension": "skill_installation",
        "tags": ["openclaw", "skill_installation", "overview", "official"],
        "body": """# OpenClaw: Personal AI Assistant

OpenClaw is a personal AI assistant you run on your own devices. It answers you on
the channels you already use. It can speak and listen on your phone, respond to
messages on Telegram and Discord, and work alongside you in the terminal.

## Skill Installation

OpenClaw uses a skill-based architecture where capabilities are added through
Markdown-based skill files.

### Installation Methods

1. **Local Directory**: Place skills under `~/.openclaw/workspace/skills/<skill-name>/`.
   Each skill requires a `SKILL.md` file. Skills are auto-discovered at startup.

2. **Package Manager**: OpenClaw supports skill installation via its built-in registry:
   `openclaw skill install <skill-name>`. Skills are downloaded to the local workspace.

3. **Git-Based Skills**: Clone skill repositories directly into the workspace:
   ```bash
   git clone <skill-repo> ~/.openclaw/workspace/skills/<skill-name>
   ```

4. **Third-Party Format Support**: OpenClaw supports skills in the agentskills.io
   open standard format. It is also compatible with anthropics/skills format.

### Workspace Organization

```text
~/.openclaw/workspace/
├── skills/          # Skill definitions (SKILL.md files)
├── memory/          # Persistent memory files
└── configs/         # Workspace-specific configuration
```

### Restart/Reload

Skills are loaded at agent initialization. Adding new skills requires an agent
restart or `openclaw skill reload` command.
""",
    },
    {
        "doc_id": "DOC-007",
        "title": "OpenClaw Tool System — Official Documentation",
        "source": "OpenClaw Official Documentation",
        "canonical_url": "https://docs.openclaw.dev/tools",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "OpenClaw",
        "authority_tier": "official_documentation",
        "dimension": "tool_invocation",
        "tags": ["openclaw", "tool_invocation", "MCP", "official"],
        "body": """# OpenClaw Tool System

## Tool Architecture

OpenClaw provides a modular tool system. Tools are defined as TypeScript modules
with a standard interface. Each tool declares its schema (name, description,
parameters) and implements an execute function.

## Built-in Tools

OpenClaw ships with 40+ built-in tools organized into categories:

| Category | Count | Examples |
|----------|-------|----------|
| File Operations | 10 | Read, Write, Edit, Glob, Grep, Delete |
| Shell & Execution | 3 | Bash, Process management, Background tasks |
| Web & Search | 5 | Web fetch, Web search, Browser automation |
| Communication | 4 | Telegram, Discord, Slack, WhatsApp |
| Knowledge & Memory | 5 | MEMORY.md, CLAUDE.md, Context injection |
| Development | 6 | Git, LSP, Code intelligence |
| MCP Integration | 3 | MCP client, MCP server, MCP resource |

## MCP Support

OpenClaw has comprehensive MCP (Model Context Protocol) support:
- Connect to any MCP-compatible server
- Expose OpenClaw tools as MCP servers for other agents
- Support for both stdio and HTTP/SSE transports
- MCP tools are available alongside native tools in the same tool registry

## Custom Tool Extension

Developers can create custom tools by implementing the Tool interface:

```typescript
interface Tool {
  name: string;
  description: string;
  parameters: JSONSchema;
  execute(params: Record<string, unknown>): Promise<ToolResult>;
}
```

Custom tools are placed in `~/.openclaw/tools/` and auto-discovered.

## Permission & Approval

OpenClaw supports a tiered permission system:
- **Auto-allow**: Read-only operations (file read, search)
- **Ask**: Potentially destructive operations (file write, shell exec)
- **Require Confirmation**: High-risk operations (git push, system config changes)
- **Deny**: Explicitly blocked operations

Permissions can be scoped by path, command pattern, or domain.
""",
    },
    {
        "doc_id": "DOC-008",
        "title": "OpenClaw Execution Sandbox — Documentation",
        "source": "OpenClaw Official Documentation",
        "canonical_url": "https://docs.openclaw.dev/security/sandbox",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "OpenClaw",
        "authority_tier": "official_documentation",
        "dimension": "sandbox",
        "tags": ["openclaw", "sandbox", "security", "official"],
        "body": """# OpenClaw Execution Sandbox

## Sandbox Overview

OpenClaw provides Docker-based execution sandboxing for running untrusted code,
shell commands, and third-party tools in an isolated environment.

### Sandbox Features

- **Isolation Type**: Docker container-based isolation
- **Default State**: Sandbox is **enabled by default** for shell execution.
  Can be disabled in configuration.
- **Workspace Mount Mode**: The agent workspace is mounted inside the container.
  Default is read-write within a volume mount; can be set to read-only.
- **Network Access**: Configurable per sandbox session:
  - `none`: Completely isolated (default for untrusted execution)
  - `bridge`: Access to host network
  - `restricted`: Allow-listed domains only
- **Filesystem**: Container root filesystem is ephemeral. Workspace mount persists
  across sessions if using a named volume.

### Configuration

```yaml
sandbox:
  enabled: true          # default
  engine: docker         # docker, podman
  default_network: none
  workspace_mode: volume
  memory_limit: 2g
  cpu_limit: 2
  timeout: 300           # seconds
```

## Additional Isolation Options

- **Process-Level**: For environments without Docker, OpenClaw can use
  process-level isolation with `chroot` on Linux
- **Resource Limits**: CPU, memory, and I/O limits configurable
- **Seccomp Profiles**: Custom seccomp profiles for fine-grained syscall filtering
- **Network Egress Rules**: Per-domain allow/deny lists for network access

## Filesystem Restrictions

- No access to host filesystem outside workspace volume
- `/proc`, `/sys`, `/dev` restricted
- Sensitive paths (`~/.ssh`, `~/.aws`, `~/.config`) excluded from mounts
""",
    },
    {
        "doc_id": "DOC-009",
        "title": "OpenClaw — LICENSE",
        "source": "GitHub openclaw/openclaw LICENSE",
        "canonical_url": "https://github.com/openclaw/openclaw/blob/main/LICENSE",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "OpenClaw",
        "authority_tier": "official_github_repository",
        "dimension": "licensing",
        "tags": ["openclaw", "licensing", "Apache-2.0", "official"],
        "body": """# Apache License 2.0 — OpenClaw

Copyright 2024-2026 OpenClaw Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

**License details:**
- License Type: Apache License 2.0
- License File: LICENSE at repository root
- Version/Commit at Retrieval: main branch, v2.5.0
- Per-Component Licensing: Core engine is Apache 2.0. MCP integration module
  uses MIT license. All other components Apache 2.0. See NOTICE file for details.
""",
    },
    {
        "doc_id": "DOC-010",
        "title": "OpenClaw Deployment Guide — Offline & Air-Gapped",
        "source": "OpenClaw Official Documentation",
        "canonical_url": "https://docs.openclaw.dev/deployment/offline",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "OpenClaw",
        "authority_tier": "official_documentation",
        "dimension": "offline_deployment",
        "tags": ["openclaw", "offline_deployment", "deployment", "official"],
        "body": """# OpenClaw Offline & Air-Gapped Deployment

## Offline Operation Support

OpenClaw supports running in air-gapped and offline environments. The core agent
loop, tool execution, and skill system do not require internet access once
initial setup is complete.

## Pre-Staging for Offline

### Dependencies
- Node.js runtime and npm packages must be installed before going offline
- Use `npm pack` to create offline-installable package archives
- Docker images must be pre-pulled and saved

### Model Inference
OpenClaw connects to LLM providers via API. For offline operation:
- Configure a local LLM endpoint (ollama, vLLM, LocalAI)
- Set `provider: local` in configuration
- Pre-download model weights before going offline

### Docker Images
```bash
docker pull node:20-alpine
docker pull openclaw/sandbox:latest
docker save node:20-alpine openclaw/sandbox:latest -o offline-images.tar
```

## Skill Installation Offline

- **Path-Based Skills**: Skills installed by local directory path require no network
- **Registry Skills**: Skills installed via `openclaw skill install` require
  network on first install. After caching, they work offline.
- **Git-Based Skills**: Require network for initial clone. After cloning, work offline.

## Feature Degradation

| Feature | Online | Offline |
|---------|--------|---------|
| Agent loop | ✓ | ✓ |
| Skill system | ✓ | ✓ |
| File operations | ✓ | ✓ |
| Shell execution | ✓ | ✓ |
| Docker sandbox | ✓ | ✓ (pre-pulled images) |
| Web search | ✓ | ✗ |
| Web fetch | ✓ | ✗ |
| Browser automation | ✓ | ✗ |
| Telegram/Discord/W | ✓ | ✗ |
""",
    },

    # ── Hermes — Official ──
    {
        "doc_id": "DOC-011",
        "title": "Hermes Agent — README (Getting Started & Installation)",
        "source": "GitHub NousResearch/hermes-agent README.md",
        "canonical_url": "https://github.com/NousResearch/hermes-agent/blob/main/README.md",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "Nous Research",
        "authority_tier": "official_github_repository",
        "dimension": "skill_installation",
        "tags": ["hermes", "skill_installation", "overview", "official"],
        "body": """# Hermes Agent

**The self-improving AI agent built by Nous Research.** It's the only agent with
a built-in learning loop — it creates skills from experience, improves them during
use, nudges itself to persist knowledge, searches its own past conversations, and
builds a deepening model of who you are across sessions.

Run it on a $5 VPS, a GPU cluster, or serverless infrastructure that costs nearly
nothing when idle.

## Quickstart — Installation

```bash
# Install Hermes Agent
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Run the setup wizard
hermes setup

# Start a conversation
hermes
```

## Skill Installation

Hermes uses a skill-based architecture compatible with the agentskills.io open standard.

### Installation Methods

1. **Skills Hub**: Browse and install skills from the community hub:
   `hermes skill install <skill-name>`. Skills are stored in `~/.hermes/skills/`.

2. **Local Directory**: Place SKILL.md files under `~/.hermes/skills/<skill-name>/`.
   Hermes discovers skills automatically at startup.

3. **Auto-Generated Skills**: Hermes can autonomously create skills from completed
   tasks. After a complex multi-step task, Hermes prompts: "Create a skill from this?"
   Auto-generated skills are stored alongside manually installed ones.

4. **Third-Party Formats**: Hermes is compatible with the agentskills.io open standard
   and can import skills from OpenClaw and VitaClaw via `hermes skill import`.

### Skill Self-Improvement

A unique Hermes feature: skills self-improve during use. When a skill is invoked
and produces suboptimal results, Hermes can update the skill's instructions based
on what it learned. This is configurable and can be disabled.

## Restart/Reload

Skills are hot-loaded — no restart required. Use `hermes skill reload` to force
re-scan the skills directory.
""",
    },
    {
        "doc_id": "DOC-012",
        "title": "Hermes Agent Tools & Toolsets — Documentation",
        "source": "Hermes Agent Official Documentation",
        "canonical_url": "https://hermes-agent.nousresearch.com/docs/user-guide/features/tools",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "Nous Research",
        "authority_tier": "official_documentation",
        "dimension": "tool_invocation",
        "tags": ["hermes", "tool_invocation", "MCP", "official"],
        "body": """# Hermes Agent — Tools & Toolsets

## Tool Architecture

Hermes provides 40+ built-in tools organized into toolsets. Tools are Python modules
that implement a standard interface.

## Built-in Toolsets

| Toolset | Description |
|---------|-------------|
| File System | Read, Write, Edit, Glob, Grep operations |
| Shell & Process | Bash execution, background tasks, process management |
| Web & Search | Web fetch, web search with multiple engines |
| Browser | Playwright-based browser automation |
| Git | Clone, commit, push, pull, branch management |
| Code Intelligence | LSP integration, code search, symbol lookup |
| MCP Client | Connect to external MCP servers |
| MCP Server | Expose Hermes tools as MCP endpoints |

## MCP Support

Hermes supports MCP (Model Context Protocol) as both client and server:
- **MCP Client**: Connect to any MCP server. Tools are auto-discovered and added
  to the agent's tool palette.
- **MCP Server**: Expose Hermes tools to other agents and tools that speak MCP.
- **Transport**: Supports stdio and HTTP/SSE transports.

## Shell / Exec Capability

Hermes provides shell execution through the `bash` tool:
- Persistent shell sessions
- Configurable timeouts
- Working directory control
- Output streaming for long-running commands

## Custom Tool Extension

Custom tools are created by adding Python modules to `~/.hermes/tools/`:

```python
from hermes.tools import Tool, ToolResult

class MyTool(Tool):
    name = "my_tool"
    description = "Does something useful"

    async def execute(self, **params) -> ToolResult:
        # Implementation
        return ToolResult(content="Done")
```

Custom tools are auto-discovered at startup.

## Tool Permissions

Hermes supports command approval and tool permission modes:
- Interactive approval dialogs for shell commands
- Workspace-scoped permission overrides
- Blocklists for dangerous operations
- DM pairing for messaging platform security
""",
    },
    {
        "doc_id": "DOC-013",
        "title": "Hermes Agent Security & Container Isolation — Documentation",
        "source": "Hermes Agent Official Documentation",
        "canonical_url": "https://hermes-agent.nousresearch.com/docs/user-guide/security",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "Nous Research",
        "authority_tier": "official_documentation",
        "dimension": "sandbox",
        "tags": ["hermes", "sandbox", "security", "official"],
        "body": """# Hermes Agent — Security & Container Isolation

## Security Overview

Hermes Agent provides multiple layers of security for agent execution including
command approval, container isolation, and DM pairing.

## Container Isolation

Hermes supports running agent operations inside isolated containers:

### Sandbox Features

- **Isolation Type**: Docker container-based isolation via terminal backends
- **Default State**: Container isolation is **optional** — users must explicitly
  configure a containerized terminal backend (Docker, Singularity, Daytona, Modal, Vercel Sandbox)
- **Seven Terminal Backends**:
  1. **Local**: Runs directly on host (no isolation)
  2. **Docker**: Container-based isolation with configurable mounts
  3. **SSH**: Remote execution via SSH
  4. **Singularity**: HPC-friendly container runtime
  5. **Modal**: Serverless GPU-enabled containers
  6. **Daytona**: Serverless development environments
  7. **Vercel Sandbox**: Cloud sandbox environment

### Docker Backend Configuration

```yaml
terminal:
  backend: docker
  image: hermes-agent:latest
  workspace_mount: /workspace
  network: bridge
  memory_limit: 4g
  cpu_limit: 2
```

### Network and Filesystem

- **Network**: Configurable per-backend. Docker backend supports `none`, `bridge`,
  and `host` networking.
- **Filesystem**: Each backend manages filesystem isolation independently.
  Local backend has no filesystem isolation. Docker backend uses container
  filesystem with workspace volume mount.

## Command Approval

Shell commands can be configured to require user approval:
- `auto`: Auto-approve all commands
- `ask`: Prompt for approval on each command
- `deny`: Block shell execution entirely

## DM Pairing

For messaging platforms (Telegram, Discord, WhatsApp), Hermes supports DM pairing
to ensure only authorized users can control the agent.
""",
    },
    {
        "doc_id": "DOC-014",
        "title": "Hermes Agent — LICENSE",
        "source": "GitHub NousResearch/hermes-agent LICENSE",
        "canonical_url": "https://github.com/NousResearch/hermes-agent/blob/main/LICENSE",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "Nous Research",
        "authority_tier": "official_github_repository",
        "dimension": "licensing",
        "tags": ["hermes", "licensing", "MIT", "official"],
        "body": """# MIT License — Hermes Agent

Copyright (c) 2025-2026 Nous Research

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**License details:**
- License Type: MIT
- License File: LICENSE at repository root (main branch)
- Version/Commit at Retrieval: v2026.7.7.2
- Per-Component Licensing: All core components under MIT. Third-party
  integrations (MCP servers, plugins) may have their own licenses.
  See NOTICE file for complete attribution.
""",
    },
    {
        "doc_id": "DOC-015",
        "title": "Hermes Agent Offline Operation — Documentation",
        "source": "Hermes Agent Official Documentation",
        "canonical_url": "https://hermes-agent.nousresearch.com/docs/user-guide/configuration",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "Nous Research",
        "authority_tier": "official_documentation",
        "dimension": "offline_deployment",
        "tags": ["hermes", "offline_deployment", "official"],
        "body": """# Hermes Agent — Offline Operation

## Offline Capabilities

Hermes Agent can operate in offline mode with some feature degradation.

### Core Operation Offline

- **Agent Loop**: Fully functional without network
- **Skill System**: Skills work offline once installed/cached
- **File Operations**: Fully functional
- **Memory & Context**: Persistent memory works offline
- **FTS5 Session Search**: Local full-text search works offline

### Network-Dependent Features

- **Model Inference**: Requires network by default (cloud API). For offline:
  configure a local provider via `hermes model` (ollama, vLLM, llama.cpp)
- **Web Search & Fetch**: Not available offline
- **Browser Automation**: Not available offline
- **Messaging Gateway**: Telegram, Discord, WhatsApp require network
- **Skills Hub**: Browsing and installing from hub requires network
- **Package Updates**: `hermes update` requires network

## Deployment Models

Hermes supports six terminal backends for different deployment scenarios:

1. **Local**: Direct host execution — no isolation, no network restrictions
2. **Docker**: Container-based with configurable network
3. **SSH**: Remote execution
4. **Singularity**: HPC environments
5. **Modal**: Serverless GPU — network available
6. **Daytona**: Serverless dev environments — network available

## Offline Configuration

```bash
# Set local model provider for offline inference
hermes model --provider ollama --model llama3.1:8b

# Pre-download skills for offline use
hermes skill install <skill-name>  # do this while online
```

## Skill Installation Network Requirements

- **Skills Hub**: Network required for discovery and download
- **Local Skills**: No network required (already on disk)
- **Auto-Generated Skills**: No network required (created locally)
- **Import from Other Frameworks**: Network required for initial import

## Distinction: Initial Install vs Post-Install

- **Initial Install**: `curl | bash` installer requires network. Python
  dependencies and model weights must be downloaded.
- **Post-Install Offline**: Core agent, local skills, local tools, and memory
  work without network. Cloud-dependent features degrade gracefully.
""",
    },

    # ── Community Discussion / Distractors ──
    {
        "doc_id": "DOC-016",
        "title": "Reddit Discussion: OpenClaw vs Hermes — Which is better for offline use?",
        "source": "Reddit r/aiagents",
        "canonical_url": "https://www.reddit.com/r/aiagents/comments/example_offline_comparison",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "Reddit Community",
        "authority_tier": "community_discussion",
        "dimension": "offline_deployment",
        "tags": ["openclaw", "hermes", "community_discussion", "comparison"],
        "body": """# Reddit Discussion: OpenClaw vs Hermes — Offline Use

**Posted by u/AIExplorer42** — 2026-06-15

I've been testing both OpenClaw and Hermes for a project that requires fully
offline operation (air-gapped environment). Here's what I found:

**OpenClaw:**
- Works well offline once dependencies are pre-staged
- Docker sandbox works offline with pre-pulled images
- Telegram/Discord obviously don't work
- Solid documentation for air-gapped setup

**Hermes:**
- Core agent works offline fine
- But the "self-improving skills" feature calls out to cloud APIs for the
  improvement step — so that part doesn't work offline
- Terminal backends Modal/Daytona need network obviously, but Docker/Singularity
  work offline
- Documentation for offline is scattered across pages

**My Verdict:** OpenClaw is better for offline use, but Hermes has a richer
feature set when online.

**Top Comment by u/DevOpsNinja:** I've run both in air-gapped environments.
OpenClaw's offline docs are better organized. Hermes works but you lose the
skill improvement feature which is its main selling point. For pure offline
CLI agent work, I'd go OpenClaw.
""",
    },
    {
        "doc_id": "DOC-017",
        "title": "Hacker News Discussion: Are AI agent sandboxes really secure?",
        "source": "Hacker News",
        "canonical_url": "https://news.ycombinator.com/item?id=example_sandbox_security",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "Hacker News Community",
        "authority_tier": "community_discussion",
        "dimension": "sandbox",
        "tags": ["sandbox", "security", "community_discussion", "cross_harness"],
        "body": """# Hacker News: Are AI Agent Sandboxes Really Secure?

**Discussion from July 2026** — 187 comments

The thread discusses sandbox security across VitaClaw, OpenClaw, and Hermes.

**Key points from the discussion:**

- Multiple users report that VitaClaw's sandbox is "opt-in and buried in docs"
  — most users run without it
- OpenClaw enables Docker sandbox by default, which several security researchers praise
- Hermes' approach of offering 7 backends is described as "flexible but confusing"
  — the default local backend has no isolation
- One user demonstrated a proof-of-concept escape from the OpenClaw sandbox via
  a Docker socket mount — fixed in v2.4.1
- Concern that all three harnesses allow shell access by default — the sandbox
  is the only defense against `rm -rf /` type commands

**Notable comment by security researcher @seceng:**
"The sandbox is your last line of defense. If your agent can execute arbitrary
shell commands, you need isolation at the OS level. Docker is good, VM-level
is better, and none of these harnesses offer VM-level isolation out of the box."
""",
    },
    {
        "doc_id": "DOC-018",
        "title": "NOT_PUBLICLY_DOCUMENTED: VitaClaw Offline Deployment — Official Docs Gap",
        "source": "Research Synthesis",
        "canonical_url": "NOT_APPLICABLE",
        "snapshot_date": SNAPSHOT_DATE,
        "publisher": "N/A",
        "authority_tier": "NOT_APPLICABLE",
        "dimension": "offline_deployment",
        "tags": ["vitaclaw", "offline_deployment", "not_documented"],
        "body": """# NOT_PUBLICLY_DOCUMENTED: VitaClaw Offline Deployment

## Research Finding

As of the snapshot date (2026-07-10), VitaClaw's public documentation does not
contain a dedicated page or comprehensive guide for offline/air-gapped deployment.

### What Is Documented

- The core agent loop, skill loading, and tool system do not inherently require
  network access once dependencies are present
- Skills installed via local directory mount require no network
- The deployment guide mentions Docker image pre-staging as a prerequisite for
  some production setups

### What Is NOT Documented

- No explicit "Offline Deployment" or "Air-Gapped Installation" guide
- No documented procedure for pre-staging all dependencies (pip packages,
  Docker images, model weights)
- No documented feature degradation matrix showing what works offline vs online
- No documented procedure for verifying an offline installation
- No guidance on model inference without cloud API access

### Note

This does NOT mean VitaClaw cannot operate offline — it means the official
documentation does not explicitly cover this scenario. The harness may work
offline with proper pre-staging, but this is not officially documented or
supported as of the snapshot date.
""",
    },
]

# ── Generate documents ───────────────────────────────────────────────────

CORPUS_DIR.mkdir(parents=True, exist_ok=True)

manifest_entries = []
index: dict[str, list[dict]] = {}

for doc in DOCUMENTS:
    doc["content_hash"] = sha256(doc["body"])

    # Write corpus file
    text = frontmatter(doc)
    fname = f"{doc['doc_id']}.md"
    (CORPUS_DIR / fname).write_text(text, encoding="utf-8")

    # Add to manifest
    manifest_entries.append({
        "doc_id": doc["doc_id"],
        "title": doc["title"],
        "source": doc["source"],
        "dimension": doc["dimension"],
        "canonical_url": doc["canonical_url"],
        "snapshot_date": doc["snapshot_date"],
        "content_hash": doc["content_hash"],
        "publisher": doc["publisher"],
        "authority_tier": doc["authority_tier"],
        "commit_or_version": doc.get("commit_or_version", "UNAVAILABLE"),
        "tags": doc.get("tags", []),
    })

    # Build index: tokenize title + body
    text_for_index = f"{doc['title']} {doc['body']}".lower()
    tokens = set(text_for_index.split())
    for token in tokens:
        # Clean token: remove punctuation, keep alphanumeric
        token_clean = "".join(c for c in token if c.isalnum())
        if not token_clean or len(token_clean) < 2:
            continue
        if token_clean not in index:
            index[token_clean] = []
        # Simple TF score
        count = text_for_index.split().count(token)
        index[token_clean].append({
            "doc_id": doc["doc_id"],
            "score": count,
        })

# ── Write manifest ───────────────────────────────────────────────────────

manifest = {
    "document_count": len(manifest_entries),
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "generated_by": "generate-corpus.py",
    "corpus_version": "1.0.0",
    "documents": manifest_entries,
}
MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

# ── Write search index ────────────────────────────────────────────────────

INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Generated {len(manifest_entries)} corpus documents in {CORPUS_DIR}")
print(f"Manifest: {MANIFEST_PATH}")
print(f"Index: {INDEX_PATH} ({len(index)} terms)")
