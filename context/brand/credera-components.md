# Credera Theme - Extended Component Library

> Components unique to the Credera theme, beyond the shared component library defined in `deck-skill.md`. These classes are **only** available when using `credera.css`.

---

## Brand System

### Logo

The Credera wordmark is an inline SVG with 8 `<path>` elements (geometric brand mark + "Credera" letterforms). Use `fill="currentColor"` so it inherits the parent's text color, or `fill="var(--accent)"` for explicit accent coloring.

**Nav sidebar** — place inside `.nav-brand`; CSS sizes it to 150px width:
```html
<div class="nav-brand">
    <svg class="nav-logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 32" fill="none">
        <path d="M0 0.034V31.979H21.709V24.495H7.486V7.52H24.461V21.744H31.944V0.034H0ZM24.461 24.495H31.944V31.979H24.461V24.495Z" fill="currentColor"/>
        <path d="M62.95 19.731C62.793 20.293..." fill="currentColor"/><!-- C -->
        <path d="M159.416 21.751..." fill="currentColor"/><!-- e -->
        <path d="M82.561 9.27..." fill="currentColor"/><!-- r -->
        <path d="M128.903 0.052..." fill="currentColor"/><!-- d -->
        <path d="M172.188 9.27..." fill="currentColor"/><!-- r -->
        <path d="M194.232 9.226..." fill="currentColor"/><!-- a -->
        <path d="M109.262 21.751..." fill="currentColor"/><!-- e -->
    </svg>
</div>
```

**Cover/bookend slide** — place inside `.cover-logo` (absolutely positioned, bottom-center, full-width). Use `style="opacity:0.12"` for a subtle watermark on dark slides or full opacity on cover slides:
```html
<div class="cover-logo">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 32" fill="none">
        <!-- Same 8 paths, fill="var(--accent)" or fill="#E55F4C" -->
    </svg>
</div>
```

> The full SVG paths are in `workspace/style-guide/archive/brands/credera/credera-template.html` (lines 1291 and 1340-1348). Copy the complete paths from there — the abbreviated versions above are for documentation only.

### Color Architecture

Colors are extracted from the **2024 Credera Global PowerPoint Accelerator** PPTX theme XML.

| Token | Hex | PPTX Source | Role |
|---|---|---|---|
| `--credera-red` | `#E55F4C` | accent2 | Brand mark, logo fill, bookend backgrounds |
| `--accent` | `#E55F4C` | accent2 | Primary interactive color (borders, highlights, active states, gradients, badges) |
| `--accent-light` | `#F08878` | derived | Hover states, light accents |
| `--accent-dark` | `#C94A38` | derived | Pressed states, emphasis |
| `--navy` | `#3A3A3A` | dk1 | Primary dark / text color |
| `--slate-blue` | `#496986` | accent1 | Extended palette, Warm variant accent |
| `--sky-blue` | `#5CA2D1` | accent4 | Charts, secondary highlights |
| `--warm-gold` | `#E9A867` | accent5 | Callouts, Sage variant accent |
| `--sage` | `#6A9E98` | accent6 | Subtle accents, Sage variant dark |
| `--light-gray` | `#F8F5F2` | lt2 | Page backgrounds, cover slides |
| `--ice-blue` | `#D7ECF3` | derived | Light info backgrounds |

Credera Red and `--accent` are intentionally the same value (`#E55F4C`). The separate token exists so bookend/logo usage is semantically distinct from interactive accent usage.

### Theme Variants

Three colour schemes available via `data-variant` on `<html>`:

| Variant | `data-variant` | Dark Tone | Accent | Usage |
|---|---|---|---|---|
| **Coral + Charcoal** | *(default)* | `#3A3A3A` | `#E55F4C` | Default, most versatile |
| **Sage + Gold** | `"sage"` | `#2A3D36` | `#E9A867` | Sustainability, growth, advisory |
| **Warm + Slate** | `"warm"` | `#4A3728` | `#496986` | Understated, enterprise, finance |

Apply by adding `data-variant="sage"` or `data-variant="warm"` to the `<html>` tag. No other changes needed.

### Typography Rules

Fonts from the PPTX font scheme (`majorFont` / `minorFont`):

- **Headlines**: Source Serif Pro SemiBold, uppercase, letter-spacing +2px
- **Subheadlines**: Source Serif Pro, regular weight, uppercase, letter-spacing +1px
- **Labels**: Lato Bold, all-caps, character spacing +0.5
- **Body copy**: Lato, line height 1.6; use Font Awesome 6 icons, never emojis

---

## Extended Components

### Cover Slide

