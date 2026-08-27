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

| Requirement | Target | Change type | Rationale | Confidence |
| --- | --- | --- | --- | --- |
| *TBD* | | | | |

## Open questions

- Does the existing product model tolerate a finite, enumerable inventory set, or
  does it assume an unbounded stream?
- Is there an existing extension mechanism (namespaced extension object, channel
  profile) we should use rather than adding top-level fields?
- How are reservations and holds handled today for guaranteed digital deals — can
  OOH reuse that machinery?
