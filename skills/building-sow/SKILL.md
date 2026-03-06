---
name: building-sow
description: Produces professional Statements of Work for consulting engagements using the SCOPE workflow — gather context, define scope and deliverables, add business terms, review quality, and finalize for signature. Invokes the proposal-writer agent for content quality.
allowed-tools: Terminal
agent: proposal-writer
---

# SOW Builder — SCOPE Workflow

Produce professional Statements of Work for consulting engagements.

| Step | Phase | What You Do |
|------|-------|-------------|
| **S** | Situate | Gather engagement context, needs, constraints |
| **C** | Craft | Define scope, deliverables, timeline, staffing |
| **O** | Operationalize | Add pricing, risks, change management, acceptance |
| **P** | Polish | Generate document, review quality |
| **E** | Execute | Finalize for signature |

---

## S — Situate

Answer these questions:

1. **Client's problem?** — One paragraph max
2. **What have they tried?** — Current state and why it's insufficient
3. **What does success look like?** — Business outcome, not technical deliverable
4. **Constraints?** — Budget, timeline, compliance, tech stack
5. **Stakeholders?** — Decision maker, technical contact, end users
6. **From an RFP?** — Cross-reference `responding-to-rfps` outputs

Save to `workspace/<project-slug>/sow/engagement_brief.md`.

---

## C — Craft

### Scope Definition

1. **Explicit in-scope items** — every deliverable and activity
2. **Explicit out-of-scope items** — protect from scope creep
3. **Assumptions** — what must be true for this scope to hold

### Deliverables Table

Each deliverable needs: **ID** (D1, D2...), **Name**, **Description**, **Acceptance criteria**, **Due date**.

### Timeline

Map milestones to deliverables (M1 → D1, M2 → D2, etc.).

### Generate Scaffold

```bash
python tools/proposals/generate_sow.py --scaffold --output workspace/<project-slug>/sow/sow_data.json
```

---

## O — Operationalize

### Pricing

Choose model: **Fixed-price** / **T&M** / **Hybrid**. Include cost breakdown, payment schedule, expense policy.

### Risks

Minimum: scope risks, resource risks, technical risks, timeline risks. Each needs: probability, impact, mitigation.

### Change Management

> Change requests submitted in writing, approved by both parties before work. Each includes impact assessment for scope, timeline, cost.

### Acceptance

Define: review period (5 business days), what constitutes acceptance, dispute resolution.

Update `workspace/<project-slug>/sow/sow_data.json`.

---

## P — Polish

### Generate

```bash
python tools/proposals/generate_sow.py \
  --input workspace/<project-slug>/sow/sow_data.json \
  --output workspace/<project-slug>/sow/sow_draft.md \
  --format markdown
```

### Checklist

- [ ] Writing conforms to `context/style-guide.md`
- [ ] All sections populated — no blanks or TBDs
- [ ] Deliverables tie to milestones
- [ ] Pricing ties to scope
- [ ] In/out-of-scope clearly delineated
- [ ] Risk mitigations are actionable
- [ ] Acceptance criteria measurable

Agents: **proposal-writer** for strategic framing, **technical-writer** for polish.

---

## E — Execute

1. Get internal review approval
2. Convert to client-ready format (PDF if needed)
3. Save: `workspace/<project-slug>/sow/sow_final.md`
4. Record: `python tools/memory/memory_write.py --content "SOW delivered: <project-slug>" --type event --importance 6`

---

## SOW Size Guidelines

| Size | Length | Emphasis |
|------|--------|----------|
| <$25K | 3-5 pages | Scope, deliverables, pricing |
| $25K-$150K | 5-10 pages | All sections |
| >$150K | 10-20 pages | + detailed risk register, staffing |
| Enterprise | 15-30+ pages | + SLAs, governance, escalation |

---

## Edge Cases

- **SOW from RFP** — Use parsed requirements as scope input
- **Amendment** — Version the output (v1.1, v2.0), modify specific sections
- **Multiple streams** — Separate SOWs when pricing models differ
- **Rate card** — T&M with NTE clause
- **Very small** — Skip risk register and change management

---

## Workspace Structure

```
workspace/<project-slug>/
└── sow/
    ├── engagement_brief.md
    ├── sow_data.json
    ├── sow_draft.md
    └── sow_final.md
```
