# 03 — Audience and measurement

> Status: **stub** — outline only.

**Question this document answers:** when an OOH seller reports an audience figure,
what does the number mean and how can an agent trust or compare it?

## What this document will cover

- [ ] Plays vs contacts: the impression multiplier and where it comes from
- [ ] Market audience currencies and their methodologies (see
      [`../docs/measurement-currencies.md`](../docs/measurement-currencies.md))
- [ ] Visibility adjustment and the different definitions of "seen"
- [ ] Reach and frequency modelling across a panel set, and why it is not additive
- [ ] Demographic and target-group indexing against a currency panel
- [ ] Modelled vs measured vs verified figures, and required provenance metadata
- [ ] Pre-campaign forecast vs post-campaign report, and acceptable variance
- [ ] Attribution: exposure-based lift, footfall, brand studies

## Why the digital-first assumption breaks

`impressions: 1200000` with no provenance is not comparable across OOH sellers, and
silently invites an agent to optimise on a number whose basis differs per seller. It
also hides the fact that the figure is a model output with a confidence range.

## Requirements

`R-AUD-1` … *to be written.*

## Open questions

- Which provenance fields are mandatory versus optional?
- Should the protocol carry both the raw play count and the modelled audience,
  always?
- How do we express a confidence interval or methodology version in a way agents can
  actually use for comparison?

## Related

- [`../mapping/adcp/signals.md`](../mapping/adcp/signals.md)
- [`../mapping/aamp/agentic-audiences.md`](../mapping/aamp/agentic-audiences.md)
- [`../mapping/aamp/trust-and-transparency.md`](../mapping/aamp/trust-and-transparency.md)
