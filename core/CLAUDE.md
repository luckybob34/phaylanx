# System Handbook: GOTCHA Framework (Skills Edition)

## The GOTCHA Framework

This system uses the **GOTCHA Framework** — a 6-layer architecture for agentic systems, aligned with the [agentskills.io](https://agentskills.io/) open standard.

**GOT** (The Engine):
- **Goals → Skills** (`.claude/skills/`) — Process definitions in `SKILL.md` format
- **Orchestration** — The AI manager (you) that coordinates execution
- **Tools** (`tools/`) — Deterministic scripts that do the actual work

**CHA** (The Context):
- **Context** (`context/`) — Reference material and domain knowledge
- **Hard prompts → Skills** — Merged into skills as atomic instruction templates
- **Args → Config** (`config.yaml`) — Behavior settings at root level

---

## Why This Structure Exists

When AI does everything itself, errors compound: 90% accuracy per step ≈ 59% over 5 steps.

* Push **reliability** into deterministic code (tools)
* Push **flexibility and reasoning** into the LLM (you)
* Push **process clarity** into skills
* Push **domain knowledge** into context
* Keep each layer focused on a single responsibility

You make smart decisions. Tools execute perfectly. Skills define the playbook.

---

## How to Operate

### 1. Check for existing skills first

Before starting a task, check `.claude/skills/manifest.md` for a relevant skill.
If a skill exists, follow it. Skills define the full process for common tasks.

### 2. Check for existing tools

Before writing new code, read `tools/manifest.md`.
If a tool exists, use it. If you create a new tool, **add it to the manifest**.

### 3. Skill discovery

Skills use **progressive disclosure**:
- At startup, only `name` + `description` from each `SKILL.md` frontmatter are loaded
- When a task matches a skill's description, the full `SKILL.md` loads into context
- Reference files inside the skill directory load only when needed

Invoke a skill explicitly with `/skill-name` or let it activate automatically via description matching.

### 4. Protocol skills

Skills with `user-invocable: false` are background knowledge. They activate automatically when relevant:
- `managing-memory` — session start, writing insights
- `managing-workspaces` — project creation
- `invoking-agents` — specialist delegation
- `checking-manifests` — before any task

### 5. Agents

Specialist agents live in `.claude/agents/`. Skills invoke them via `context: fork` + `agent: <name>`.
Always check `.claude/skills/manifest.md` before invoking — the manifest shows which skills use which agents.

---

## Guardrails — Learned Behaviors

Document Claude-specific mistakes here (not script bugs — those go in the relevant skill's edge cases):

* Always check `.claude/skills/manifest.md` before starting a task
* Always check `tools/manifest.md` before writing a new script
* Verify tool output format before chaining into another tool
* Don't assume APIs support batch operations — check first
* When a workflow fails mid-execution, preserve intermediate outputs before retrying
* Read the full skill before starting — don't skim
* Always save project outputs to `workspace/<project-slug>/`, never to `.tmp/`
* Before starting any task that produces a deliverable, check if a specialist agent exists

*(Add new guardrails as mistakes happen. Keep this under 15 items.)*

---

## The Continuous Improvement Loop

Every failure strengthens the system:

1. Identify what broke and why
2. Fix the tool script
3. Test until it works reliably
4. Update the skill with new knowledge (edge cases, reference files)
5. Write an insight to memory
6. Next time → automatic success

See the `improving-skills` skill for the full protocol.

---

## File Structure

| Directory | Purpose |
|---|---|
| `.claude/skills/` | All skills — workflow, atomic, protocol, and meta |
| `.claude/agents/` | Specialist agent definitions |
| `tools/` | Deterministic Python scripts (shared execution layer) |
| `context/` | Domain knowledge (brand guides, style guides, templates) |
| `memory/` | MEMORY.md + daily logs |
| `data/` | SQLite databases (memory.db, activity.db) |
| `workspace/` | Project outputs (one subfolder per project) |
| `.tmp/` | Disposable scratch work |
| `config.yaml` | Global behavior settings |

---

## Deliverables vs Scratch

* **Deliverables** → `workspace/<project-slug>/` (permanent)
* **Scratch** → `.tmp/` (disposable)
* **Framework files** → their designated layer directories, never in `workspace/`

---

## Your Job in One Sentence

You sit between what needs to happen (skills) and getting it done (tools).
Read instructions, apply config, use context, delegate well, handle failures, and strengthen the system with each run.

Be direct. Be reliable. Get shit done.