| Class | Description |
|---|---|
| `.slide-cover` | Light-gray background cover with Credera branding |
| `.cover-date` | Date text at top |
| `.cover-title` | Large cover title (lighter weight than hero-title) |
| `.cover-logo` | Absolutely positioned SVG logo at bottom center |

### Callout Accent (Red)

| Class | Description |
|---|---|
| `.callout-accent` | Red-branded callout bar (uses `--credera-red` instead of accent) |
| `.callout-accent i` | Font Awesome icon, red |
| `.callout-accent span` | Body text |

### Success Highlight

| Class | Description |
|---|---|
| `.success-highlight` | Large accent-gradient callout box with left border |
| `.success-highlight h3` | Accent-coloured heading |
| `.success-highlight p` | Body text with generous line height |
| `.highlight-text` | Inline span for accent-dark emphasis |

### Timeline (Horizontal)

Credera's default timeline is **horizontal** with dot indicators, progress overlay, and staggered node states.

| Class | Description |
|---|---|
| `.timeline` | Horizontal flex container with `::before` track and `::after` progress fill |
| `.timeline-node` | Individual phase column |
| `.timeline-dot` | Circle indicator (28px) |
| `.timeline-node.completed` | Purple dot |
| `.timeline-node.active` | Purple dot with pulsing ring animation |
| `.timeline-label` | Phase name (uppercase, centered) |
| `.timeline-bullets` | Bullet list under a node |
| `.timeline-active-badge` | Small "CURRENT" pill badge |

> A vertical timeline variant is also available via `.timeline-vertical` wrapper.

### Question Items

| Class | Description |
|---|---|
| `.question-item` | Flex row for discussion prompts |
| `.question-number` | Gradient-background square with number |
| `.question-text` | Large italic question text |

### Program Elements

| Class | Description |
|---|---|
| `.program-elements` | Horizontal flex layout for dark slides |
| `.program-element` | Panel with accent top border |
| `.program-element-title` | White heading with bottom accent border |
| `.program-element-list` | Bullet list with accent square markers |

### Quote Block & Cards

| Class | Description |
|---|---|
| `.quote-block` | Large featured quote on dark background |
| `.quote-attr` | Attribution line (accent colour, uppercase) |
| `.quote-card` | Light card with accent left border |
| `.quote-text` | Italic quote text |
| `.quote-source` | Source attribution |

### Capabilities Band

| Class | Description |
|---|---|
| `.capabilities-band` | Full-width dark navy band |
| `.capabilities-band-label` | Accent uppercase label |
| `.capabilities-grid` | 3-column grid inside the band |
| `.capability-item` / `.capability-title` / `.capability-desc` | Individual capability |

### Equation Layout

| Class | Description |
|---|---|
| `.equation-layout` | Flex container for visual equations (A + B = C) |
| `.equation-column` | Individual term |
| `.equation-icon` | Circular icon container (80px) |
| `.equation-title` | Term label (uppercase) |
| `.equation-list` | Detail list under a term |
| `.equation-operator` | Large +/= sign between columns |

### Materials Grid

| Class | Description |
|---|---|
| `.materials-grid` | Flex layout for thumbnail sections |
| `.material-section` / `.material-section-wide` | Grouped panel with accent top border |
| `.material-section-header` / `-label` / `-desc` | Section header row |
| `.material-thumbs` / `.material-thumb` | Thumbnail image gallery |
| `.material-thumb-label` | Caption under thumbnail |

### Participants Grid

| Class | Description |
|---|---|
| `.participants-grid` | Auto-fit grid for stakeholder groups |
| `.participant-group` | Card with accent left border |
| `.participant-group h4` | Group name |
| `.participant-group li` | Individual name |

### Additional Utilities

| Class | Description |
|---|---|
| `.status-badge` | Inline badge (accent background, white text) |
| `.card-dark` | Dark variant card (navy background, accent top border) |
| `.card-clickable` | Card with enhanced hover (translateY -8px) |
| `.card-arrow` | CTA arrow text inside clickable cards |
| `.card-icon` | Gradient icon square (60px) |
| `.card-type` | Small uppercase type label |
| `.card-img` | Card image (180px height, accent bottom border) |

---

## Section Color Strategy

- **Title/closing slides** - Bookend with `.slide-dark` or Credera Red backgrounds (use sparingly)
- **Dark sections** - Jewel tone (`.slide-dark`, `.slide-accent`) for high-impact slides
- **Neutral slides** - `.slide-light` or `.slide-gray` for content-heavy slides
- **Never mix** jewel-tone colours within the same section
