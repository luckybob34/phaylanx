---
name: creating-skills
description: >
  Creates new skills following the agentskills.io open standard. Use when the
  user requests a new capability, workflow, or repeatable process that does not
  exist yet. Handles directory creation, SKILL.md authoring, frontmatter
  validation, and manifest registration.
allowed-tools: Bash(python:*) Read Write
metadata:
  author: phalanx
  version: "1.0"
  spec: agentskills.io/1.0
---

# Skill Creation Workflow

## Step 1 — Check if a skill already exists

Read `.claude/skills/manifest.md`. If an existing skill covers the request, use it instead of creating a new one.

## Step 2 — Choose a name

**Naming rules** (agentskills.io spec):
- 1-64 characters
- Lowercase letters, numbers, hyphens only
- Must NOT start or end with `-`
- No consecutive hyphens (`--`)
- **Gerund form preferred**: `processing-pdfs`, `building-apps`, `responding-to-rfps`
- Avoid vague names: `helper`, `utils`, `documents`
- No reserved words: `anthropic`, `claude`
- Directory name MUST match the `name` field in frontmatter

## Step 3 — Create directory structure

Minimal:
```
.claude/skills/<skill-name>/
└── SKILL.md
```

Full (when needed):
```
.claude/skills/<skill-name>/
├── SKILL.md              # Main instructions (required, <500 lines)
├── reference/
│   └── detailed-spec.md  # Supplementary docs (loaded when needed)
└── scripts/
    └── validate.py       # Executable utilities
```

**Rules:**
- Reference files must be **one level deep** from SKILL.md (no nested chains)
- Files >100 lines should include a table of contents
- Always use forward slashes in paths

## Step 4 — Write SKILL.md

### Required frontmatter

```yaml
---
name: <skill-name>
description: >
  What this skill does AND when to use it. Be specific. Include keywords
  for discoverability. Write in third person. Max 1024 chars.
---
```

### Optional frontmatter fields

| Field | Purpose | Example |
|---|---|---|
| `allowed-tools` | Pre-approved tools (space-delimited) | `Bash(python:*) Read Write` |
| `context` | Set to `fork` to run as subagent | `fork` |
| `agent` | Subagent type when forked | `Explore`, `Plan`, `general-purpose`, or custom |
| `disable-model-invocation` | `true` = manual `/name` only | `true` |
| `user-invocable` | `false` = background knowledge | `false` |
| `argument-hint` | Autocomplete hint | `[filename] [format]` |
| `metadata` | Arbitrary key-value pairs | `author: phalanx` |
| `compatibility` | Environment requirements | `Requires python 3.10+` |

### Body guidelines

- **Under 500 lines** — move detailed specs to `reference/` files
- Step-by-step instructions
- Examples of inputs and outputs
- Common edge cases
- Use consistent terminology throughout
- No time-sensitive information
- Progressive disclosure: link to reference files for details

### Skill types

| Type | Characteristics | `user-invocable` |
|---|---|---|
| **Workflow** | Multi-step orchestration, invokes tools and agents | `true` (default) |
| **Atomic** | Single-purpose instruction template | `true` (default) |
| **Protocol** | Background system behavior | `false` |
| **Meta** | Framework self-management | `true` |

## Step 5 — Validate

Run the validation script:

```bash
python .claude/skills/creating-skills/scripts/validate-skill.py .claude/skills/<skill-name>/
```

### Validation checks:
- [ ] `SKILL.md` exists in directory
- [ ] Frontmatter has `name` field
- [ ] Frontmatter has `description` field
- [ ] `name` matches directory name
- [ ] `name` passes format rules (kebab-case, 1-64 chars, no leading/trailing `-`)
- [ ] `description` is 1-1024 characters
- [ ] Body is under 500 lines
- [ ] Reference files are max 1 level deep
- [ ] No Windows-style paths (`\`)
- [ ] No XML tags in name or description

## Step 6 — Register in manifest

Add the new skill to `.claude/skills/manifest.md` in the appropriate section (Workflow, Atomic, Protocol, or Meta). Include:
- Skill name (matches directory)
- Description (from frontmatter)
- Tools referenced
- Agent used (if any)

## Step 7 — Cross-platform sync (optional)

If Copilot or Codex instruction files need updating:

```bash
python tools/platform/generate_instructions.py
```

---

## Quality Checklist

- [ ] Description is specific and includes key terms
- [ ] Description includes both WHAT and WHEN
- [ ] SKILL.md body under 500 lines
- [ ] Additional details in separate reference files if needed
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references one level deep
- [ ] Workflows have clear sequential steps
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful

---

## Anti-Patterns to Avoid

| Don't | Do Instead |
|---|---|
| Windows paths (`scripts\helper.py`) | Forward slashes (`scripts/helper.py`) |
| Multiple tool options ("use A, or B, or C...") | One default, mention alternatives for edge cases |
| Nested references (SKILL.md → ref.md → detail.md) | Keep references one level deep |
| Vague descriptions ("Helps with documents") | Specific: what + when |
| Magic numbers | Document why every constant has its value |
| Over-explaining what Claude already knows | Challenge each piece: does it justify its token cost? |
