# 06 — Delivery and proof of play

> Status: **stub** — outline only.

**Question this document answers:** what does "delivered" mean in OOH, and what
evidence does a buying agent get?

## What this document will cover

- [ ] Proof of play: what a playout log record contains and who produces it
- [ ] Log latency: player logs may be batched, delayed or reconciled after the fact
- [ ] Plays delivered vs plays scheduled vs audience delivered
- [ ] Screen downtime, network outages, weather closures and how they surface
- [ ] Partial plays and how they are counted
- [ ] Reporting granularity: per screen, per network, per daypart, per creative
- [ ] Classic/static: installation proof, photographic evidence, posting reports
- [ ] Third-party verification and independent playout auditing
- [ ] Discrepancy handling, under-delivery, make-goods and credits
- [ ] Reconciliation and invoicing against verified delivery

## Why the digital-first assumption breaks

A near-real-time impression counter does not model an eventually-consistent playout
log that is reconciled days later, and has no concept of a photograph as delivery
evidence. Reporting also needs to distinguish clearly between what was *played*
(observed) and what was *seen* (modelled).

## Requirements

`R-DEL-1` … *to be written.*

## Open questions

- What reporting latency should the protocol assume, and how is provisional versus
  final data flagged?
- Should the protocol carry PoP records themselves, or a reference to an auditable
  log held elsewhere?
- How are make-goods represented — as an amendment to the existing buy or a new one?

## Related

- [`../mapping/adcp/media-buy.md`](../mapping/adcp/media-buy.md)
- [`../mapping/aamp/trust-and-transparency.md`](../mapping/aamp/trust-and-transparency.md)
