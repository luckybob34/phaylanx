# Phalanx Bootstrap

> AI-readable installation playbook. Execute these steps in order to set up a new
> GOTCHA Framework (Skills Edition) instance from the Phalanx registry.

---

## Section 1 — Detect Platform

Determine which AI coding platform is running this bootstrap:

| Signal | Platform | Config Strategy |
|--------|----------|-----------------|
| `CLAUDE.md` is the entry point | **Claude Code** | Progressive disclosure via `.claude/skills/` |
| `.github/copilot-instructions.md` is loaded | **GitHub Copilot** | Flat composite instruction file |
| `AGENTS.md` is loaded | **OpenAI Codex** | Flat composite agents file |

Set `$PLATFORM` to one of: `claude`, `copilot`, `codex`.

If uncertain, ask the user. If the user doesn't know, default to `claude`.

---

## Section 2 — Verify Prerequisites

Before installing, confirm:

1. **Terminal access**: Can you run shell commands? (Required for git/API fetch)
2. **Internet access**: Can you reach `https://github.com`?
3. **Git**: Is `git` available? Run `git --version`. If not, the system falls back to API download.
4. **Python 3.8+**: Run `python --version` or `python3 --version`. Required for tools.

If any prerequisite fails, note the limitation and continue — the installer adapts.

---

## Section 3 — Create Project Structure

Create the base directory structure for a new GOTCHA Skills Edition project:

```bash
# Core framework directories
mkdir -p .claude/skills
mkdir -p .claude/agents
mkdir -p tools/memory
mkdir -p tools/platform
mkdir -p context/templates/presentations/themes
mkdir -p memory/logs
mkdir -p data
mkdir -p workspace
mkdir -p .tmp
```

---

## Section 4 — Install Core

The core is required. Fetch it from the registry.

### Option A: Git Sparse-Checkout (Preferred)

```bash
REPO="https://github.com/luckybob34/phalanx"
BRANCH="main"
CLONE_DIR=".tmp/phalanx-core"

git clone --filter=blob:none --no-checkout --depth=1 -b $BRANCH $REPO $CLONE_DIR
cd $CLONE_DIR
git sparse-checkout init --cone
git sparse-checkout set core/
git checkout
cd -
```

### Option B: GitHub API (Fallback)

If git is unavailable, use the GitHub REST API to download `core/` contents:

```
GET https://api.github.com/repos/luckybob34/phalanx/git/trees/main?recursive=1
```

Filter for entries starting with `core/` and download each blob.

### Copy Core Files

After fetching, copy files to their correct locations:

```bash
# Skills → .claude/skills/
cp -r $CLONE_DIR/core/skills/* .claude/skills/

# Tools → tools/
cp -r $CLONE_DIR/core/tools/* tools/

# Context → context/
cp -r $CLONE_DIR/core/context/* context/

# Root files
cp $CLONE_DIR/core/CLAUDE.md ./CLAUDE.md
cp $CLONE_DIR/core/config.yaml ./config.yaml

# Manifests
cp $CLONE_DIR/core/skills/manifest.md .claude/skills/manifest.md
cp $CLONE_DIR/core/tools/manifest.md tools/manifest.md

# Registry tool — also place in tools/platform/ for direct access
cp $CLONE_DIR/core/skills/installing-bundles/scripts/registry.py tools/platform/registry.py
```

---

## Section 5 — Configure Registry

Add the registry section to `config.yaml` if not already present:

```yaml
# Registry configuration
registry:
  url: https://github.com/luckybob34/phalanx
  branch: main
  auth_env: GITHUB_PAT
  cache_dir: .tmp/registry-cache
  cache_ttl: 3600
```

---

## Section 6 — Initialize Memory

Create the initial memory infrastructure:

```bash
# Create MEMORY.md
cat > memory/MEMORY.md << 'EOF'
# Persistent Memory

> Curated long-term facts, preferences, and context that persist across sessions.

## User Preferences

- (Add your preferences here)

## Key Facts

- Framework: GOTCHA Skills Edition (Phalanx)
- Installed via: Phalanx bootstrap

## Learned Behaviors

- Always check .claude/skills/manifest.md before starting a task
- Always check tools/manifest.md before writing a new script
- Follow GOTCHA framework: Skills define process, Tools execute, Context informs

## Current Projects

- (List active projects)

---

*Last updated: (date)*
EOF

# Create today's log
echo "# Daily Log: $(date +%Y-%m-%d)" > "memory/logs/$(date +%Y-%m-%d).md"
```

