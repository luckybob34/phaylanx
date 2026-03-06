#!/usr/bin/env python3
"""
Generate platform-specific instruction files from skill definitions.

Reads all SKILL.md files and produces:
  - .github/copilot-instructions.md  (GitHub Copilot)
  - AGENTS.md                        (OpenAI Codex)

Usage:
    python generate_instructions.py                  # Auto-detect project root
    python generate_instructions.py --root /path      # Explicit root
    python generate_instructions.py --dry-run         # Preview without writing
"""

import re
import sys
from pathlib import Path
from datetime import datetime


# ── Frontmatter Parsing ──────────────────────────────────────────────────────

def _strip_code_fence(content: str) -> str:
    """Strip ```skill or ````skill code-fence wrapper if present."""
    lines = content.splitlines()
    if not lines:
        return content
    first = lines[0].strip()
    if re.match(r'^`{3,}\s*skill\b', first, re.IGNORECASE):
        lines = lines[1:]
        if lines and re.match(r'^`{3,}\s*$', lines[-1].strip()):
            lines = lines[:-1]
    return "\n".join(lines)


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md content."""
    content = _strip_code_fence(content)
    stripped = content.lstrip("\n")
    if not stripped.startswith("---"):
        return {}

    end = stripped.find("\n---", 3)
    if end == -1:
        return {}

    fm_text = stripped[3:end].strip()

    fm = {}
    current_key = None
    current_value = []
    in_list = False

    for line in fm_text.split("\n"):
        line_stripped = line.strip()

        if in_list and line_stripped.startswith("- "):
            fm[current_key].append(line_stripped[2:].strip())
            continue
        elif in_list and line_stripped and not line_stripped.startswith("-"):
            in_list = False

        match = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line)
        if match:
            if current_key and current_key not in fm:
                val = "\n".join(current_value).strip()
                if val.startswith(">"):
                    val = val[1:].strip()
                fm[current_key] = val

            current_key = match.group(1)
            value = match.group(2).strip()

            if value == ">":
                current_value = []
                in_list = False
            elif value == "":
                fm[current_key] = []
                current_value = []
                in_list = True
            elif value.lower() == "true":
                fm[current_key] = True
                current_value = []
                in_list = False
            elif value.lower() == "false":
                fm[current_key] = False
                current_value = []
                in_list = False
            elif value.startswith('"') and value.endswith('"'):
                fm[current_key] = value[1:-1]
                current_value = []
                in_list = False
            else:
                fm[current_key] = value
                current_value = []
                in_list = False
        elif current_key:
            current_value.append(line)

    if current_key and current_key not in fm:
        val = "\n".join(current_value).strip()
        if val.startswith(">"):
            val = val[1:].strip()
        fm[current_key] = val

    return fm


# ── Skill Classification ─────────────────────────────────────────────────────

def classify_skill(fm: dict) -> str:
    """Classify a skill as workflow, atomic, protocol, or meta."""
    name = fm.get("name", "")

    # Protocol skills have user-invocable: false
    if fm.get("user-invocable") is False:
        return "protocol"

    # Meta skills
    meta_names = {"creating-skills", "improving-skills", "restoring-system"}
    if name in meta_names:
        return "meta"

    # Atomic skills (template-only, no multi-step workflow)
    atomic_names = {"generating-architecture-diagrams", "generating-proposal-visuals"}
    if name in atomic_names:
        return "atomic"

    return "workflow"


def make_trigger(name: str, description: str) -> str:
    """Generate a short trigger phrase from the skill name."""
    triggers = {
        "building-pptx-decks": "User wants a PowerPoint",
        "building-html-decks": "User wants an HTML presentation",
        "responding-to-rfps": "User provides an RFP",
        "building-sow": "User needs a Statement of Work",
        "building-apps": "User wants to build an application",
        "designing-architecture": "User needs cloud architecture",
        "planning-cloud-migration": "User needs migration plan",
        "deploying-infrastructure": "User wants IaC deployment",
        "reviewing-architecture": "User wants architecture review",
        "creating-visuals": "User needs diagrams/graphics",
        "building-university-decks": "User wants a university program deck",
    }
    return triggers.get(name, "Matches description")


def make_short_description(name: str, description: str) -> str:
    """Generate a short description for the skills table."""
    # Truncate at first sentence or 80 chars
    desc = str(description)
    # Try to extract the key phrase (after the first dash or period)
    parts = desc.split(" — ")
    if len(parts) > 1:
        return parts[-1][:80]
    if len(desc) > 80:
        return desc[:77] + "..."
    return desc


# ── Template Generation ──────────────────────────────────────────────────────

SYSTEM_IDENTITY = """## System Identity

