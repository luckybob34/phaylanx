# Credera PPTX Components

> Reference for available component renderers in the Credera PPTX theme.
> Maps to `config.yaml` component settings.

---

## Template Layouts (Native)

These layouts use the Credera PPTX template's built-in design:

| Outline Key | Template Layout | Notes |
|-------------|----------------|-------|
| `title` | Title Slide [3] | Large title + subtitle on branded background |
| `section` | Gradient [8] or Photo [7] Section Break | Set `style: gradient` or `style: photo` |
| `stat` | Impressive Stat [17] | Big number + subtitle on colour block |
| `quote` | Quote [23] | Quote text + author attribution |
| `end` | End Splash [33] | "Unlock Extraordinary" branded close |

## Programmatic Components (Drawn)

These are rendered programmatically on a blank layout:

### Data Components
- **stat-grid** — 3-6 metric cards in columns
- **card-grid** — Auto-fit content cards (2-4 columns)
- **data-table** — Styled table with header row
- **highlight-grid** — Feature/pillar cards with icons

### Flow Components
- **step-flow** — Horizontal numbered step nodes with arrows
- **funnel** — Decaying bars showing filtering/conversion
- **timeline** — Horizontal timeline with dot status indicators
- **ascend** — Ascending columns showing growth/phases

### Structure Components
- **layer-stack** — Tiered architecture rows
- **hub-spoke** — Centre node with radial satellites

### Process Components
- **process-loop** — Circular cycle diagram with centre label

### Comparison Components
- **comparison** — Side-by-side before/after panels
- **two-col** — Two-column text layout

---

## Colour Usage

| Token | Hex | Usage |
|-------|-----|-------|
| primary | #3A3A3A | Main text |
| accent | #E55F4C | Brand highlight, stat values, active elements |
| slate_blue | #496986 | Secondary emphasis, links |
| gold | #E9A867 | Tertiary accent, warnings |
| sage | #6A9E98 | Success states, complete indicators |
| light_blue | #5CA2D1 | Info, links |
| ice | #D7ECF3 | Light background fills |
| background_warm | #F8F5F2 | Alternate row backgrounds |

## Typography

| Role | Font | Size |
|------|------|------|
| Hero title | Source Serif Pro SemiBold | 36pt |
| Section title | Source Serif Pro SemiBold | 28pt |
| Slide title | Source Serif Pro SemiBold | 22pt |
| Subtitle | Source Serif Pro SemiBold | 14pt |
| Body | Lato | 13pt |
| Labels/captions | Lato | 11pt |
| Eyebrow | Lato | 10pt |
| Big stat | Source Serif Pro SemiBold | 48pt |
| Stat grid value | Source Serif Pro SemiBold | 32pt |
