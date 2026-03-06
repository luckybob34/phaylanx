# Minimal — Default Theme Reference

> Brand-agnostic default theme. Uses system fonts and a neutral slate/blue palette. Clone this theme to scaffold a new brand.

---

## Color Tokens

| Token | Value |
|---|---|
| `--primary` | `#0F172A` (Slate 900) |
| `--accent` | `#2563EB` (Blue 600) |
| `--accent-light` | `#60A5FA` (Blue 400) |
| `--light-gray` | `#F1F5F9` (Slate 100) |

---

## Typography

System fonts only — no external dependencies, works fully offline:
- Headings: `'Segoe UI', system-ui, sans-serif`
- Body: Same stack

---

## Notes

- No brand-specific components — all shared components from the component library work as-is
- No theme variants
- Use as a starting point for new brand themes: copy the CSS below, update custom properties, add brand-specific selectors per [`../_contract.md`](../_contract.md)

---

## Theme CSS

The complete CSS theme for this brand. Inline this into the `<style>` block of the HTML deck.

```css
/* =================================================================
   MINIMAL THEME
   A clean, brand-agnostic starter theme. No external fonts or icon
   libraries required. Uses system fonts and a neutral slate palette.
   Clone this file and customise to create a new brand theme.
   ================================================================= */

/* ====================  TOKENS  ==================== */
:root {
    /* Core palette */
    --slate-900:  #0F172A;
    --slate-800:  #1E293B;
    --slate-700:  #334155;
    --slate-600:  #475569;
    --slate-500:  #64748B;
    --slate-400:  #94A3B8;
    --slate-300:  #CBD5E1;
    --slate-200:  #E2E8F0;
    --slate-100:  #F1F5F9;
    --slate-50:   #F8FAFC;
    --white:      #FFFFFF;
    --blue-600:   #2563EB;
    --blue-500:   #3B82F6;
    --blue-400:   #60A5FA;
    --blue-100:   #DBEAFE;
    --red-500:    #EF4444;

    /* Contract tokens (generic names) */
    --primary:          var(--slate-900);
    --primary-light:    var(--slate-700);
    --primary-lighter:  var(--slate-500);
    --primary-lightest: var(--slate-400);
    --accent:           var(--blue-600);
    --accent-light:     var(--blue-400);
    --accent-dark:      var(--blue-600);
    --brand-red:        var(--red-500);

    /* Typography */
    --font-heading: 'Segoe UI', system-ui, -apple-system, sans-serif;
    --font-body:    'Segoe UI', system-ui, -apple-system, sans-serif;

    /* Layout */
    --nav-width: 200px;

    /* Motion */
    --slide-easing: cubic-bezier(0.4, 0, 0.2, 1);
}

/* ====================  BODY  ==================== */
body {
    font-family: var(--font-body);
    color: var(--slate-800);
    background: var(--slate-100);
    -webkit-font-smoothing: antialiased;
}
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading);
}

/* ====================  NAVIGATION  ==================== */
.nav {
    background: var(--slate-900);
    border-right: 1px solid var(--slate-700);
}

/* Brand area */
.nav-brand {
    padding: 1.25rem 1rem;
    font-family: var(--font-heading);
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--blue-400);
    border-bottom: 1px solid var(--slate-700);
}
.nav-brand-sub {
    display: block;
    color: var(--slate-400);
    font-size: 0.6rem;
    font-weight: 400;
    margin-top: 0.15rem;
    letter-spacing: 1.5px;
}

/* Nav menu */
.nav-menu { padding: 0.5rem 0; }

.nav-section-label {
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--slate-500);
    padding: 0.9rem 1rem 0.3rem;
}

.nav-link {
    font-size: 0.72rem;
    padding: 0.45rem 1rem 0.45rem 1.25rem;
    color: var(--slate-400);
    border-left: 2px solid transparent;
    transition: background 0.15s, color 0.15s, border-color 0.15s;
}
.nav-link:hover {
    background: rgba(255, 255, 255, 0.04);
    color: var(--slate-200);
}
.nav-link.active {
    background: rgba(255, 255, 255, 0.06);
    color: var(--white);
    border-left-color: var(--blue-500);
    font-weight: 600;
}

.nav-divider {
    height: 1px;
    margin: 0.4rem 1rem;
    background: var(--slate-700);
}

/* Footer / controls */
.nav-footer {
    padding: 0.75rem 1rem;
    border-top: 1px solid var(--slate-700);
}
.nav-progress {
    height: 3px;
    background: var(--slate-700);
    border-radius: 2px;
    overflow: hidden;
    margin-bottom: 0.5rem;
}
.nav-progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--blue-600), var(--blue-400));
    border-radius: 2px;
    transition: width 0.4s ease;
    width: 16.67%;
}
.slide-counter {
    text-align: center;
    font-size: 0.65rem;
    color: var(--slate-500);
    margin-bottom: 0.4rem;
    font-variant-numeric: tabular-nums;
}
.slide-counter .current {
    color: var(--white);
    font-weight: 600;
}
.nav-controls {
    gap: 0.4rem;
    padding-top: 0.25rem;
}
.nav-btn {
    width: 28px;
    height: 28px;
    border-radius: 4px;
    background: var(--slate-800);
    color: var(--slate-400);
    font-size: 0.6rem;
    border: 1px solid var(--slate-700);
    transition: background 0.15s, color 0.15s;
}
.nav-btn:hover:not(:disabled) {
    background: var(--slate-700);
    color: var(--white);
}

/* ====================  SLIDES  ==================== */

/* --- Backgrounds --- */
.slide-dark {
    background: var(--slate-900);
    color: var(--white);
}
.slide-light {
    background: var(--white);
    color: var(--slate-800);
}
.slide-gray {
    background: var(--slate-100);
    color: var(--slate-800);
}
.slide-accent {
    background: var(--blue-600);
    color: var(--white);
}

/* Subtle pattern on dark & accent slides */
.slide-dark::before,
.slide-accent::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: 1;
    opacity: 0.03;
    background-image: repeating-linear-gradient(
        45deg,
        transparent,
        transparent 20px,
        currentColor 20px,
        currentColor 21px
    );
    pointer-events: none;
}

/* --- Slide inner --- */
.slide-inner {
    height: 100%;
    max-width: 90%;
    margin: 0 auto;
    padding: clamp(1.5rem, 3vw, 3.5rem) clamp(2rem, 4vw, 5rem);
    display: flex;
    flex-direction: column;
    justify-content: center;
}

/* --- Entry animations --- */
.slide-inner > * {
    opacity: 0;
    transform: translateY(16px);
    transition: opacity 0.5s ease, transform 0.5s ease;
}
.slide.visible .slide-inner > * { opacity: 1; transform: translateY(0); }
.slide.visible .slide-inner > *:nth-child(2) { transition-delay: 0.08s; }
.slide.visible .slide-inner > *:nth-child(3) { transition-delay: 0.16s; }
.slide.visible .slide-inner > *:nth-child(4) { transition-delay: 0.20s; }
.slide.visible .slide-inner > *:nth-child(5) { transition-delay: 0.24s; }
.slide.visible .slide-inner > *:nth-child(6) { transition-delay: 0.28s; }
.slide.visible .slide-inner > *:nth-child(7) { transition-delay: 0.32s; }

/* --- Slide footer accent bar --- */
.slide-footer {
    height: 3px;
    background: linear-gradient(90deg, var(--blue-600), var(--blue-400));
}
.slide-dark .slide-footer,
.slide-accent .slide-footer {
    background: linear-gradient(90deg, var(--blue-400), var(--slate-400));
}

/* --- Slide number --- */
.slide-number {
    bottom: 1rem;
    right: 1.5rem;
    font-size: 0.65rem;
    color: var(--slate-400);
    font-variant-numeric: tabular-nums;
}
.slide-dark .slide-number,
.slide-accent .slide-number { color: rgba(255,255,255,0.3); }

/* ====================  TYPOGRAPHY  ==================== */
.hero-title {
    font-family: var(--font-heading);
    font-size: clamp(2.2rem, 4vw, 4.5rem);
    font-weight: 700;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin-bottom: 0.75rem;
}
.hero-subtitle {
    font-size: clamp(0.75rem, 1vw, 1.1rem);
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--blue-400);
    margin-bottom: 0.75rem;
}
.hero-desc {
    font-size: clamp(1rem, 1.4vw, 1.5rem);
    line-height: 1.6;
    color: var(--slate-400);
    max-width: 700px;
}
.section-eyebrow {
    font-size: clamp(0.65rem, 0.85vw, 0.95rem);
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--blue-500);
    margin-bottom: 0.75rem;
}
.slide-dark .section-eyebrow,
.slide-accent .section-eyebrow { color: var(--blue-400); }

.slide-title {
    font-family: var(--font-heading);
    font-size: clamp(1.5rem, 2.5vw, 2.75rem);
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 0.5rem;
}
.slide-subtitle {
    font-size: clamp(0.85rem, 1.1vw, 1.2rem);
    color: var(--slate-500);
    margin-bottom: 1.5rem;
    line-height: 1.5;
}
.slide-dark .slide-subtitle { color: var(--slate-400); }
.slide-accent .slide-subtitle { color: rgba(255,255,255,0.7); }

/* ====================  COMPONENTS  ==================== */

/* --- Two-column --- */
.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}
.two-col-header {
    font-weight: 700;
    font-size: clamp(0.85rem, 1.1vw, 1.15rem);
    color: var(--blue-600);
    margin-bottom: 0.5rem;
    padding-bottom: 0.35rem;
    border-bottom: 2px solid var(--slate-200);
}
.slide-dark .two-col-header { color: var(--blue-400); border-bottom-color: var(--slate-700); }

/* --- Callout --- */
.callout {
    margin-top: 1.25rem;
    padding: 1rem 1.25rem;
    border-left: 3px solid var(--blue-500);
    background: var(--blue-100);
    border-radius: 0 6px 6px 0;
    font-size: clamp(0.82rem, 1.05vw, 1.15rem);
    line-height: 1.5;
}
.slide-dark .callout { background: rgba(59,130,246,0.08); }
.callout-label {
    font-weight: 700;
    font-size: clamp(0.7rem, 0.9vw, 0.95rem);
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--blue-600);
    margin-bottom: 0.35rem;
}

/* --- Stat grid --- */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem;
    margin-top: 1rem;
}
.stat-item { text-align: center; }
.stat-value {
    font-family: var(--font-heading);
    font-size: clamp(2rem, 3.5vw, 4rem);
    font-weight: 700;
    color: var(--blue-400);
    line-height: 1;
    margin-bottom: 0.35rem;
}
.stat-label {
    font-size: clamp(0.72rem, 0.9vw, 1rem);
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--slate-400);
}

/* --- Data table --- */
.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: clamp(0.78rem, 1vw, 1.1rem);
    margin-top: 1rem;
}
.data-table th {
    padding: 0.6rem 0.75rem;
    text-align: left;
    font-size: clamp(0.65rem, 0.85vw, 0.95rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--slate-500);
    border-bottom: 2px solid var(--slate-200);
}
.data-table td {
    padding: 0.6rem 0.75rem;
    border-bottom: 1px solid var(--slate-200);
    color: var(--slate-700);
    font-size: clamp(0.78rem, 1vw, 1.1rem);
}
.slide-dark .data-table th { color: var(--slate-400); border-bottom-color: var(--slate-700); }
.slide-dark .data-table td { color: var(--slate-300); border-bottom-color: var(--slate-700); }

/* --- Card grid --- */
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.card {
    background: var(--white);
    border: 1px solid var(--slate-200);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.15s, box-shadow 0.15s;
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
.card-body { padding: 1rem 1.25rem; }
.card-body h4 {
    font-size: clamp(0.85rem, 1.1vw, 1.2rem);
    font-weight: 700;
    margin-bottom: 0.35rem;
    color: var(--slate-900);
}
.card-body p {
    font-size: clamp(0.78rem, 1vw, 1.1rem);
    color: var(--slate-600);
    line-height: 1.5;
}
.slide-dark .card { background: var(--slate-800); border-color: var(--slate-700); }
.slide-dark .card-body h4 { color: var(--white); }
.slide-dark .card-body p { color: var(--slate-400); }

/* --- Highlight box --- */
.highlight-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.highlight-box {
    padding: 1.25rem;
    border-radius: 8px;
    background: var(--slate-100);
    border: 1px solid var(--slate-200);
}
.highlight-box h4 {
    font-size: clamp(0.82rem, 1.05vw, 1.15rem);
    font-weight: 700;
    margin-bottom: 0.4rem;
    color: var(--slate-900);
}
.highlight-box p {
    font-size: clamp(0.78rem, 1vw, 1.1rem);
    color: var(--slate-600);
    line-height: 1.5;
}
.slide-dark .highlight-box { background: var(--slate-800); border-color: var(--slate-700); }
.slide-dark .highlight-box h4 { color: var(--white); }
.slide-dark .highlight-box p { color: var(--slate-400); }

/* --- Badge pills --- */
.badge {
    display: inline-block;
    padding: 0.3rem 0.75rem;
    border-radius: 100px;
    font-size: clamp(0.68rem, 0.85vw, 0.9rem);
    font-weight: 600;
    background: var(--slate-200);
    color: var(--slate-700);
    margin: 0.15rem 0.2rem;
}
.badge-accent { background: var(--blue-100); color: var(--blue-600); }

/* --- Pillar grid --- */
.pillar-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
}
.pillar {
    background: var(--slate-100);
    border-radius: 8px;
    padding: 1.25rem;
    text-align: center;
    border-top: 3px solid var(--blue-500);
}
.pillar h4 { font-size: clamp(0.82rem, 1.05vw, 1.15rem); font-weight: 700; margin-bottom: 0.3rem; }
.pillar p { font-size: clamp(0.72rem, 0.9vw, 1rem); color: var(--slate-600); line-height: 1.4; }
.slide-dark .pillar { background: var(--slate-800); }
.slide-dark .pillar p { color: var(--slate-400); }

/* --- Program element list (vertical) --- */
.program-element-list {
    list-style: none;
    padding: 0;
    margin-top: 1rem;
}
.program-element-list li {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.6rem 0;
    font-size: clamp(0.82rem, 1.05vw, 1.15rem);
    border-bottom: 1px solid var(--slate-200);
}
.program-element-list li::before {
    content: '\2192';
    color: var(--blue-500);
    font-weight: 700;
    flex-shrink: 0;
}
.slide-dark .program-element-list li { border-bottom-color: var(--slate-700); }

/* --- Timeline --- */
.timeline {
    margin-top: 1rem;
    padding-left: 2rem;
    border-left: 2px solid var(--slate-300);
}
.timeline-node {
    position: relative;
    padding-bottom: 1.25rem;
}
.timeline-node::before {
    content: '';
    position: absolute;
    left: -2.35rem;
    top: 0.3rem;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--blue-500);
    border: 2px solid var(--white);
}
.timeline-label {
    font-size: clamp(0.68rem, 0.85vw, 0.9rem);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--blue-600);
    margin-bottom: 0.15rem;
}
.timeline-text {
    font-size: clamp(0.8rem, 1.05vw, 1.15rem);
    color: var(--slate-600);
    line-height: 1.5;
}
.slide-dark .timeline { border-left-color: var(--slate-700); }
.slide-dark .timeline-label { color: var(--blue-400); }
.slide-dark .timeline-text { color: var(--slate-400); }

/* --- Code block --- */
.code-block {
    margin-top: 1rem;
    padding: 1rem 1.25rem;
    background: var(--slate-900);
    color: var(--slate-300);
    border-radius: 6px;
    font-family: 'Cascadia Code', 'Fira Code', 'Consolas', monospace;
    font-size: clamp(0.78rem, 1vw, 1.1rem);
    line-height: 1.7;
    overflow-x: auto;
    white-space: pre;
}

/* ====================  UTILITY HELPERS  ==================== */
.grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.25rem; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }
.text-center { text-align: center; }
.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
```
