# Audience measurement and currencies

> Status: **stub** — outline only.

**Question this document answers:** when an OOH product reports "impressions", what
exactly is being reported, who produced the number, and how can an agent compare it
across sellers and markets?

## Why this matters for the protocols

An OOH impression is **modelled**, not observed. A play on a screen is converted
into an audience figure using a market-specific methodology (panel research,
mobility data, traffic counts, dwell-time modelling, visibility adjustment). Two
sellers can report different impression counts for the same physical exposure
because they use different currencies, methodology versions or visibility
definitions.

An agent comparing offers therefore needs the number **and its provenance**:
currency, methodology version, geography, visibility basis, and whether the figure
is modelled, measured or verified.

## What this document will cover

- [ ] The concepts: plays, contacts/OTS, reach, frequency, visibility-adjusted contacts
- [ ] Per-market currencies and their methodologies (US, UK, DE, FR, CA, ... )
- [ ] How the impression multiplier is derived and at what granularity
- [ ] Modelled vs measured vs verified delivery — and how each should be labelled
- [ ] Existing standardisation efforts we should align with rather than duplicate
- [ ] The minimum provenance metadata a protocol must carry alongside any OOH
      audience figure

## Open questions

- Does an agentic protocol need to make currencies *comparable*, or only
  *self-describing*? (Self-describing is achievable; comparable may not be.)
- Where should provenance live — on the product, on the delivery report, or both?
