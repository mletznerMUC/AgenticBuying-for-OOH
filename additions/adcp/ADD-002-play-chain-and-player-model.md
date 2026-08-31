---
id: ADD-002
title: Play Chain and Master/Slave Player Model
version: 0.2.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §3 and Fig. 1"
targets:
  adcp: [media-buy]
  aamp: [artf, trust-and-transparency]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
protocol_ownership:
  owner: adcp
  secondary: [aamp]
upstream_status: partial
verified_against:
  adcp: 3.2.0-beta.8
  aamp: "agentic-direct/OpenDirect-2.1; ARTF/OpenRTB-2.6"
  date: 2026-08-27
---

# ADD-002 — Play Chain and Master/Slave Player Model

> Version 0.2.0 · Status: `draft` · Since `R1.0`
>
> **Protocol owner: AdCP** · also binds into AAMP
>
> 🟡 **Verified partially exists upstream** against AdCP 3.2.0-beta.8 and AAMP (OpenDirect 2.1 / OpenRTB 2.6) on 2026-08-27.

## Verification

AdCP `dooh_metrics` already reports loop plays, screens used and share of voice achieved, and `plays` is defined as the raw count before the multiplier. The delivery half exists; the **forecast** fan-out does not.

Full evidence: [`../verification/verdicts.md`](../../verification/verdicts.md) · [`../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) · [`../verification/aamp.md`](../../verification/aamp.md)


## Problem

One transaction in DOOH is not one ad render. Ströer states the chain explicitly:

```
1 DSP Impression  =  1 Master Play  ×  n Screen Plays  ×  n Total Audience Impressions
```

A single won bid fans out to many physical screens, each of which plays the creative,
and each play is seen by many people. Three different quantities are all called
"impressions" depending on who is speaking.

No protocol expresses this fan-out. A buyer agent cannot tell how many screens a bid
buys, cannot reconcile a delivery report against what it bought, and cannot compare
two sellers whose fan-out factors differ by an order of magnitude. Reporting
"impressions: 4.8m" without the chain is unfalsifiable.

## Semantic definition

1. A transaction MUST be able to declare the levels of the delivery chain it covers.
   The levels are:
   - **transaction** — one agreed buy (one won bid, or one order line)
   - **master play** — one scheduling decision distributed to a player group
   - **screen play** — one execution on one physical screen
   - **audience impression** — one modelled opportunity-to-see (see **ADD-001**)
2. A seller MUST state the **fan-out** between adjacent levels, as a forecast before
   delivery and as an actual after it.
3. Delivery reporting MUST report screen plays and audience impressions as separate
   quantities. Reporting only one is not conformant.
4. Where a master play distributes to a player group, the seller MUST be able to
   identify the group and SHOULD be able to enumerate its screens, subject to the
   disclosure tier in **ADD-005**.
5. An "impression" MUST NOT appear unqualified in any interface between agents. Every
   count carries its level.

## Programmatic binding

**Today (Ströer):** the chain is documented in prose only. In the transport, one bid
response yields one `${TOTAL_IMP}` value; the master/slave distribution is invisible.
Ströer SSP aggregates play confirmations from slave players internally (v6 Fig. 1)
and surfaces only the aggregate. Ad play reports and in-depth location reports exist
but are requested from operations out of band.

**Proposed:** the impression opportunity declares the master-play fan-out (screen
count, or player group identity) so a bidder knows what one win commits it to. The
settlement record reports both screen plays and audience impressions.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- how many screens the offer covers, and how many plays per screen over the period;
- the forecast fan-out at each level, so that the headline audience figure is
  decomposable;
- whether plays are distributed evenly across the screen set or concentrated;
- what will be reported back, at which level, and at what granularity.

Sketch:

```json
{
  "delivery_chain": {
    "screens": 412,
    "player_groups": 118,
    "forecast": {
      "master_plays": 96000,
      "screen_plays": 1240000,
      "audience_impressions": 4820000
    },
    "reporting_granularity": ["screen_play", "audience_impression"],
    "reporting_dimensions": ["screen", "daypart", "creative"]
  }
}
```

The decomposition is what makes an offer comparable. Two offers quoting the same
audience impressions but differing 10× in screen plays are completely different media
propositions, and today nothing in either protocol reveals that.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product / offer | `new-object` | Delivery-chain object with per-level forecasts |
| AdCP | Media Buy → delivery reporting | `add-field` | Screen plays and audience impressions as separate quantities |
| AAMP | ARTF | `add-field` | Master-play fan-out on the impression opportunity |
| AAMP | Trust and Transparency | `clarify-semantics` | Which level a reported "impression" refers to; play-level auditability |

## Partial conformance

- MAY omit `player_groups` where the seller does not expose grouping.
- MAY report screen plays at aggregate rather than per-screen granularity, if the
  disclosure tier (**ADD-005**) does not permit per-screen reporting.
- MUST NOT collapse screen plays and audience impressions into one figure.
- MUST NOT emit an unqualified "impressions" count.

## Open questions

- [ ] Is the master/slave grouping stable, or does it vary per play?
- [ ] Can a bidder decline a subset of the fan-out, or is a win all-or-nothing?
- [ ] How does this interact with sync groups (**ADD-007**) — is a sync group a
      player group, or an orthogonal concept?
- [ ] Should the chain be modelled as fixed levels, or as a general nested structure
      that other channels (cinema, audio) could reuse?

## Sources

- `../analysis/stroeer-ppv-baseline.md` §1
- Ströer PPV Implementation Guide v6, §3, §4.1 (Fig. 1: Ströer SSP aggregating play
  confirmations from Slave Players), Appendix (ad play reports, in-depth location
  reports)

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.2.0 | 2026-08-27 | Verified against AdCP 3.2.0-beta.8 and AAMP; added protocol ownership and upstream status |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
