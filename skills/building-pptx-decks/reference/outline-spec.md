# PPTX Outline Specification

> Structured YAML outline that the LLM generates and `render_pptx.py` consumes.

---

## Document Structure

```yaml
meta:
  title: "Deck Title"
  theme: credera            # matches brand folder name in context/brands/
  variant: default          # theme colour variant (default | sage | warm)
  author: ""
  date: ""                  # auto-fills to today if blank

slides:
  - layout: title           # layout key (see below)
    ...                      # layout-specific fields
```

---

## Layout Keys

### Structural Slides

| Key | Purpose | Required | Optional |
|-----|---------|----------|----------|
| `title` | Opening cover | `title` | `subtitle`, `client_logo` |
| `section` | Section break | `title` | `style: photo \| gradient` |
| `end` | Closing splash | — | `title` |
| `blank` | Custom-drawn | — | `title` |

### Content Slides

| Key | Purpose | Required | Optional |
|-----|---------|----------|----------|
| `content` | Title + body | `title`, `body` | `subtitle`, `eyebrow` |
| `two-col` | Two columns | `title`, `left`, `right` | `subtitle`, `eyebrow` |
| `stat` | Big stat | `title`, `value` | `subtitle`, `label` |
| `quote` | Quote + attribution | `quote`, `author` | `role`, `photo` |
| `comparison` | Before/after | `title`, `before`, `after` | `subtitle`, `eyebrow` |

### Data Slides

| Key | Purpose | Required | Optional |
|-----|---------|----------|----------|
| `stat-grid` | 3-6 metrics | `title`, `stats[]` | `subtitle`, `eyebrow` |
| `card-grid` | Auto-fit cards | `title`, `cards[]` | `subtitle`, `eyebrow`, `columns` |
| `data-table` | Tabular data | `title`, `headers[]`, `rows[][]` | `subtitle`, `eyebrow` |
| `highlight-grid` | Feature cards | `title`, `items[]` | `subtitle`, `eyebrow`, `columns` |

### Flow Slides

| Key | Purpose | Required | Optional |
|-----|---------|----------|----------|
| `step-flow` | Numbered steps | `title`, `steps[]` | `subtitle`, `eyebrow` |
| `funnel` | Decaying bars | `title`, `bars[]` | `subtitle`, `eyebrow` |
| `timeline` | Horizontal timeline | `title`, `events[]` | `subtitle`, `eyebrow` |
| `ascend` | Ascending columns | `title`, `nodes[]` | `subtitle`, `eyebrow` |

### Structure Slides

| Key | Purpose | Required | Optional |
|-----|---------|----------|----------|
| `layer-stack` | Tiered rows | `title`, `layers[]` | `subtitle`, `eyebrow` |
| `hub-spoke` | Centre + radial | `title`, `center`, `spokes[]` | `subtitle`, `eyebrow` |

### Process Slides

| Key | Purpose | Required | Optional |
|-----|---------|----------|----------|
| `process-loop` | Circular cycle | `title`, `nodes[]` | `subtitle`, `eyebrow`, `center_label` |

---

## Common Fields

```yaml
title: "Slide Title"
subtitle: "Supporting context"
eyebrow: "SECTION NAME"
notes: "Speaker notes go here"
```

---

## Field Definitions

### Body Text

```yaml
body: |
  Paragraph with **bold** and *italic* markdown.
  - Bullet point one
  - Bullet point two
    - Sub-bullet
```

### Stats Array

```yaml
stats:
  - value: "98%"
    label: "Client Satisfaction"
  - value: "$4.2M"
    label: "Revenue Impact"
```

### Cards Array

```yaml
cards:
  - title: "Card Title"
    body: "Description"
    icon: "🔧"
```

### Table Data

```yaml
headers: ["Phase", "Duration", "Owner", "Status"]
rows:
  - ["Discovery", "2 weeks", "Team A", "Complete"]
  - ["Design", "4 weeks", "Team B", "In Progress"]
```

### Steps Array

```yaml
steps:
  - title: "Discover"
    desc: "Identify requirements"
  - title: "Design"
    desc: "Architect the solution"
```

### Funnel Bars

```yaml
bars:
  - label: "Total Leads"
    value: 1000
    pct: 100
  - label: "Qualified"
    value: 340
    pct: 34
```

### Timeline Events

```yaml
events:
  - date: "Q1 2026"
    title: "Kickoff"
    desc: "Project initiation"
    status: complete    # complete | active | upcoming
```

### Layer Stack

```yaml
layers:
  - label: "Presentation Layer"
    items: ["React SPA", "Mobile App"]
  - label: "API Layer"
    items: ["API Gateway", "Auth Service"]
```

### Hub & Spokes

```yaml
center: "AI Platform"
spokes:
  - "Data Ingestion"
  - "Model Training"
  - "Inference API"
```

### Process Loop

```yaml
center_label: "Continuous Improvement"
nodes:
  - "Plan"
  - "Build"
  - "Test"
  - "Deploy"
```

### Comparison

```yaml
before:
  title: "Current State"
  items:
    - "Manual deployments"
    - "4-hour release cycles"
after:
  title: "Future State"
  items:
    - "CI/CD pipelines"
    - "15-minute releases"
```

### Highlight Items

```yaml
items:
  - title: "Feature Name"
    desc: "Brief description"
    icon: "⚡"
```

### Ascending Nodes

```yaml
nodes:
  - title: "Foundation"
    desc: "Basic infrastructure"
    stat: "Month 1-2"
  - title: "Optimization"
    desc: "Full maturity"
    stat: "Month 5-6"
```

---

## Notes for LLM Authors

1. Do not invent content — use only what the user provides
2. Alternate visual patterns — no 3+ consecutive same-category slides
3. Match shape to content — sequences → step-flow, comparisons → comparison, hierarchies → layer-stack, cycles → process-loop
4. Keep stat values short — 1-4 characters ("98%", "$4M", "3x")
5. Speaker notes encouraged for every content slide
6. 10-20 slides is the sweet spot
