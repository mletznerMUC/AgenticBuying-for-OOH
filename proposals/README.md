# OOH Extension Proposals (OEPs)

An **OEP** is a single, self-contained, reviewable document proposing one change to
AdCP or AAMP. It is the unit we hand to a working group.

## Rules

- One OEP per coherent change. If it needs two independent decisions, split it.
- Copy [`TEMPLATE.md`](TEMPLATE.md) to `NNNN-short-title.md`, taking the next free
  number. `0000` is reserved for the template.
- An OEP must cite the `ADD-NNN@version` additions it carries, and the `R-*`
  requirement IDs from [`../ooh-specifics/`](../ooh-specifics/) that it satisfies.
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

An OEP bundles one or more **additions** ([`../additions/`](../additions/)) into a
coherent ask. Additions are the long-lived, versioned definitions; an OEP is a one-shot
submission. See [`../VERSIONING.md`](../VERSIONING.md) §5 for why the two are separate.

## Index

| OEP | Title | Target | Status |
| --- | --- | --- | --- |
| — | *none written yet* | | |

## Planned OEPs

Four are planned, bundling the R1.0 additions. Rationale and sequencing in
[`../PLAN.md`](../PLAN.md) §5.

| OEP | Title | Bundles | Target |
| --- | --- | --- | --- |
| 0001 | OOH product & offer shape | ADD-001, ADD-002, ADD-004, ADD-006 | AdCP Media Buy + Creative |
| 0002 | Briefs and offers in planning terms | ADD-015, ADD-005, ADD-012 | AdCP Media Buy + AAMP Agentic Direct |
| 0003 | Creative approval as a gated lifecycle | ADD-008, ADD-009, ADD-010 | AdCP Creative |
| 0004 | Orders and commercial prerequisites | ADD-014, ADD-013, ADD-011 | AAMP Agentic Direct |

None can be written yet: the blockers in [`../PLAN.md`](../PLAN.md) §6 must clear first —
in particular, every placement is still unverified against the current upstream
revisions, and OEP-0003 needs the Creative Pre-Approval API's rejection reason codes
([`../analysis/open-gaps.md`](../analysis/open-gaps.md) §1).
