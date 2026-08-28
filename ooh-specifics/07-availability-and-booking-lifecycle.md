# 07 — Availability and booking lifecycle

> Status: **stub** — outline only.

**Question this document answers:** how does an agent find out what is available,
hold it, and commit to it, when the supply is finite and physically constrained?

## What this document will cover

- [ ] Availability as a calendar, not a forecast: what is already sold, per screen,
      per daypart, per period
- [ ] Loop capacity as the binding constraint on DOOH availability
- [ ] Soft holds/options, hold expiry, and first-refusal conventions
- [ ] Firm booking, confirmation and contracting
- [ ] Lead times that cannot be compressed: print, logistics, installation,
      clearance, scheduling cutoffs
- [ ] Fixed booking-period start dates in classic OOH
- [ ] Amendments: extending, shortening, swapping panels, changing creative
- [ ] Cancellation windows, penalties and non-cancellable inventory
- [ ] Overbooking and how sellers resolve it
- [ ] Multi-seller plans: coordinating holds across media owners for one campaign

## Why the digital-first assumption breaks

An always-available, forecast-based auction model has no representation for a hold
that expires, a print deadline, or a booking that cannot start on an arbitrary
Tuesday. Agents that cannot reason about holds and lead times will produce plans
that cannot actually be executed.

> ### ⚠️ Partly contradicted by verification (2026-08-27)
>
> **A hold that expires is representable**: `OpenDirect.Line.reservedexpirydate`, in
> AAMP Agentic Direct. Lead time and minimum commitments are too —
> `OpenDirect.Product.leadtime` ("days from today that line can begin"), `minspend`,
> `minflight`, `maxflight`. AdCP adds `commercial-terms.cancellation_terms` and
> `core/cancellation-policy.json`, and `ChangeRequest` covers amendments.
>
> What remains genuinely unmet is the **availability calendar** — per-screen, per-daypart
> capacity — and fixed booking-period start dates. Narrow the claim above accordingly.
> See [`../verification/aamp.md`](../verification/aamp.md) §4.

## Requirements

`R-BOOK-1` … *to be written.*

## Open questions

- Does the hold/option lifecycle need to be in the protocol, or can it be handled as
  a seller-side detail behind a booking request?
- How should lead times be expressed so an agent can plan backwards from a live date?
- What is the right failure semantic when availability changes between quote and
  commit?

## Related

- [`../mapping/adcp/media-buy.md`](../mapping/adcp/media-buy.md)
- [`../mapping/aamp/agentic-direct.md`](../mapping/aamp/agentic-direct.md)
