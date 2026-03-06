```skill
---
name: installing-bundles
description: >
  Searches, installs, updates, and removes skill bundles from the Phaylanx
  registry. Handles natural language search against the catalog, git
  sparse-checkout for content fetch (with GitHub API fallback), and local
  file placement. Invoke with /installing-bundles or when the user asks to
  add capabilities, install a bundle, or extend the system.
allowed-tools: Terminal
metadata:
  author: phaylanx
  version: "1.0"
  spec: agentskills.io/1.0
---

# Bundle Installation Workflow

Manages the lifecycle of optional bundles from the Phaylanx registry.

---

## Step 1 — Understand the Request

Parse the user's intent:
- **Search**: "what bundles are available?", "find cloud skills", "what can I install?"
- **Install**: "install the presentations bundle", "add cloud architecture"
- **Update**: "update my bundles", "refresh proposals"
- **Remove**: "remove the media bundle", "uninstall IaC"
- **List installed**: "what bundles do I have?", "show installed"

---

## Step 2 — Load Registry Configuration

Read `config.yaml` at project root and find the `registry:` section:

```yaml
registry:
  url: https://github.com/luckybob34/phaylanx
  branch: main
  auth_env: GITHUB_PAT          # optional for public repos
  cache_dir: .tmp/registry-cache
  cache_ttl: 3600               # seconds before re-fetching catalog
```

If no `registry:` section exists, use defaults:
- url: `https://github.com/luckybob34/phaylanx`
- branch: `main`

---

## Step 3 — Run the Registry Tool

All operations go through `registry.py`:

```bash
# Search bundles by natural language query
python tools/platform/registry.py --search "cloud architecture"

# List all available bundles
python tools/platform/registry.py --list

# Show installed bundles
python tools/platform/registry.py --installed

# Install a bundle
python tools/platform/registry.py --install cloud-architecture

# Update a specific bundle
python tools/platform/registry.py --update cloud-architecture

# Update all installed bundles
python tools/platform/registry.py --update-all

# Remove a bundle
python tools/platform/registry.py --remove cloud-architecture
```

---

## Step 4 — Post-Install Actions

After any install or update:

1. **Verify files**: Confirm all expected files from the bundle manifest landed correctly
2. **Update manifests**: Run `python tools/platform/generate_instructions.py` to regenerate platform files
3. **Report**: Tell the user what was installed, which skills are now available, and any agents added
4. **Memory**: Write an event to memory noting the bundle installation

After any removal:

1. **Clean files**: Confirm all bundle files were removed
2. **Update manifests**: Regenerate platform files
3. **Report**: Confirm what was removed

---

## Step 5 — Handle Errors

| Error | Resolution |
|-------|-----------|
| No internet / git unavailable | Tell user, suggest manual download from GitHub |
| Bundle not found | Show closest matches from catalog |
| Partial install (some files missing) | Retry with `--install --force`, or fall back to API fetch |
| Auth required but no PAT | Explain: set `GITHUB_PAT` in `.env` or `.credentials/.env` |
| Conflicting files exist | Warn user, ask before overwriting |

---

## Edge Cases

- If the user asks for a capability by description rather than bundle name, search the catalog first
- Multiple bundles can be installed in sequence: process them one at a time
- Some bundles share agents — installing a second bundle that needs the same agent should skip the duplicate copy
- The `core/` directory is never modified by bundle operations — it's read-only after bootstrap
```
