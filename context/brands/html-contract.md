# CSS Theme Contract

> Every theme CSS file must satisfy this contract so it works with `base-template.html` without modification.

---

## Required CSS Custom Properties

Define these on `:root`. The base engine references `--nav-width` and `--slide-easing`; the remainder are conventions your own rules should use for consistency.

| Variable | Purpose | Example (Minimal) |
|---|---|---|
| `--nav-width` | Sidebar width | `200px` |
| `--slide-easing` | Slide track cubic-bezier | `cubic-bezier(0.4, 0, 0.2, 1)` |
| `--primary` | Main dark colour | `#0F172A` |
| `--primary-light` | Lighter variant | `#334155` |
| `--primary-lighter` | Body text on light bg | `#64748B` |
| `--primary-lightest` | Muted text | `#94A3B8` |
| `--accent` | Hero accent colour | `#2563EB` |
| `--accent-light` | Lighter accent | `#60A5FA` |
| `--accent-dark` | Darker accent | `#2563EB` |
| `--white` | White | `#FFFFFF` |
| `--light-gray` | Light background | `#F1F5F9` |
| `--font-heading` | Heading font stack | `'Segoe UI', system-ui, sans-serif` |
| `--font-body` | Body font stack | `'Segoe UI', system-ui, sans-serif` |

> Themes may add brand-specific variables for internal use.

---

## Required Selectors

The theme CSS **must** style every selector below. The base HTML uses these classes.

### Body & Typography

| Selector | What to define |
|---|---|
| `body` | `font-family`, `background`, `color`, `line-height` |
| `.hero-title` | Font, size, colour, margin |
| `.hero-subtitle` | Font, size, colour, margin |
| `.hero-desc` | Font size, colour, max-width |
| `.section-eyebrow` | Small uppercase label above slide title |
| `.slide-title` | Slide heading (h2) |
| `.slide-subtitle` | Slide sub-heading |

### Navigation

| Selector | What to define |
|---|---|
| `.nav` | Background, border |
| `.nav-brand` | Padding, font, colour, border-bottom |
| `.nav-brand-sub` | Subtitle text styling (or `display:none`) |
| `.nav-menu` | Padding, scrollbar styling |
| `.nav-section-label` | Small uppercase group label |
| `.nav-divider` | Visual separator (height, background, margin) |
| `.nav-link` | Padding, font-size, colour, border-left, transition |
| `.nav-link:hover` | Hover state |
| `.nav-link.active` | Active indicator (colour, border, background) |
| `.nav-footer` | Padding, border-top |
| `.nav-progress` | Progress bar track (height, background, border-radius) |
| `.nav-progress-fill` | Progress bar fill (background gradient, transition) |
| `.slide-counter` | Font, colour, alignment |
| `.slide-counter .current` | Highlighted current number |
| `.nav-controls` | Gap, margin-top |
| `.nav-btn` | Size, border, colour, transitions |
| `.nav-btn:hover` | Hover state |

### Slides

| Selector | What to define |
|---|---|
| `.slide-inner` | `height`, `max-width` (use `%`, not fixed `px`), `padding` (use `clamp()` for responsive scaling), flex/centering |
| `.slide-dark` | Background, text colour |
| `.slide-dark::before` | Optional pattern overlay |
| `.slide-light` | Background, text colour |
| `.slide-gray` | Background, text colour |
| `.slide-accent` | Background gradient, text colour |
| `.slide-accent::before` | Optional pattern overlay |
| `.slide-footer` | `height`, `background` gradient |
| `.slide-number` | `bottom`, `right`, font, colour, opacity |

### Components (minimum set)

| Selector | What to define |
|---|---|
| `.two-col` | Grid layout (2 columns) |
| `.two-col-header` | Column header label |
| `.callout` | Left-border callout box |
| `.callout-label` | Callout title text |
| `.callout p` | Callout body text |
| `.stat-grid` | Grid layout for metrics |
| `.stat-item` | Individual metric card |
| `.stat-value` | Large metric number |
| `.stat-label` | Metric description text |
| `.data-table` | Full table styling (thead, td, hover) |
| `.card-grid` | Card layout container |
| `.card` | Individual card styling |
| `.card-body` | Card content area |

