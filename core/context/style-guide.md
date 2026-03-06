---
title: Phalanx Technical Writing Style Guide
version: 1.0
status: Approved
date: 2026-03-01
owner: Technical Writer Agent
---

# Phalanx Technical Writing Style Guide

This guide defines the writing standards for all technical content produced by the Phalanx framework - consulting deliverables, internal documentation, architecture docs, proposals, and any other written output.

---

## 1. Voice & Tone

### Default Voice
- **Direct and confident** - State what is, not what might be. "This architecture uses multi-AZ deployment" not "It is recommended that multi-AZ deployment be considered."
- **Expert but accessible** - Write like an experienced consultant briefing a smart colleague. No condescension, no jargon for jargon's sake.
- **Action-oriented** - Every paragraph should move the reader toward a decision or action.

### Tone Adjustments by Audience

| Audience | Tone | Characteristics |
|----------|------|-----------------|
| **C-suite / Executives** | Strategic, concise | Lead with impact and outcomes. Numbers over adjectives. No implementation details. |
| **Technical leadership** | Authoritative, structured | Architecture decisions with rationale. Trade-offs stated explicitly. |
| **Engineers / Operators** | Precise, practical | Step-by-step specifics. Exact commands, config snippets, endpoint URLs. Nothing ambiguous. |
| **Evaluators / Auditors** | Formal, evidence-based | Compliance language. Cross-references. Traceability to requirements. |
| **Mixed / Unknown** | Professional, layered | Executive summary up top, technical detail below. Let readers self-select depth. |

### Words to Avoid

