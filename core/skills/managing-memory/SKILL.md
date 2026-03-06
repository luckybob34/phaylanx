---
name: managing-memory
description: Manages persistent memory across sessions. Reads MEMORY.md and daily logs at session start, writes events and facts during sessions, and searches memory for relevant context. Activates automatically at session start and when preserving insights.
user-invocable: false
allowed-tools: Terminal
---

# Memory Protocol

The system has persistent memory across sessions using a dual-write architecture: SQLite database for structured search + markdown files for human readability.

---

## Session Start — Load Memory

Run these steps at the beginning of every session:

1. Read `memory/MEMORY.md` for curated facts and preferences
2. Read today's log: `memory/logs/YYYY-MM-DD.md`
3. Read yesterday's log for continuity
4. Optionally load from database:

```bash
python tools/memory/memory_read.py --format markdown
```

---

## During Session — Write Memory

### Log Events

Append notable events to today's log:

```bash
python tools/memory/memory_write.py --content "description of event" --type event
```

### Store Facts

Add facts to the database with importance weighting (1-10):

```bash
python tools/memory/memory_write.py --content "fact content" --type fact --importance 7
```

### Update Persistent Memory

For truly persistent facts that should always load at session start, write to MEMORY.md:

```bash
python tools/memory/memory_write.py --update-memory --content "New preference or fact" --section user_preferences
```

---

## Search Memory

| Method | Command | Best For |
|--------|---------|----------|
| Keyword | `python tools/memory/memory_db.py --action search --query "keyword"` | Exact matches |
| Semantic | `python tools/memory/semantic_search.py --query "related concept"` | Conceptual similarity |
| Hybrid | `python tools/memory/hybrid_search.py --query "what does user prefer"` | Best overall recall |

---

## Memory Types

| Type | Purpose | Example |
|------|---------|---------|
| `fact` | Objective information | "User prefers Terraform over Bicep" |
| `preference` | User preferences | "Always use dark theme for presentations" |
| `event` | Something that happened | "Delivered SOW for client X" |
| `insight` | Learned pattern | "RFP parser misses appendix requirements" |
| `task` | Something to do | "Follow up on architecture review" |
| `relationship` | Connection between entities | "Project X feeds into Project Y" |

---

## Memory Tools

| Tool | Purpose |
|------|---------|
| `tools/memory/memory_read.py` | Read memory entries |
| `tools/memory/memory_write.py` | Write entries, update MEMORY.md |
| `tools/memory/memory_db.py` | Direct database operations |
| `tools/memory/semantic_search.py` | Embedding-based search |
| `tools/memory/hybrid_search.py` | Combined keyword + semantic search |
| `tools/memory/embed_memory.py` | Generate embeddings for entries |

---

## When to Write Memory

- Project starts/completes → `event` with importance 6-7
- User states a preference → `preference` with importance 8
- A tool failure teaches something → `insight` with importance 7
- A new guardrail is discovered → add to CLAUDE.md guardrails AND write as `insight`
