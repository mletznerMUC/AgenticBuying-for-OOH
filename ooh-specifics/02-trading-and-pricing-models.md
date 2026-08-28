# 02 — Trading and pricing models

> Status: **stub** — outline only.

**Question this document answers:** what is actually being bought and sold in an OOH
transaction, and how is it priced?

## What this document will cover

- [ ] Trading units in use: per play, per slot, share of voice, share of time,
      panel per booking period, modelled CPM/CPT, cost per venue per period
- [ ] How the same inventory is sold on different units to different buyers
- [ ] Guaranteed/reserved vs biddable, and the large middle ground of
      pre-negotiated deals with programmatic execution
- [ ] Booking periods as trading units in classic OOH (calendar weeks, decades,
      months) and their fixed start dates
- [ ] Frequency and pacing expressed as loop share rather than impression pacing
- [ ] Minimum spends, minimum durations, minimum panel counts
- [ ] Floor prices, rate cards, seasonal and daypart multipliers
- [ ] Currency, tax and production/installation costs as separate line items
- [ ] What "budget" means when the constraint is physical capacity, not spend

## Why the digital-first assumption breaks

A pricing model enum of `cpm | cpc | cpcv` cannot express "€X per panel per calendar
week" or "20 % share of voice in this loop, 06:00–10:00, for two weeks". Nor can an
impression-pacing model express loop-share pacing.

> ### ⚠️ Partly contradicted by verification (2026-08-27)
>
> AdCP 3.2 is not limited to `cpm | cpc | cpcv`. It has twelve pricing options,
> including **`time-option`** (per `hour`/`day`/`week`/`month`, with `min_duration` and
> `max_duration`), **`flat-rate-option`** with DOOH parameters carrying
> **`sov_percentage`**, `loop_duration_seconds` and `min_plays_per_hour`, and
> **`cpp-option`** for cost per point. `OpenDirect.Product.ratetype` includes `CPD` and
> `FlatRate`.
>
> So panel-per-period pricing and share-of-voice **are** expressible. The claim above
> needs rewriting when this document is filled in. See
> [`../verification/adcp-3.2.md`](../verification/adcp-3.2.md) §4.

## Requirements

`R-TRD-1` … *to be written.*

## Open questions

- Do we extend the existing pricing-model enums, or introduce an OOH-specific
  pricing object that carries its own unit and basis?
- How should production and installation costs be represented so an agent can
  compare total cost across sellers?
- Can classic-OOH booking periods be expressed in the protocols' existing flight
  model, or do they need explicit period semantics?

## Related

- [`../mapping/adcp/media-buy.md`](../mapping/adcp/media-buy.md)
- [`../mapping/aamp/agentic-direct.md`](../mapping/aamp/agentic-direct.md)
