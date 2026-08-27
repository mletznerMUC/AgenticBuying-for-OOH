# AAMP — Agentic Real-Time Framework (ARTF)

> Status: **stub** — targets identified, mapping not yet written.
> Component scope below is from public sources as of August 2026 and needs
> verification against the current revision.

ARTF defines how agents operate inside real-time programmatic environments. This is
where **programmatic DOOH** lives.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Impression representation | One play equals many contacts — the impression multiplier, and its provenance |
| Screen/placement context | Screen properties, venue type, geography, loop position, operating state |
| Loop constraints | Slots per loop, SOV limits, competitive separation within the loop |
| Timing | Play-out scheduling latency, and the fact that a bid decision precedes a play by an interval |
| Creative constraints in-bid | Exact duration, resolution, orientation, no audio, no click |
| Trigger conditions | Weather, transit and event conditions evaluated at play-out time |
| Existing DOOH conventions | Alignment with how DOOH is already represented in real-time bidding today, rather than a parallel model |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 01 Inventory, 03 Audience,
04 Targeting, 05 Creative.

## Mapping table

| Requirement | Target | Change type | Rationale | Confidence |
| --- | --- | --- | --- | --- |
| *TBD* | | | | |

## Open questions

- Does ARTF inherit existing DOOH representations from established real-time bidding
  specifications, or define its own? If it inherits, our work is mostly alignment.
- How is the multiplied-impression concept currently handled, if at all?
- Is a bid request in ARTF per play, per loop, or per screen-hour?
