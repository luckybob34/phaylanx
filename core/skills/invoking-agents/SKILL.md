---
name: invoking-agents
description: Invokes specialist agents for tasks requiring domain expertise. Handles loading agent role prompts, context files, MCP availability checks, and chaining multiple agents. Activates when a workflow skill specifies agent delegation or deep domain knowledge is needed.
user-invocable: false
allowed-tools: Terminal
---

# Agent Invocation Protocol

Specialist agents are pre-built AI roles with defined expertise, context, and linked resources. Use them when a task requires deep domain knowledge or when outputs will be reviewed by domain experts.

---

## When to Use a Specialist

Invoke a specialist agent when:

- The task requires domain expertise (cloud architecture, IaC, technical writing, research)
- The active skill specifies a specialist for a step
- Output quality matters and the audience has domain expertise

Do NOT use a specialist for:

- General tasks
- Framework maintenance
- Quick answers
- Simple lookups

---

## Available Agents

Always check `.claude/skills/manifest.md` — it shows which skills use which agents.

| Agent | Expertise |
|-------|-----------|
| `aws-architect` | AWS cloud architecture, Well-Architected, services |
| `azure-architect` | Azure architecture, Well-Architected, services |
| `iac-engineer` | Terraform, Bicep, IaC patterns |
| `devops-engineer` | CI/CD, pipelines, operational automation |
| `proposal-writer` | RFP responses, SOWs, consulting proposals |
| `technical-writer` | Documentation, editing, formatting |
| `researcher` | Market research, competitive analysis, data gathering |
| `creative-director` | Visual design, brand, image generation prompts |

---

## How to Invoke

1. **Check availability** — Read `.claude/agents/<name>/config.yaml` for required MCPs and context files
2. **Load role** — Read `.claude/agents/<name>/role.md` (the agent's system prompt)
3. **Load context** — Read any files listed under `config.yaml → context.files`
4. **Check MCPs** — If required MCPs are listed, verify they're available
5. **Construct prompt:**

```
[Full contents of role.md]

---

[Loaded context file contents, if any]

---

Your task: [specific instruction]

Context: [relevant project info, existing files, etc.]
```

6. **Launch** as a sub-agent with this prompt

---

## MCP Fallback

If a required MCP is unavailable:

- Proceed with general knowledge
- Flag to user: "MCP [name] not connected — output reflects general knowledge, not live system data"

---

## Chaining Agents

When multiple specialists work on the same task:

1. Save the output of the first agent to `workspace/<project-slug>/notes/`
2. Pass that output as context to the next agent
3. Document the chain in the session log

Example chain: `aws-architect` → `iac-engineer` → `devops-engineer`

---

## Edge Cases

- **Agent role.md missing** — Flag the gap, proceed with general knowledge, note limitation
- **Multiple cloud platforms** — Invoke both `aws-architect` and `azure-architect`, document integration points
- **Conflicting agent recommendations** — Present both perspectives to the user with pros/cons
