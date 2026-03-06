---
name: building-university-decks
description: Builds comprehensive HTML slide deck presentations about university degree programs using the Phalanx slide engine with the Minimal theme. Covers degree plans, tuition breakdowns, financial aid, housing, and campus context with a structured research phase followed by a 14-slide deck.
allowed-tools: Terminal
---

# University Degree Deck Builder

Build a comprehensive slide deck about a university degree program. Research first, then build.

---

## Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{{UNIVERSITY}}` | Full university name | University of Texas at Dallas |
| `{{UNIVERSITY_SHORT}}` | Abbreviated name | UT Dallas |
| `{{DEGREE}}` | Degree name and level | BS in Computer Science |
| `{{MINOR}}` | Minor or concentration | Cyber Security |
| `{{SEMESTER}}` | Target start semester | Fall 2026 |
| `{{RESIDENCY}}` | In-state or out-of-state | Texas resident |

---

## Research Phase

Before building, gather from official university sources:

1. **Degree Plan** — Total hours, core curriculum, major courses, electives, accreditation (ABET)
2. **Minor Overlay** — Hours, required courses, overlap with major, net additional hours
3. **Tuition & Costs** — Annual tuition (residency rate), per-credit cost, room/board, meal plans, 4-year projection
4. **Financial Aid** — % receiving aid, average grant, net price, tuition lock programs
5. **Housing & Living** — First-year options, upperclassman options, included amenities, off-campus estimates
6. **Campus Context** — Population, size, program ranking, key employers, co-op proximity

---

## Output Phase

### 1. Degree Outline

Create `workspace/<project-slug>/degree-outline.md`:
- 4-year semester-by-semester course map
- Credit hour breakdown by category
- Minor overlap analysis table
- Math prerequisite chain
- Key dates and deadlines

### 2. Slide Deck

Create `workspace/<project-slug>/presentation.html` using the Phalanx slide engine:

1. Read `context/templates/presentations/base-template.html`
2. Use **Minimal theme** — inline CSS from `context/templates/presentations/themes/minimal.css`
3. Follow the `building-html-decks` skill rules

### Slide Structure (14 slides)

| # | Title | Type | Content |
|---|-------|------|---------|
| 0 | Title | `.slide-dark` | University, degree + minor, semester |
| 1 | Why {{UNIVERSITY_SHORT}}? | `.slide-light` | Card grid: selling points |
| 2 | Academics | `.slide-accent` | Section break |
| 3 | Degree Overview | `.slide-light` | Stat grid + pillar grid |
| 4 | 4-Year Course Map | `.slide-gray` | Two-col: Y1-2 / Y3-4 |
| 5 | Minor Overlay | `.slide-light` | Highlight boxes, overlap tags |
| 6 | Costs & Finances | `.slide-accent` | Section break |
| 7 | Tuition Breakdown | `.slide-light` | Data table, 4-year callout |
| 8 | Financial Aid | `.slide-gray` | Stat grid, key programs |
| 9 | Campus Life | `.slide-accent` | Section break |
| 10 | Housing | `.slide-light` | Card grid with costs |
| 11 | Meal Plans | `.slide-gray` | Data table |
| 12 | Off-Campus | `.slide-light` | Two-col: rent / transport |
| 13 | Next Steps | `.slide-dark` | Timeline: milestones |

---

## Rules

- Do not invent data — use only researched figures
- All costs reflect residency rate
- Inline all CSS — no external stylesheet references
- Use Minimal theme's slate/blue palette
- Follow all Phalanx engine rules (sequential data-index, first slide `.visible`, nav matches slides)

---

## Engine References

| File | Purpose |
|------|---------|
| `context/templates/presentations/base-template.html` | HTML + JS engine |
| `context/templates/presentations/themes/minimal.css` | Theme CSS |
| `context/templates/presentations/themes/_contract.md` | CSS contract |