### Components (variety set)

These selectors are **strongly recommended** to avoid visual monotony. Themes that omit them will fall back on box grids for all content.

| Selector | What to define |
|---|---|
| `.step-flow` | Horizontal flex container for numbered step nodes |
| `.step-node` | Individual step (number, title, desc) |
| `.step-arrow` / `.step-arrow-line` | Connector line between steps |
| `.before-after` | Flex row: `.before-panel` + `.ba-arrow` + `.after-panel` |
| `.metric-strip` | Single-row stat dashboard. Supports `--ms-bg`, `--ms-text` CSS vars |
| `.metric-strip-item` | Individual metric (`.metric-strip-value`, `.metric-strip-label`) |
| `.funnel` | Vertical decaying bars. Children: `.funnel-bar` with `--bar-width`, `--bar-color` |
| `.layer-stack` | Stacked tier rows. Children: `.layer-row` > `.layer-item` |
| `.hub-spoke` | Radial layout with SVG lines. Center: `.hub-center`, nodes: `.hub-spoke-node` |
| `.annotated-stack` | Vertical layers + side notes. `.annotated-stack-layers` + `.annotated-stack-annotations` |
| `.process-loop` | Circular SVG ring + positioned nodes. `.loop-ring`, `.loop-center`, `.loop-node` |
| `.ascend-timeline` | Ascending columns for growth narratives. Children: `.ascend-node` |

> Themes may add extra components (timeline, quote-block, equation-layout, etc.) beyond this minimum set. Document them in a companion file or in the deck skill hardprompt.

### Responsive Typography

All content `font-size` values must use `clamp(min-rem, vw-preferred, max-rem)` so text scales with the viewport. Navigation and UI elements (`.nav-*`, `.slide-counter`, `.nav-btn`) keep fixed `rem` sizes since the sidebar has a fixed width.

---

## Optional Features

### Slide Entry Animations

If your theme uses the `.visible` class to animate slide content on entry, define:

```css
.slide-inner > * {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.5s ease, transform 0.5s ease;
}
.slide.visible .slide-inner > * {
    opacity: 1;
    transform: translateY(0);
}
/* Stagger children */
.slide.visible .slide-inner > *:nth-child(1) { transition-delay: 0.1s; }
.slide.visible .slide-inner > *:nth-child(2) { transition-delay: 0.2s; }
/* … up to :nth-child(5) */
```

The JS engine always toggles `.visible`. Themes without these rules will show content instantly - no harm done.

### Top Progress Bar

To enable the fixed top progress bar instead of (or alongside) the nav progress:

```css
.top-progress {
    display: block;
    background: linear-gradient(90deg, var(--accent), var(--accent-light));
}
/* Optionally hide nav progress */
.nav-progress { display: none; }
```

### Theme Variants (`data-variant`)

Themes with multiple colour variants should override `:root` variables on `html[data-variant="name"]`:

```css
html[data-variant="alt"] {
    --primary: #173E2F;
    --accent:  #C8D630;
    /* ... */
}
```

No HTML or JS changes required - CSS-only swap.

---

## File Naming

| File | Purpose |
|---|---|
| `context/brands/<brand>/brand.md` | Brand reference (tokens, typography, logo, extended components) |
| `context/brands/<brand>/theme.css` | Complete theme CSS |
| `context/brands/html-contract.md` | This document |
| `context/brands/component-library.md` | Shared component library (brand-agnostic) |
| `context/brands/minimal/` | Minimal (brand-agnostic) theme |
| `context/brands/credera/` | Credera brand theme (3 colour variants) |
| `context/brands/quanta/` | Quanta Services brand theme |


---

## Testing Checklist

After creating or editing a theme, verify:

- [ ] All 4 slide types render correctly (dark, light, gray, accent)
- [ ] Nav sidebar scrolls when many items are present
- [ ] Active nav link highlights on slide change
- [ ] Progress bar updates
- [ ] Slide entry animations fire (if applicable)
- [ ] Prev/next buttons work and disable at boundaries
- [ ] Keyboard, wheel, and touch navigation work
- [ ] Components render on both dark and light slides