Initialize databases:

```bash
python3 -c "
import sqlite3
from pathlib import Path

Path('data').mkdir(exist_ok=True)

conn = sqlite3.connect('data/memory.db')
conn.execute('''CREATE TABLE IF NOT EXISTS memory_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL DEFAULT 'fact',
    content TEXT NOT NULL,
    content_hash TEXT UNIQUE,
    source TEXT DEFAULT 'session',
    confidence REAL DEFAULT 1.0,
    importance INTEGER DEFAULT 5,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_accessed DATETIME,
    access_count INTEGER DEFAULT 0,
    embedding BLOB,
    embedding_model TEXT,
    tags TEXT,
    context TEXT,
    expires_at DATETIME,
    is_active INTEGER DEFAULT 1
)''')
conn.commit()
conn.close()

conn = sqlite3.connect('data/activity.db')
conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    source TEXT,
    request TEXT,
    status TEXT DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    summary TEXT
)''')
conn.commit()
conn.close()

print('Databases initialized.')
"
```

---

## Section 7 — Generate Platform Files

Generate **all** platform entry-point files regardless of detected platform. This ensures
the project works if the user later switches platforms or uses multiple tools:

### Step 7a — Claude Code (already done)

`CLAUDE.md` was copied in Section 4. Skills in `.claude/skills/` are auto-discovered by Claude Code.

### Step 7b — GitHub Copilot + OpenAI Codex

Run the platform generator to produce both `.github/copilot-instructions.md` and `AGENTS.md`:

```bash
python tools/platform/generate_instructions.py
```

This reads all installed skill frontmatter and generates:
- `.github/copilot-instructions.md` — flat composite for GitHub Copilot
- `AGENTS.md` — flat composite for OpenAI Codex

> **Always run this step**, even for Claude Code users. It costs nothing and
> makes the project portable across all three platforms.

---

## Section 8 — Offer Bundles

Present the user with available bundles. Use natural language search if they describe what they need:

```bash
python tools/platform/registry.py --list
```

**Recommended presentation:**

> Your GOTCHA framework is installed with core skills (memory, workspaces, agents, manifests, skill creation, improvement, system restore, and bundle management).
>
> Optional bundles are available to add capabilities:
>
> | Bundle | What It Adds |
> |--------|-------------|
> | `cloud-architecture` | Cloud architecture design (AWS/Azure) |
> | `cloud-migration` | Migration planning and assessment |
> | `cloud-iac` | Infrastructure as Code (Terraform/Bicep) |
> | `cloud-review` | Architecture review and audit |
> | `presentations-html` | Interactive HTML slide decks |
> | `presentations-pptx` | PowerPoint presentations |
> | `proposals` | RFP responses and SOW generation |
> | `media` | Visual asset generation (diagrams, graphics) |
> | `app-development` | Full-stack application development |
>
> Which bundles would you like to install? You can install multiple or say "all".

---

## Section 9 — Install Selected Bundles

For each bundle the user selects:

```bash
python tools/platform/registry.py --install <bundle-name>
```

After all bundles are installed:

1. Regenerate platform files: `python tools/platform/generate_instructions.py`
2. Run health check: `python .claude/skills/restoring-system/scripts/healthcheck.py`

---

## Section 10 — Verify Installation

Run the full verification suite:

```bash
# Health check
python .claude/skills/restoring-system/scripts/healthcheck.py

# Validate all skills
python .claude/skills/creating-skills/scripts/validate-skill.py --all

# Show installed bundles
python tools/platform/registry.py --installed
```

Expected: All checks pass, all skills validate, installed bundles listed.

---

## Section 11 — Clean Up

Remove the temporary checkout:

```bash
rm -rf .tmp/phalanx-core
```

---

## Section 12 — Confirmation

Tell the user:

> ✓ GOTCHA Framework (Skills Edition) installed via Phalanx.
>
> **Core skills**: 8 (memory, workspaces, agents, manifests, skill creation, improvement, system restore, bundle management)
> **Bundles installed**: [list]
> **Platform**: [claude/copilot/codex]
>
> To add more capabilities later: "install a bundle" or `/installing-bundles`
> To update bundles: "update my bundles"
> To see what's available: "what bundles can I install?"
