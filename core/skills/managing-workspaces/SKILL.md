---
name: managing-workspaces
description: Creates and manages project workspace directories for deliverables. Activates when starting any task that produces files, spans multiple sessions, or the user names as a project. Ensures outputs are permanently stored, never in .tmp/.
user-invocable: false
---

# Workspace Protocol

Every project task gets its own named workspace folder. All project outputs live here permanently — never in `.tmp/`.

---

## When to Create a Workspace

Create a workspace at the start of any task that:

- Will produce files, documents, code, data, or other artifacts
- Spans more than one session
- The user refers to as a "project," "build," "engagement," or names it explicitly

Do NOT create a workspace for:

- One-off questions
- Memory operations
- Tool fixes
- Framework maintenance tasks

---

## Naming Convention

Use a slugified version of the project name: lowercase, hyphens instead of spaces, no special characters.

| User Says | Slug |
|-----------|------|
| "My CRM App" | `my-crm-app` |
| "Q2 RFP Response" | `q2-rfp-response` |
| "Market Research - APAC" | `market-research-apac` |

If the user hasn't named the project, ask before creating the folder. If they don't care, use `project-YYYY-MM-DD`.

---

## Creating a Workspace

1. Check if `workspace/<project-slug>/` already exists:

```bash
ls workspace/
```

2. If it exists, review contents and resume from where work left off. Do not recreate existing files.

3. If new, create the top-level folder. The active skill defines the internal structure:

```bash
mkdir -p workspace/<project-slug>
```

4. Record in memory:

```bash
python tools/memory/memory_write.py --content "Project: <project-slug> - workspace/<project-slug>/ - <one-line description>" --type fact --importance 7
```

5. Update `memory/MEMORY.md` under "Current Projects" with the workspace path.

---

## Internal Structure

Each workflow skill defines its own subfolder structure. Common patterns:

| Skill | Subfolders |
|-------|------------|
| `building-apps` | `brief/`, `design/`, `src/`, `tests/`, `notes/` |
| `responding-to-rfps` | `rfp/source/`, `rfp/response/sections/`, `rfp/response/final/` |
| `building-sow` | `sow/` |
| `designing-architecture` | `architecture/`, `architecture/adrs/` |
| `building-html-decks` | `presentations/`, `notes/` |
| `building-pptx-decks` | `presentations/`, `notes/` |
| `creating-visuals` | `visuals/` |
| `planning-cloud-migration` | `migration/`, `migration/runbooks/`, `migration/target_architectures/` |
| `deploying-infrastructure` | `infrastructure/modules/`, `infrastructure/environments/` |
| `reviewing-architecture` | `review/` |

---

## Rules

- **Deliverables** → `workspace/<project-slug>/` (permanent)
- **Scratch work** → `.tmp/` (disposable)
- **Framework files** → their designated layer directories, never in `workspace/`
- If the user asks for outputs at a custom location, save a copy there AND to the workspace
