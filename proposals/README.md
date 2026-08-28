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
coherent ask to **one** protocol. Additions are the long-lived, versioned definitions;
an OEP is a one-shot submission. See [`../VERSIONING.md`](../VERSIONING.md) §5.

## Proposals are organised by target protocol

```
proposals/
├── adcp/     Proposals to AdCP        — OEP-ADCP-NNNN
└── aamp/     Proposals to AAMP        — OEP-AAMP-NNNN
```

An OEP targets exactly one protocol. A change needing both is two OEPs that reference
each other — they will be reviewed by different people, on different schedules, in
different repositories.

| Directory | Upstream | Verified against |
| --- | --- | --- |
| [`adcp/`](adcp/) | `adcontextprotocol/adcp` | 3.2.0-beta.8 |
| [`aamp/`](aamp/) | `IABTechLab/*` | OpenDirect 2.1, OpenRTB 2.6 |

## Status

**No OEP has been written yet.** Verification
([`../verification/`](../verification/)) substantially changed what should be proposed:
four of the sixteen additions turned out to be already satisfied upstream, and eight
more only partially unmet. The planned lists in
[`adcp/README.md`](adcp/README.md) and [`aamp/README.md`](aamp/README.md) reflect the
corrected picture — **confirmed gaps first**.

## Rules

- One OEP per coherent change, to one protocol. If it needs two independent decisions,
  split it.
- Copy [`TEMPLATE.md`](TEMPLATE.md) into the target protocol's directory as
  `OEP-<PROTO>-NNNN-slug.md`, taking the next free number **for that protocol**.
- An OEP must cite the `ADD-NNN@version` additions it carries, and the `R-*`
  requirement IDs from [`../ooh-specifics/`](../ooh-specifics/) that it satisfies.
- An OEP must name the target surface **and the revision it was written against**.
  Verification found R1.0's assumptions wrong often enough that this is not optional.
- An OEP must state what already exists upstream and why it is insufficient. A proposal
  that re-proposes an existing field will be rejected, and rightly.
- An OEP is not a discussion thread. Discussion happens in the pull request; the
  document records the decision.

## Status values

| Status | Meaning |
| --- | --- |
| `draft` | Being written; not ready for review |
| `review` | Open for review in this repository |
| `ready` | Agreed here, ready to submit upstream |
| `submitted` | Filed upstream — link the issue/PR |
| `accepted` | Adopted upstream |
| `rejected` | Declined or withdrawn — keep the document and record why |
| `superseded` | Replaced by a later OEP — link it |
