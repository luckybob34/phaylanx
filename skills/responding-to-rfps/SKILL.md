---
name: responding-to-rfps
description: Produces complete, compliant, and competitive RFP responses using the PARSE workflow — parse requirements, analyze go/no-go, draft sections, build compliance matrix, and edit for final delivery. Invokes the proposal-writer agent for drafting and researcher agent for competitive intelligence.
allowed-tools: Terminal
agent: proposal-writer researcher
---

# RFP Response — PARSE Workflow

Produce a complete, compliant, and competitive RFP response.

| Step | Phase | What You Do |
|------|-------|-------------|
| **P** | Parse | Extract requirements, criteria, deadlines |
| **A** | Analyze | Score go/no-go, identify strengths/gaps |
| **R** | Respond | Draft section-by-section mapped to evaluation criteria |
| **S** | Structure | Build compliance matrix, assemble package |
| **E** | Edit | Final review, compliance check, polish |

---

## P — Parse

1. Place RFP source in `workspace/<project-slug>/rfp/source/`
2. Run parser:

```bash
python tools/proposals/parse_rfp.py \
  --input workspace/<project-slug>/rfp/source/<filename>.md \
  --output workspace/<project-slug>/rfp/parsed_rfp.json
```

3. Generate markdown summary:

```bash
python tools/proposals/parse_rfp.py \
  --input workspace/<project-slug>/rfp/source/<filename>.md \
  --output workspace/<project-slug>/rfp/parsed_rfp.md --format markdown
```

---

## A — Analyze

Score each factor 1-5 (minimum 3.0 average to proceed):

| Factor | Question |
|--------|----------|
| Capability match | Can we deliver >80% of requirements? |
| Past performance | Relevant case studies? |
| Resource availability | Have the team to deliver? |
| Strategic fit | Aligns with growth areas? |
| Win probability | Competitive against likely bidders? |
| Profitability | Price competitively and profit? |

Classify each mandatory requirement: **Strong** / **Adequate** / **Gap** / **Disqualifier**.

Save to `workspace/<project-slug>/rfp/analysis.md`.

---

## R — Respond

### Drafting Rules

1. Lead with evaluator's language — mirror RFP terminology
2. Answer the question first — don't bury in preamble
3. Prove every claim — reference case studies, certifications, metrics
4. Quantify — "reduced costs by 40%" beats "reduced costs"
5. Address gaps honestly — propose mitigation
6. Match section numbering to the RFP
7. Follow `context/style-guide.md` for voice and tone

### Agent Delegation

- **proposal-writer** — drafting
- **researcher** — competitive intelligence
- **aws-architect** / **azure-architect** — technical sections

### Template

Use `reference/rfp-response-template.md` (this skill) for section structure.

Save drafts to `workspace/<project-slug>/rfp/response/sections/`.

---

## S — Structure

### Build Compliance Matrix

```bash
python tools/proposals/build_compliance_matrix.py \
  --requirements workspace/<project-slug>/rfp/parsed_rfp.json \
  --capabilities workspace/<project-slug>/rfp/capabilities.json \
  --output workspace/<project-slug>/rfp/compliance_matrix.md \
  --format markdown
```

### Assemble Response Package

1. Cover letter
2. Executive summary
3. Technical approach
4. Management approach
5. Past performance / case studies
6. Staffing plan
7. Compliance matrix
8. Cost proposal (separate volume if required)
9. Appendices

Save to `workspace/<project-slug>/rfp/response/final/`.

---

## E — Edit

### Checklist

- [ ] Every mandatory requirement has a compliant response
- [ ] Section numbering matches RFP
- [ ] All evaluation criteria weighted appropriately
- [ ] No placeholder text (TBD, TODO, [PLACEHOLDER])
- [ ] Consistent voice and formatting
- [ ] Page/word counts within limits
- [ ] Pricing internally consistent
- [ ] All attachments referenced correctly

Invoke **technical-writer** for final polish.

---

## Edge Cases

- **Ambiguous requirements** — Flag, interpret conservatively, document interpretation
- **Short turnaround** — Skip deep competitive analysis, focus on compliance first
- **Mandatory requirement we can't meet** — Evaluate subcontractor or phased approach
- **Amendment issued** — Re-run parser on updated document, diff against original

---

## Workspace Structure

```
workspace/<project-slug>/
├── rfp/
│   ├── source/
│   ├── parsed_rfp.json
│   ├── parsed_rfp.md
│   ├── analysis.md
│   ├── capabilities.json
│   ├── compliance_matrix.md
│   └── response/
│       ├── sections/
│       └── final/
```
