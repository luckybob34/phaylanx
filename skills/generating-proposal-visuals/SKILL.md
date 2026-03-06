---
name: generating-proposal-visuals
description: Generates professional proposal graphics including team org charts, project timelines, and methodology diagrams using structured prompt templates for image generation models. Used by the creating-visuals and responding-to-rfps skills.
allowed-tools: Terminal
---

# Proposal Visual Prompt Builder

Construct image generation prompts for professional proposal graphics — org charts, timelines, and methodology diagrams.

---

## Template: Team Organization Chart

```
Create a clean, professional organizational chart on a white background in a corporate flat-design style.

Structure:
- [TOP LEVEL]: [Role/Title] at the top center
- [SECOND LEVEL]: [Number] roles reporting directly, arranged horizontally below
- [THIRD LEVEL]: [Number] team members per group, arranged below their manager

Roles:
[For each person/role:]
- [TITLE] - shown as a [COLOR] rounded rectangle labeled "[TITLE]" with subtitle "[NAME or RESPONSIBILITY]"

Reporting Lines:
- Solid lines connect each role to its direct report
- Dashed lines show dotted-line relationships (advisory, cross-functional)

Visual Style:
- Color coding: [LEADERSHIP COLOR] for leadership, [TECHNICAL COLOR] for technical, [SUPPORT COLOR] for PMO
- Each box has subtle shadow and 8px rounded corners
- Text is dark gray (#333333) on light backgrounds
- Clean sans-serif font throughout

Title: "[CHART TITLE]" at the top in [COLOR]
Subtitle: "[SUBTITLE]" in smaller gray text

This organizational chart shows the proposed project team structure for [CONTEXT].
```

---

## Template: Project Timeline

```
Create a clean, professional horizontal project timeline infographic on a white background.

Layout: A horizontal timeline bar runs from left to right across the center.

Phases:
[For each phase:]
- [PHASE NAME]: spans from [START] to [END], shown as a [COLOR] rounded bar labeled "[PHASE NAME]"
  - Key milestones: [MILESTONE 1], [MILESTONE 2]

Milestones:
[For each milestone:]
- [MILESTONE NAME] - shown as a [COLOR] diamond at [POSITION], labeled above/below

Visual Style:
- Each phase is a different color: [COLOR 1], [COLOR 2], [COLOR 3], [COLOR 4]
- Milestone diamonds are [ACCENT COLOR]
- Month/quarter markers along the bottom
- Phase labels inside bars in white text; milestone labels outside in dark text
- Legend at bottom maps colors to phase names

Title: "[TIMELINE TITLE]" at the top in dark blue
Duration: "[DURATION]" subtitle

This timeline illustrates [CONTEXT].
```

---

## Template: Methodology Diagram

```
Create a clean, professional process flow diagram on a white background showing a [NUMBER]-step methodology.

Layout: [NUMBER] steps arranged [horizontally / circular / vertical cascade].

Steps:
[For each step:]
- Step [N]: "[STEP NAME]" - shown as a [COLOR] [shape] with number "[N]" and name below
  - Key activities: [ACTIVITY 1], [ACTIVITY 2], [ACTIVITY 3]

Flow:
- Curved arrows connect each step to the next
- [Optional: feedback arrow from last step to first labeled "Continuous Improvement"]

Visual Style:
- Steps use a gradient of [COLOR FAMILY] from light to dark
- Activity text in small bullets below each step
- Arrows are [COLOR] with slight curves
- Clean sans-serif font, dark text on light backgrounds
- Each step shape has a subtle drop shadow

Title: "[METHODOLOGY NAME]" at the top in [COLOR]
Subtitle: "[CONTEXT]"

This diagram illustrates [PURPOSE].
```

---

## Tips

- **Org charts**: 3-4 levels maximum. Color-code by role category.
- **Timelines**: 6-8 phases max. Highlight 3-5 key milestones.
- **Methodology diagrams**: 4-7 steps is the sweet spot.
- **All visuals**: Use muted, professional colors — no bright/neon tones.
- **Aspect ratios**: 16:9 for slides, 4:3 for document inserts.
- **Text caveat**: AI-generated text may be imperfect. Plan for post-processing on critical labels.

---

## Tool

```bash
python tools/media/generate_image.py \
  --prompt "<composed prompt>" \
  --output "workspace/<project-slug>/visuals/<name>.png" \
  --aspect-ratio 16:9
```