You are the orchestration layer of the **GOTCHA Framework** — a 6-layer architecture for agentic systems. You make smart decisions and delegate work to deterministic tools. You never execute business logic directly.

**Layers:** Goals (→ Skills) | Orchestration (→ You) | Tools (→ Scripts) | Context (→ Reference) | Hardprompts (→ Skills) | Args (→ Config)"""

OPERATING_RULES = """## Operating Rules

1. **Check manifests first** — Read `.claude/skills/manifest.md` and `tools/manifest.md` before starting any task
2. **Check tools before writing** — If a tool exists in `tools/`, use it. If you create one, add it to `tools/manifest.md`
3. **Skills activate on match** — When a task matches a skill description, read its full `SKILL.md` and follow the workflow
4. **Protocol skills are always active** — Memory, workspace, agent, and manifest protocols run automatically
5. **Delegate to agents** — When a task needs domain expertise, invoke the specialist agent per `agents/manifest.md`
6. **Workspace protocol** — Save all project outputs to `workspace/<project-slug>/`, never to `.tmp/`
7. **Memory protocol** — Read `memory/MEMORY.md` at session start; log notable events during session"""

GUARDRAILS = """## Guardrails

- Always check `tools/manifest.md` before writing a new script
- Verify tool output format before chaining into another tool
- Don't assume APIs support batch operations — check first
- When a workflow fails mid-execution, preserve intermediate outputs before retrying
- Read the full skill before starting a task — don't skim
- Always save project outputs to `workspace/<project-slug>/`
- Before starting any deliverable task, check `agents/manifest.md` for a specialist agent"""

CONTINUOUS_IMPROVEMENT = """## Continuous Improvement

Every failure strengthens the system: identify what broke → fix the tool → test → update the skill → next time it works automatically."""

FILE_STRUCTURE = """## File Structure

