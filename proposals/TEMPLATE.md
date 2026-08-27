# OEP-NNNN: <short title>

| | |
| --- | --- |
| **Status** | `draft` |
| **Target protocol** | AdCP / AAMP |
| **Target surface** | e.g. Media Buy → product discovery |
| **Target revision** | revision or version this was written against, and the date checked |
| **Author(s)** | |
| **Created** | YYYY-MM-DD |
| **Requirements** | `R-XXX-n`, `R-XXX-m` (from `ooh-specifics/`) |
| **Supersedes / superseded by** | |
| **Upstream issue/PR** | |

## Summary

One paragraph. What changes, and what becomes possible that is not possible today.

## Motivation

The OOH reality that the current protocol cannot express. Be concrete: name the
trading practice, the market, the field that is missing. Link the relevant
`ooh-specifics/` document rather than restating it.

## Current behaviour

What the protocol does today at this surface, quoted or referenced precisely. If an
agent tries to do this now, describe exactly how it fails or what it has to
misrepresent.

## Proposal

The change itself.

- **Change type:** `extend-enum` / `add-field` / `new-object` / `new-task` /
  `clarify-semantics`
- **Placement:** the exact object or task, and why here rather than elsewhere.

### Schema

```json
{
  "// draft schema or example payload": ""
}
```

Full schema drafts live in [`../schemas/`](../schemas/) and are referenced from here
once the shape is agreed.

### Field reference

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| | | | |

## Examples

At least one realistic end-to-end example. Use a real trading scenario — a named
market, a plausible panel set, a plausible period — not `foo`/`bar`.

## Alternatives considered

Other placements or shapes, and why they were not chosen. Include "do nothing" and
what it costs.

## Compatibility

- Backwards compatibility for existing implementers.
- Behaviour of an agent or seller that does not implement this.
- Whether anything becomes required that was previously optional.

## Market applicability

Which markets this holds for. Flag anything that is convention in one market and
different in another — a proposal that only fits one market needs to say so.

## Privacy and compliance

Any personal data touched, and any regulatory constraint. For most OOH proposals the
honest answer is "none — OOH is non-addressable", and saying so explicitly is useful.

## Open questions

- [ ] …
