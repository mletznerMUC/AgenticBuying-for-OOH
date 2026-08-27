# Schemas

JSON Schema drafts backing the proposals in [`../proposals/`](../proposals/).

Nothing here yet — schemas are written once an OEP's shape is agreed, so that the
discussion happens on the concept rather than on syntax.

## Conventions (to be confirmed)

- [ ] **Schema dialect** — match whatever the target protocol uses, per target. AdCP
      keeps its normative schemas under `static/schemas/source/`; check the dialect
      and conventions there before writing anything.
- [ ] **Layout** — one directory per target protocol, mirroring the upstream layout,
      so a diff against upstream is readable.
- [ ] **Naming** — `oep-NNNN-<name>.schema.json`, cross-linked from the OEP.
- [ ] **Namespacing** — if we propose extension objects rather than core fields,
      settle a namespace prefix early and use it consistently.
- [ ] **Validation** — a script that validates every schema and every example payload
      in the OEPs, so examples cannot drift from their schema.

## Planned layout

```
schemas/
├── adcp/     Drafts targeting Ad Context Protocol surfaces
└── aamp/     Drafts targeting AAMP component surfaces
```
