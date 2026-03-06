---
name: building-apps
description: Builds full-stack applications using the ATLAS workflow — architect requirements, trace data schema and integrations, link and validate all connections, assemble with layered architecture, and stress-test before shipping. Ensures apps are production-ready, not just demos.
allowed-tools: Terminal
---

# App Builder — ATLAS Workflow

Build full-stack applications that are production-ready, not just demos.

| Step | Phase | What You Do |
|------|-------|-------------|
| **A** | Architect | Define problem, users, success metrics |
| **T** | Trace | Data schema, integrations map, stack proposal |
| **L** | Link | Validate ALL connections before building |
| **A** | Assemble | Build with layered architecture |
| **S** | Stress-test | Test functionality, error handling |

For production builds, add: **V** (Validate security/edge cases) + **M** (Monitor logging/observability).

---

## A — Architect

1. **What problem does this solve?** — One sentence.
2. **Who is this for?** — Specific user, not "everyone".
3. **What does success look like?** — Measurable outcome.
4. **Constraints?** — Budget (API costs), time (MVP vs full), technical mandates.

Save to `workspace/<project-slug>/brief/app-brief.md`.

---

## T — Trace

### Data Schema

Define source of truth BEFORE building:

```
Tables:
- users (id, email, name, created_at)
- items (id, user_id, title, content, created_at)

Relationships:
- users 1:N items
```

### Integrations Map

| Service | Purpose | Auth Type | MCP Available? |
|---------|---------|-----------|----------------|

### Technology Stack

Based on requirements, propose: database, backend, frontend, other services. User approves before proceeding.

### Edge Cases

Document what could break: rate limits, auth expiry, timeouts, invalid input, MCP unavailability.

Save to `workspace/<project-slug>/design/` — `schema.md`, `stack.md`, `integrations.md`, `edge-cases.md`.

---

## L — Link

Validate ALL connections before building:

```
[ ] Database connection tested
[ ] All API keys verified
[ ] MCP servers responding
[ ] OAuth flows working
[ ] Environment variables set
[ ] Rate limits understood
```

All green → proceed. Any failure → fix first.

Save to `workspace/<project-slug>/tests/connection-validation.md`.

---

## A — Assemble

### Build Order

1. Database schema first
2. Backend API routes second
3. Frontend UI last

### Architecture Layers

- **Frontend** — UI components, interactions, display logic
- **Backend** — API routes, business logic, data validation
- **Database** — Schema, migrations, indexes

Save code to `workspace/<project-slug>/src/` following framework conventions.

---

## S — Stress-test

### Functional

```
[ ] All buttons work
[ ] Data saves and retrieves
[ ] Navigation works
[ ] Error states handled
```

### Integration

```
[ ] API calls succeed
[ ] MCP operations work
[ ] Auth persists across sessions
[ ] Rate limits not exceeded
```

### Edge Cases

```
[ ] Invalid input handled
[ ] Empty states display correctly
[ ] Network errors show feedback
[ ] Long text doesn't break layout
```

Save to `workspace/<project-slug>/tests/test-report.md`.

---

## Anti-Patterns

1. Building before designing → rewrite everything
2. Skipping connection validation → hours wasted
3. No data modeling → schema changes cascade
4. No testing → ship broken code
5. Hardcoding everything → no flexibility

---

## Workspace Structure

```
workspace/<project-slug>/
├── brief/
│   └── app-brief.md
├── design/
│   ├── schema.md
│   ├── stack.md
│   ├── integrations.md
│   └── edge-cases.md
├── src/
├── tests/
│   ├── connection-validation.md
│   └── test-report.md
└── notes/
```

---

## Note

Deployment is NOT part of this workflow — it's a separate, user-initiated action. Use `deploying-infrastructure` when ready.
