# Additions

An **addition** is one normative extension unit: a single OOH concept, defined
independently of any transport, with bindings that show how it appears in both
programmatic and insertion-order buying, plus its proposed placement in AdCP and
AAMP.

Additions are the versioned core of this repository. See
[`../VERSIONING.md`](../VERSIONING.md) for the scheme, and
[`REGISTRY.md`](REGISTRY.md) for the index.

## Organised by owning protocol

```
additions/
├── adcp/        13 additions whose definition belongs in AdCP
├── aamp/         3 additions whose definition belongs in AAMP
└── releases/     Frozen manifests
```

The directory names the protocol that owns the **definition**. Most additions still
bind into both protocols — the `protocol_ownership` front matter names the secondary
bindings, and each addition's Proposed placement table gives the per-surface detail.

`scripts/validate.py` enforces the placement: an addition whose `owner` disagrees with
its directory is an error, so the structure cannot silently drift.

Every addition also declares `upstream_status` — 🟢 `exists`, 🟡 `partial` or
🔴 `gap` — from [`../verification/verdicts.md`](../verification/verdicts.md).

## Where additions come from

Release R1 is derived entirely from analysis of Ströer's production DSP integration
standards — see [`../analysis/`](../analysis/). These are not speculative
requirements; each one is a concept a media owner already had to invent privately in
order to sell DOOH programmatically.

## The three layers of every addition

This structure is the point of the whole exercise. Ströer's additions exist only in
the bottom layer; agentic buying needs all three.

```
┌─────────────────────────────────────────────────────────────┐
│  1. SEMANTIC DEFINITION            transport-neutral        │
│     What the concept IS. No field names, no protocol.       │
│     "The audience of one play is a modelled, fractional      │
│      count restated after the play occurs."                 │
└─────────────────────────────────────────────────────────────┘
            │                                   │
            ▼                                   ▼
┌───────────────────────────┐   ┌─────────────────────────────┐
│  2a. PROGRAMMATIC BINDING │   │  2b. OFFER / IO BINDING     │
│  Bid request/response,    │   │  Brief → offer → order.     │
│  macros, notifications.   │   │  What a buyer agent reads   │
│  Where Ströer is today.   │   │  BEFORE any bid exists.     │
└───────────────────────────┘   └─────────────────────────────┘
```

### Why the offer/IO binding is not optional

The brief asked for this explicitly, and it is the difference between a protocol
that works for OOH and one that does not.

In OOH the majority of spend is still transacted by insertion order, and in Ströer's
case **every** deal — programmatic included — is contingent on an IO issued by sales
(see **ADD-014**). A buyer agent that sends a brief and receives an offer must be
able to understand, from the offer alone:

- what it will be billed on, and that the figure is modelled and fractional (**ADD-001**)
- which venues and networks it is buying (**ADD-004**)
- how precisely the locations will be disclosed, and at what price (**ADD-005**)
- that some screens will only accept static creative (**ADD-006**)
- that some screens must be bought as a synchronised pair (**ADD-007**)
- how long creative approval takes, and that it can fail (**ADD-008**)
- what it must declare before it can run anything (**ADD-011**)
- when it will be invoiced and by whom (**ADD-014**)
- in what planning terms the offer is expressed — SOV, GRP, OTS, dwell (**ADD-015**)

None of that is discoverable from a bid request, because at brief time there is no
bid request. Every addition therefore carries an offer binding, even when its
programmatic binding is the one that exists today.

`applies_to` in each addition's front matter records which bindings are meaningful:
`[programmatic, io]` for most, `[programmatic]` only where the concept genuinely has
no offer-time meaning.

## Document structure

Every addition file has the same sections:

| Section | Content |
| --- | --- |
| Front matter | Machine-readable metadata (see `../VERSIONING.md`) |
| **Problem** | What breaks today, concretely |
| **Semantic definition** | The concept, transport-neutral. Normative. |
| **Programmatic binding** | How it is or should be carried in RTB — including Ströer's current encoding |
| **Offer / IO binding** | How it appears in a brief response or order, so an agent can reason before bidding |
| **Proposed placement** | Target surfaces in AdCP and AAMP, with change type |
| **Partial conformance** | What may be omitted while still claiming support |
| **Open questions** | |
| **Sources** | Citations into `../analysis/` and the source documents |
| **Changelog** | One row per version |

## Adding a new addition

1. Copy [`TEMPLATE.md`](TEMPLATE.md) to `<owner>/ADD-NNN-slug.md` with the next free
   ID, in the directory of the protocol that owns the definition.
2. Fill in the front matter — `version: 0.1.0`, `status: draft`, `protocol_ownership`,
   `upstream_status`.
3. Add a row to [`REGISTRY.md`](REGISTRY.md).
4. Note it in [`CHANGELOG.md`](CHANGELOG.md) under the unreleased heading.
5. It joins a release only when a release manifest pins it.
6. Run `python3 scripts/validate.py` — it checks front matter, ID agreement, SemVer and
   registry consistency, and will tell you if you missed step 3.
