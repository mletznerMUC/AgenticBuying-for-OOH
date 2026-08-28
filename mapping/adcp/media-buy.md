# AdCP — Media Buy

> Status: **stub** — targets identified, mapping not yet written.
> Task and field names below are from public sources as of August 2026 and need
> verification against the current revision.

The Media Buy domain carries most of the OOH work: inventory discovery, targeting,
pricing, booking and delivery reporting.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Product discovery (`get_products`) | Describing OOH supply: screens, networks, loops, venue types, geography, capacity, measurement currency |
| Targeting | Geospatial (radius, polygon, isochrone), POI proximity, venue taxonomy, dayparts, triggers, screen/network lists |
| Pricing model | Per play, per slot, share of voice, share of time, panel per booking period, modelled CPM — alongside the existing units |
| Buy creation (`create_media_buy`) | Reservation and hold semantics, fixed booking-period starts, lead times, minimum commitments, amendments and cancellation terms |
| Delivery reporting (`get_media_buy_delivery`) | Plays vs modelled audience, per-screen granularity, proof-of-play references, provisional vs final data, under-delivery and make-goods |
| Pacing | Loop-share pacing rather than impression pacing |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/):
01 Inventory, 02 Trading & pricing, 04 Targeting, 06 Delivery, 07 Booking, 10 Sustainability.

## Mapping table

`P` = this surface is the addition's primary home (define the semantic here); `S` = secondary binding. Roles are from [`../../PLAN.md`](../../PLAN.md) §3. Target and change type are filled in once this surface is verified against the current upstream revision — see [`../../PLAN.md`](../../PLAN.md) §6.

| Addition (R1.0) | Role | Target | Change type | Confidence |
| --- | :-: | --- | --- | --- |
| [ADD-001](../../additions/aamp/ADD-001-total-audience-impressions.md) · Total Audience Impressions | `P` | | | unverified |
| [ADD-002](../../additions/adcp/ADD-002-play-chain-and-player-model.md) · Play chain / player model | `P` | | | unverified |
| [ADD-003](../../additions/adcp/ADD-003-delayed-play-confirmation.md) · Delayed play confirmation | `P` | | | unverified |
| [ADD-004](../../additions/aamp/ADD-004-venue-and-network-taxonomy.md) · Venue & network taxonomy | `P` | | | unverified |
| [ADD-005](../../additions/adcp/ADD-005-location-disclosure-tiers.md) · Location disclosure tiers | `P` | | | unverified |
| [ADD-013](../../additions/adcp/ADD-013-deal-access-and-response-obligation.md) · Deal access & response obligation | `P` | | | unverified |
| [ADD-006](../../additions/adcp/ADD-006-creative-format-constraints.md) · Creative format constraints | `S` | | | unverified |
| [ADD-007](../../additions/adcp/ADD-007-synchronised-multi-screen-delivery.md) · Sync groups | `S` | | | unverified |
| [ADD-012](../../additions/adcp/ADD-012-advertiser-loop-separation.md) · Advertiser loop separation | `S` | | | unverified |
| [ADD-014](../../additions/aamp/ADD-014-accreditation-io-and-settlement.md) · Accreditation, IO & settlement | `S` | | | unverified |
| [ADD-015](../../additions/adcp/ADD-015-ooh-planning-metrics.md) · OOH planning metrics | `S` | | | unverified |
| [ADD-016](../../additions/adcp/ADD-016-seller-conformance-profile.md) · Seller conformance profile | `S` | | | unverified |

## Open questions

- Does the existing product model tolerate a finite, enumerable inventory set, or
  does it assume an unbounded stream?
- Is there an existing extension mechanism (namespaced extension object, channel
  profile) we should use rather than adding top-level fields?
- How are reservations and holds handled today for guaranteed digital deals — can
  OOH reuse that machinery?