| Directory | Purpose |
|-----------|---------|
| `.claude/skills/` | Skill definitions (SKILL.md per directory) |
| `tools/` | Deterministic scripts organized by workflow |
| `agents/` | Specialist agent definitions (role.md + config.yaml) |
| `context/` | Reference material and domain knowledge |
| `config.yaml` | Global behavior settings |
| `workspace/` | Project outputs (permanent) |
| `memory/` | Persistent memory (MEMORY.md + daily logs) |
| `data/` | SQLite databases (memory.db, activity.db) |
| `.tmp/` | Disposable scratch work |"""


def build_skills_section(skills: dict[str, dict]) -> str:
    """Build the Available Skills section from classified skills."""
    classified = {"workflow": [], "protocol": [], "meta": [], "atomic": []}

    for name, fm in sorted(skills.items()):
        skill_type = classify_skill(fm)
        classified[skill_type].append((name, fm))

    lines = ["## Available Skills", ""]

    # Workflow skills (with trigger column)
    if classified["workflow"]:
        lines.append("### Workflow Skills")
        lines.append("")
        lines.append("| Skill | Trigger | Description |")
        lines.append("|-------|---------|-------------|")
        for name, fm in classified["workflow"]:
            desc = str(fm.get("description", ""))
            trigger = make_trigger(name, desc)
            short = make_short_description(name, desc)
            lines.append(f"| `{name}` | {trigger} | {short} |")
        lines.append("")

    # Protocol skills
    if classified["protocol"]:
        lines.append("### Protocol Skills (Always Active)")
        lines.append("")
        lines.append("| Skill | Description |")
        lines.append("|-------|-------------|")
        for name, fm in classified["protocol"]:
            desc = make_short_description(name, str(fm.get("description", "")))
            lines.append(f"| `{name}` | {desc} |")
        lines.append("")

    # Meta skills
    if classified["meta"]:
        lines.append("### Meta Skills")
        lines.append("")
        lines.append("| Skill | Description |")
        lines.append("|-------|-------------|")
        for name, fm in classified["meta"]:
            desc = make_short_description(name, str(fm.get("description", "")))
            lines.append(f"| `{name}` | {desc} |")
        lines.append("")

    # Atomic skills
    if classified["atomic"]:
        lines.append("### Atomic Skills")
        lines.append("")
        lines.append("| Skill | Description |")
        lines.append("|-------|-------------|")
        for name, fm in classified["atomic"]:
            desc = make_short_description(name, str(fm.get("description", "")))
            lines.append(f"| `{name}` | {desc} |")
        lines.append("")

    return "\n".join(lines)


def generate_copilot(skills: dict[str, dict]) -> str:
    """Generate .github/copilot-instructions.md content."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    skills_section = build_skills_section(skills)

    return f"""```instructions
# Copilot Instructions — GOTCHA Framework (Phalanx)

> Auto-generated composite of all skills for GitHub Copilot compatibility.
> Copilot does not support progressive disclosure — all skill summaries are inlined here.
> Generated: {timestamp}

---

{SYSTEM_IDENTITY}

---

{skills_section}
---

{OPERATING_RULES}

---

{GUARDRAILS}

---

{CONTINUOUS_IMPROVEMENT}

---

{FILE_STRUCTURE}

```"""


def generate_agents(skills: dict[str, dict]) -> str:
    """Generate AGENTS.md content."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    skills_section = build_skills_section(skills)

    return f"""```markdown
# AGENTS.md — GOTCHA Framework (Phalanx)

> Auto-generated composite of all skills for OpenAI Codex compatibility.
> Codex reads AGENTS.md as its system context.
> Generated: {timestamp}

---

{SYSTEM_IDENTITY}

---

{skills_section}
---

{OPERATING_RULES}

---

{GUARDRAILS}

---

{CONTINUOUS_IMPROVEMENT}

---

{FILE_STRUCTURE}

```"""


# ── CLI ───────────────────────────────────────────────────────────────────────

def find_project_root() -> Path:
    """Walk up from script location to find CLAUDE.md."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists():
            return current
        current = current.parent
    return Path.cwd()


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    root_override = None

    for i, arg in enumerate(args):
        if arg == "--root" and i + 1 < len(args):
            root_override = Path(args[i + 1])

    root = root_override or find_project_root()
    skills_dir = root / ".claude" / "skills"

    if not skills_dir.is_dir():
        print(f"Error: skills directory not found: {skills_dir}")
        sys.exit(1)

    # Scan all skills
    skills = {}
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        content = skill_file.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        if fm.get("name"):
            skills[fm["name"]] = fm

    print(f"Found {len(skills)} skills in {skills_dir}")

    # Generate files
    copilot_content = generate_copilot(skills)
    agents_content = generate_agents(skills)

    copilot_path = root / ".github" / "copilot-instructions.md"
    agents_path = root / "AGENTS.md"

    if dry_run:
        print(f"\n--- .github/copilot-instructions.md ---")
        print(copilot_content[:500] + "\n...")
        print(f"\n--- AGENTS.md ---")
        print(agents_content[:500] + "\n...")
        print(f"\nDry run complete. No files written.")
    else:
        copilot_path.parent.mkdir(parents=True, exist_ok=True)
        copilot_path.write_text(copilot_content, encoding="utf-8")
        agents_path.write_text(agents_content, encoding="utf-8")
        print(f"  Written: {copilot_path.relative_to(root)}")
        print(f"  Written: {agents_path.relative_to(root)}")
        print(f"\nDone. {len(skills)} skills synced to platform files.")

    sys.exit(0)


if __name__ == "__main__":
    main()
