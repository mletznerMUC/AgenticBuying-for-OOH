# OOH Extension Proposals (OEPs)

An **OEP** is a single, self-contained, reviewable document proposing one change to
AdCP or AAMP. It is the unit we hand to a working group.

## Rules

- One OEP per coherent change. If it needs two independent decisions, split it.
- Copy [`TEMPLATE.md`](TEMPLATE.md) to `NNNN-short-title.md`, taking the next free
  number. `0000` is reserved for the template.
- An OEP must cite the `R-*` requirement IDs from
  [`../ooh-specifics/`](../ooh-specifics/) that it satisfies.
- An OEP must name the target protocol, surface and revision it was written against.
- An OEP is not a discussion thread. Discussion happens in the pull request; the
  document records the resulting decision.

## Status values

| Status | Meaning |
| --- | --- |
| `draft` | Being written; not ready for review |
| `review` | Open for review in this repository |
| `ready` | Agreed here, ready to submit upstream |
| `submitted` | Filed with the AdCP or AAMP project — link the upstream issue/PR |
| `accepted` | Adopted upstream |
| `rejected` | Declined upstream, or withdrawn — keep the document and record why |
| `superseded` | Replaced by a later OEP — link it |

## Index

| OEP | Title | Target | Status |
| --- | --- | --- | --- |
| — | *none yet* | | |

## Likely first OEPs

Candidates, in rough order of value against effort:

1. **OOH product shape** — describing screens, networks, loops, venue types and
   capacity in AdCP Media Buy product discovery.
2. **Geospatial and venue targeting** — radius, polygon, isochrone, POI proximity and
   venue taxonomy as first-class targeting dimensions.
3. **Play-based and SOV pricing units** — extending the pricing model beyond
   impression-based units.
4. **Proof of play and modelled-vs-observed delivery** — delivery reporting that
   distinguishes plays from contacts and carries provenance.
5. **DOOH creative format constraints** — exact duration, orientation, silent,
   no-click, multi-frame.

Each needs its `ooh-specifics` requirements written and its target surface verified
first.
