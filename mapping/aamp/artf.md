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

`P` = this surface is the addition's primary home (define the semantic here); `S` = secondary binding. Roles are from [`../../PLAN.md`](../../PLAN.md) §3. Target and change type are filled in once this surface is verified against the current upstream revision — see [`../../PLAN.md`](../../PLAN.md) §6.

| Addition (R1.0) | Role | Target | Change type | Confidence |
| --- | :-: | --- | --- | --- |
| [ADD-001](../../additions/aamp/ADD-001-total-audience-impressions.md) · Total Audience Impressions | `S` | | | unverified |
| [ADD-002](../../additions/adcp/ADD-002-play-chain-and-player-model.md) · Play chain / player model | `S` | | | unverified |
| [ADD-003](../../additions/adcp/ADD-003-delayed-play-confirmation.md) · Delayed play confirmation | `S` | | | unverified |
| [ADD-004](../../additions/aamp/ADD-004-venue-and-network-taxonomy.md) · Venue & network taxonomy | `S` | | | unverified |
| [ADD-005](../../additions/adcp/ADD-005-location-disclosure-tiers.md) · Location disclosure tiers | `S` | | | unverified |
| [ADD-006](../../additions/adcp/ADD-006-creative-format-constraints.md) · Creative format constraints | `S` | | | unverified |
| [ADD-007](../../additions/adcp/ADD-007-synchronised-multi-screen-delivery.md) · Sync groups | `S` | | | unverified |
| [ADD-009](../../additions/adcp/ADD-009-creative-integrity-and-caching.md) · Creative integrity & caching | `S` | | | unverified |
| [ADD-012](../../additions/adcp/ADD-012-advertiser-loop-separation.md) · Advertiser loop separation | `S` | | | unverified |
| [ADD-013](../../additions/adcp/ADD-013-deal-access-and-response-obligation.md) · Deal access & response obligation | `S` | | | unverified |

## Open questions

- Does ARTF inherit existing DOOH representations from established real-time bidding
  specifications, or define its own? If it inherits, our work is mostly alignment.
- How is the multiplied-impression concept currently handled, if at all?
- Is a bid request in ARTF per play, per loop, or per screen-hour?
