---
name: restoring-system
description: >
  Detects and repairs missing or corrupt framework components. Use when
  directories, manifests, databases, or skill files are missing. Handles
  first-run initialization and disaster recovery. Invoke with /restoring-system.
user-invocable: true
disable-model-invocation: true
allowed-tools: Bash(python:*) Bash(mkdir:*) Read Write
metadata:
  author: phalanx
  version: "1.0"
---

# System Restoration Protocol

## When to use

- First session in a new or corrupted environment
- After accidental file deletion
- When `healthcheck.py` reports failures
- When commands fail due to missing infrastructure

## Step 1 — Run health check

```bash
python .claude/skills/restoring-system/scripts/healthcheck.py
```

This checks all required directories, files, and databases. It reports what's missing and returns exit code 0 (healthy) or 1 (needs repair).

## Step 2 — Repair missing components

Based on the health check output, repair in this order:

### A. Core directories

```bash
mkdir -p .claude/skills
mkdir -p .claude/agents
mkdir -p tools/memory
mkdir -p context
mkdir -p memory/logs
mkdir -p data
mkdir -p workspace
mkdir -p .tmp
```

### B. Memory infrastructure

If `memory/MEMORY.md` is missing — this is the primary "fresh environment" indicator:

1. Create `memory/MEMORY.md` with default template:

```markdown
# Persistent Memory

> Curated long-term facts, preferences, and context that persist across sessions.
> Read at session start. Edit directly to update.

## User Preferences

- (Add your preferences here)

## Key Facts

- (Add key facts about your work/projects)

## Learned Behaviors

- Always check .claude/skills/manifest.md before starting a task
- Always check tools/manifest.md before creating new scripts
- Follow GOTCHA framework: Skills, Orchestration, Tools, Context, Config

## Current Projects

- (List active projects)

## Technical Context

- Framework: GOTCHA (Skills Edition) — agentskills.io aligned
```

2. Create today's daily log in `memory/logs/YYYY-MM-DD.md`

3. Initialize SQLite databases:

```bash
python .claude/skills/restoring-system/scripts/healthcheck.py --repair
```

### C. Manifests

If `.claude/skills/manifest.md` is missing:
- Scan `.claude/skills/*/SKILL.md` and regenerate the manifest from frontmatter

If `tools/manifest.md` is missing:
- Scan `tools/` for Python scripts and generate a stub manifest
- Flag to user that descriptions need manual review

### D. Skills validation

```bash
python .claude/skills/creating-skills/scripts/validate-skill.py --all .claude/skills/
```

Fix any validation issues found.

## Step 3 — Verify

Run the health check again to confirm all issues are resolved:

```bash
python .claude/skills/restoring-system/scripts/healthcheck.py
```

Confirm to user: "System restored. All components healthy."

---

## Edge Cases

- **Partial corruption**: If only some files are missing, repair only what's needed. Don't overwrite existing files.
- **Database corruption**: If SQLite files exist but are corrupt, back up the corrupt file to `.tmp/` and recreate.
- **Skill directory exists but SKILL.md missing**: Flag as an error — skill directories without SKILL.md are invalid.
- **Tools exist but no manifest**: Generate manifest from file scan, mark all entries as "description pending review".