| Instead of... | Write... |
|---------------|----------|
| "It is important to note that..." | *(just state the thing)* |
| "In order to..." | "To..." |
| "Leverage" | "Use" |
| "Utilize" | "Use" |
| "At this point in time" | "Now" |
| "Going forward" | *(delete it - it's almost always filler)* |
| "Best-in-class" | *(be specific: what makes it good?)* |
| "Synergy" | *(describe the actual interaction)* |
| "Robust" | *(describe what makes it resilient)* |
| "Seamless" | *(describe the actual integration mechanism)* |

---

## 2. Structure & Formatting

### Document Hierarchy
Every document follows this principle: **the reader should be able to stop at any level and have gotten value.**

1. **Title** - What this document is
2. **Metadata block** - Author, date, version, status
3. **Executive summary** - 2-4 sentences; the entire document compressed
4. **Body** - Sections with clear headers, progressing from overview → detail
5. **Appendices** - Supporting data, raw tables, detailed configs (optional)

### Metadata Block
All documents include a YAML frontmatter block:

```yaml
---
title: [Document Title]
version: 1.0
status: Draft | Review | Approved
date: YYYY-MM-DD
owner: [Name or Team]
---
```

### Formatting Rules

- **Markdown by default** - All output in GitHub-flavored Markdown unless specified otherwise
- **Headers** - Use `##` as the top working level in documents (reserve `#` for the document title). Never skip levels (`##` → `####`)
- **Paragraphs** - 3 sentences max. If a paragraph exceeds 4 sentences, break it up or convert to a list
- **Lists** - Use bullets for unordered items, numbers only when sequence matters. No list longer than 7 items without subgrouping
- **Tables** - Use for any comparison, matrix, or structured data. Tables > paragraphs for anything with 2+ dimensions
- **Bold** - Use for key terms on first introduction and for emphasis in lists. Don't bold entire sentences
- **Inline code** - Use backticks for: commands, file paths, variable names, config keys, service names (`ec2`, `terraform plan`, `/etc/nginx/`)
- **Code blocks** - Use fenced blocks with language tags for anything over one line. Always specify the language (```yaml, ```bash, ```hcl)
- **Links** - Descriptive text, never "click here" or bare URLs in prose

### Section Naming
Use descriptive, noun-based headers. The reader should know what's in a section without reading it.

| Good | Bad |
|------|-----|
| "Authentication Architecture" | "Auth" |
| "Cost Estimate - Monthly Breakdown" | "Costs" |
| "Migration Risk Assessment" | "Risks and Other Things" |
| "Deployment Prerequisites" | "Before You Begin" *(acceptable for runbooks)* |

---

## 3. Technical Writing Rules

### Precision
- **Name everything** - "The ALB forwards traffic to the EC2 Auto Scaling group" not "The load balancer sends requests to the servers"
- **Quantify** - "Reduces deployment time from 45 minutes to 8 minutes" not "Significantly reduces deployment time"
- **Version-pin** - "Terraform 1.7+" not "a recent version of Terraform". "Python 3.10+" not "Python 3"
- **Specify scope** - "This applies to production workloads in us-east-1" not "This applies to most environments"

### Clarity
- **One idea per sentence** - If a sentence has "and" connecting two independent clauses, split it
- **Active voice** - "The pipeline deploys the container" not "The container is deployed by the pipeline". Passive voice is acceptable in process descriptions where the actor is irrelevant
- **Subject-verb proximity** - Keep the subject and verb close. Don't bury the verb behind clauses
- **Define acronyms on first use** - "Virtual Private Cloud (VPC)" on first mention, then "VPC" thereafter. Per document, not per section

### Consistency
- **Terminology** - Pick one term and stick with it. Don't alternate between "server," "instance," "host," and "node" for the same thing
- **Capitalization** - Service names match official casing: "Amazon EC2" not "amazon ec2" or "EC2 instances" not "Ec2 Instances"
- **Oxford comma** - Always. "VPCs, subnets, and security groups"
- **Date format** - YYYY-MM-DD in technical docs. Spell out month in executive docs ("February 28, 2026")
- **Number formatting** - Spell out one through nine; use numerals for 10+. Always use numerals with units ("3 GB", "5 instances")

---

## 4. Document Types

### Architecture Documents
- Lead with a component diagram (text-described or image reference)
- Include an Architecture Decision Record (ADR) section for each non-obvious choice
- State constraints before presenting the design
- End with costs, risks, or next steps

### Proposals & SOWs
- Mirror the RFP's language and structure - evaluators score against their rubric, not ours
- Lead each section with the compliance answer, then expand with approach
- Include a compliance matrix mapping every requirement to a response section
- Quantify experience: "Migrated 340+ workloads across 12 engagements" not "extensive migration experience"

### SOPs & Runbooks
- Start with: who, when, why, prerequisites
- Number every step (sequence matters)
- Include expected output for each step so the operator knows it worked
- End with: rollback procedure, escalation contacts, verification checklist

### Executive Summaries
- Maximum one page
- Structure: Situation → Recommendation → Key Evidence → Next Steps
- No technical jargon - translate to business impact
- Include one summary table or data point that tells the story at a glance

---

## 5. Visual & Diagram Conventions

### Architecture Diagrams (text-described)
When describing diagrams in text or prompting image generation:
- **Flow direction** - Left-to-right for data flow, top-to-bottom for hierarchy
- **Label everything** - Every box, arrow, and connection gets a name
- **Group by boundary** - VPC, subnet, security zone, region
- **Color semantics** - Use consistently: blue for compute, green for networking, orange for storage, red for security alerts

### Tables
- Always include a header row
- Align numbers right, text left
- Keep cell content under 20 words; link to detail sections for complex entries
- Use "-" for empty cells, not blank

### Code Samples
- Keep samples minimal - show only what's relevant to the point being made
- Add inline comments for non-obvious lines
- Use realistic values, not `foo`, `bar`, `test123` - show actual service names, realistic IPs, real config keys

### Presentation Visuals

Slide decks must use a variety of visual patterns. Match the visual shape to the content shape:

| Content Shape | Recommended Pattern | Avoid |
|---|---|---|
| Sequential steps (3-5) | `step-flow`, `funnel`, `ascend-timeline` | `card-grid` with numbered cards |
| Layered architecture | `layer-stack`, `annotated-stack` | `two-col` with bullet lists |
| Central coordinator + satellites | `hub-spoke` | `card-grid` wrapped around a heading |
| Transformation / improvement | `before-after` | `two-col` with "Before" and "After" headers |
| Continuous cycle | `process-loop` | `highlight-grid` with numbered boxes |
| Key metrics (compact) | `metric-strip` | `stat-grid` when space is tight |
| Key metrics (featured) | `stat-grid` | Only when 3-4 stats deserve full emphasis |

**Variety rule:** No more than 2 consecutive slides may use the same component category (box grids, flows, structure, comparison, process). Plan the component sequence during outlining.

### Brand Themes

Available brand themes for presentations. Each theme has CSS (for HTML decks) and may have a PPTX theme (for PowerPoint decks).

| Brand | HTML Theme | PPTX Theme | Brand Guide |
|---|---|---|---|
| **Minimal** | `themes/minimal.css` | — | Brand-agnostic default |
| **Credera** | `themes/credera.css` + `themes/credera-components.md` | `themes/pptx/credera/` | — |
| **Quanta** | `themes/quanta.css` + `themes/quanta-components.md` | — | `context/quanta-brand.md` |

All theme paths are relative to `context/templates/presentations/`. See `themes/_contract.md` for the CSS theme contract and `hardprompts/presentations/deck-skill.md` for the HTML deck builder skill.

---

## 6. Review Checklist

Before any document is considered complete, verify:

- [ ] **Audience** - Is the tone and depth appropriate for the stated audience?
- [ ] **Structure** - Can the reader get value by reading only the headers and first sentence of each section?
- [ ] **Scannable** - No paragraph longer than 4 sentences? Lists and tables used where appropriate?
- [ ] **Precise** - Are services, versions, and quantities named specifically?
- [ ] **Consistent** - Same terms, same capitalization, same formatting throughout?
- [ ] **Metadata** - Title, version, status, date, owner present?
- [ ] **Actionable** - Does the reader know what to do next after reading?
- [ ] **No filler** - Could any sentence be deleted without losing meaning?

---

## 7. Templates

### Standard Document Template

```markdown
---
title: [Title]
version: 1.0
status: Draft
date: YYYY-MM-DD
owner: [Owner]
---

# [Title]

## Executive Summary

[2-4 sentences: what this is, what it recommends, why it matters]

## [Section 1]

### [Subsection]

## [Section 2]

## Next Steps

1. [Action item with owner and date]
2. [Action item with owner and date]

---

*Document version history maintained via Git commits.*
```

### ADR Template

```markdown
# ADR-[NNN]: [Decision Title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Deciders:** [Names/roles]

## Context

[What is the problem or situation requiring a decision?]

## Decision

[What was decided and why?]

## Alternatives Considered

| Option | Pros | Cons |
|--------|------|------|
| [A] | ... | ... |
| [B] | ... | ... |

## Consequences

- [What changes as a result of this decision]
- [What risks does this introduce]
- [What does this enable]
```

---

*This is a living document. Update as patterns emerge and standards evolve.*
