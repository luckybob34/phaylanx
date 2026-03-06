---
name: improving-skills
description: >
  Handles error recovery, tool fixes, and skill updates when workflows fail
  or produce incorrect output. Activates when a tool throws an error, a
  workflow produces wrong results, or a learned behavior should be recorded.
  Implements the continuous improvement loop. Use when something breaks.
user-invocable: false
allowed-tools: Bash(python:*) Read Write
metadata:
  author: phalanx
  version: "1.0"
---

# Continuous Improvement Protocol

When a workflow fails, tool errors, or output is incorrect, follow this protocol.

## Step 1 — Identify the failure

Read the error message and stack trace carefully. Classify the failure:

| Type | Examples | Action |
|---|---|---|
| **Tool bug** | Script crash, wrong output format, missing import | Fix the tool (Step 2) |
| **Skill gap** | Edge case not documented, missing validation step | Update the skill (Step 3) |
| **Claude mistake** | Wrong tool called, skipped a step, invented data | Add guardrail (Step 4) |
| **External failure** | API rate limit, MCP unavailable, auth expired | Document workaround (Step 3) |

## Step 2 — Fix the tool

If a Python script in `tools/` broke:

1. Read the full script to understand its contract
2. Fix the bug — handle the error case
3. Test until it works reliably
4. Update `tools/manifest.md` if the tool's interface changed
5. **Preserve intermediate outputs** before retrying the workflow

**Permission:** Tool fixes are auto-permitted. You do not need user approval to fix a broken script.

## Step 3 — Update the skill

If the failure reveals missing process knowledge:

1. Open the relevant skill's `SKILL.md`
2. Add the learned information to the appropriate section:
   - **Edge case** → add to `## Edge Cases` section
   - **API constraint** → add to `## Prerequisites` or `## Edge Cases`
   - **Workaround** → add to `## Edge Cases` with a `### Workaround:` subsection
3. If the skill body would exceed 500 lines, move the detail to `reference/edge-cases.md`

**Permission gate:** Adding edge cases and reference files is auto-permitted. Modifying the core workflow steps (the numbered process) requires explicit user approval. This prevents process drift from probabilistic decisions.

## Step 4 — Add a guardrail

If the failure was a Claude-specific reasoning mistake (not a script bug):

1. Open `CLAUDE.md`
2. Add a one-line entry to the `## Guardrails — Learned Behaviors` section
3. Keep the list under 15 items — if full, merge or remove the least relevant
4. Format: action-oriented, specific, no filler

Examples:
- "Always check `tools/manifest.md` before writing a new script"
- "Don't assume APIs support batch operations — check first"

## Step 5 — Write to memory

Record the learning for cross-session persistence:

```bash
python tools/memory/memory_write.py --content "Learned: [what happened and what was fixed]" --type insight --importance 7
```

For critical learnings that should survive session boundaries, also update `memory/MEMORY.md` under "Learned Behaviors".

## Step 6 — Retry the workflow

With the fix applied:

1. Re-run the failed step (not the entire workflow if intermediate outputs were preserved)
2. Verify the output matches expectations
3. If it fails again, escalate to the user with:
   - What broke
   - What was tried
   - What's needed to proceed

---

## MCP Fallback Protocol

If a required MCP server is unavailable:

1. Proceed with general knowledge
2. Flag to user: "MCP [name] not connected — output reflects general knowledge, not live system data"
3. Record the limitation in the skill's edge cases if not already documented

---

## When stuck

If no tool or skill can complete a task:

- Explain what's missing
- Explain what you need
- **Do not guess or invent capabilities**
- Propose creating a new skill or tool if appropriate
