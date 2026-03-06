---
name: checking-manifests
description: Checks skills and tools manifests before starting any task. Ensures existing skills are used rather than reinvented and existing tools are called rather than rewritten. Activates automatically before every task.
user-invocable: false
---

# Manifest Check Protocol

Before starting any task, check both manifests to avoid reinventing the wheel.

---

## Step 1 — Check Skills Manifest

Read `.claude/skills/manifest.md` and scan for a skill that matches the current task.

- If a matching skill exists → activate it and follow its workflow
- If no match → proceed with general reasoning, consider creating a new skill afterward

---

## Step 2 — Check Tools Manifest

Read `tools/manifest.md` and scan for tools relevant to the current task.

- If a tool exists → use it, don't rewrite it
- If you create a new tool → **add it to `tools/manifest.md`** with a one-sentence description

---

## When This Activates

This protocol runs automatically before:

- Starting any user request
- Delegating to a sub-agent
- Running any workflow skill's first step

---

## Rules

1. Never skip manifest checks — even for tasks that seem novel
2. If a skill exists but is outdated, use it and then update it (see `improving-skills`)
3. If a tool exists but its interface changed, fix the tool and update the manifest
4. The manifests are the system's index — keep them accurate
