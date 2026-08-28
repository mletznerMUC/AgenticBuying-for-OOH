---
id: ADD-001
title: Total Audience Impressions
version: 0.2.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §3 and §4"
targets:
  adcp: [media-buy, signals]
  aamp: [artf, agentic-audiences]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
protocol_ownership:
  owner: aamp
  secondary: [adcp]
upstream_status: exists
verified_against:
  adcp: 3.2.0-beta.8
  aamp: "agentic-direct/OpenDirect-2.1; ARTF/OpenRTB-2.6"
  date: 2026-08-27
---

# ADD-001 — Total Audience Impressions

> Version 0.2.0 · Status: `draft` · Since `R1.0`
>
> **Protocol owner: AAMP** · also binds into AdCP
>
> 🟢 **Verified exists upstream** against AdCP 3.2.0-beta.8 and AAMP (OpenDirect 2.1 / OpenRTB 2.6) on 2026-08-27.

## Verification

OpenRTB 2.6 `Imp.Qty` already carries the fractional multiplier, source type and measurement vendor. Ströer's `imp.ext.totalaud` is a pre-2.6 workaround. Ask becomes migration guidance plus settled-figure provenance.

Full evidence: [`../verification/verdicts.md`](../../verification/verdicts.md) · [`../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) · [`../verification/aamp.md`](../../verification/aamp.md)


## Problem

An OOH play is seen by many people. The number of people is **modelled**, it is
**fractional**, and it is **not known when the transaction is agreed** — it is
restated after the play happens, and that restated figure is what the buyer pays on.

No standard field expresses any part of that. Ströer had to add an extension object
for the forecast, a substitution macro for the confirmed figure, and a formula in
prose for the DSP to compute the amount payable. A buyer agent reading a bid request
sees `imp.ext.totalaud: 118.63105` with no indication that this is a forecast, what
methodology produced it, or how far the settled figure may move from it.

At brief time, none of it is discoverable at all.

## Semantic definition

An **audience impression** is one modelled opportunity-to-see by one person. A
**play** is one execution of a creative on one screen.

1. A play MUST be associated with an audience-impression count. That count MAY be
   fractional — it is a model output, not a tally of events.
2. Two distinct values exist and MUST be distinguishable:
   - the **forecast** audience impressions, available before the play, used for
     bidding, planning and pacing;
   - the **confirmed** audience impressions, available only after the play, used for
     billing and reporting.
3. The confirmed value MAY differ from the forecast. A seller MUST state the basis of
   the forecast and SHOULD state the expected variance.
4. Monetary settlement is computed on the confirmed value:
   `amount = confirmed_audience_impressions × price_per_mille ÷ 1000`.
5. Every audience-impression figure MUST carry provenance: the measurement
   methodology, its version, and whether the figure is modelled, measured or
   independently verified. A bare number is not conformant.
6. A buyer agent MUST NOT assume that an audience impression is comparable to a
   digital served impression, nor that figures from two sellers are comparable
   without matching provenance.

Requirement 5 is the substantive addition beyond Ströer's implementation, which
supplies the number but not its basis.

## Programmatic binding

**Today (Ströer):**

- `imp[].ext.totalaud` — float, "the total number of viewers in the audience".
  Forecast, present only on PPV traffic (also serves as a traffic-identification
  signal).
- `${TOTAL_IMP}` — substitution macro, "replaced with a rational number of the actual
  Total Audience Impressions when the creative is played, thus confirming the billing
  impression". For video creatives it MUST be placed in the VAST impression tracking
  URL, **not** in the `nURL`. For the banner path it goes in
  `bid.ext.imptrackers`, alongside `${AUCTION_PRICE}`.
- Settlement is computed DSP-side as `(${TOTAL_IMP} × ${AUCTION_PRICE}) ÷ 1000`.
- The DSP is required to surface Total Audience Impressions on all user-facing
  reports and dashboards, and the buyer sets a CPM on this basis in the DSP UI.

**Proposed:** the forecast belongs on the impression opportunity as a typed object,
not a bare float, carrying value plus provenance. The confirmed figure belongs in the
delivery/settlement record rather than being smuggled through a tracking URL — a
macro works, but it makes the billing basis invisible to anything that is not
rendering a pixel.

## Offer / IO binding

A buyer agent that sends a brief and receives an offer MUST be able to determine,
from the offer alone:

- that the offer is priced on audience impressions, not plays or served impressions;
- the forecast audience impressions for the offered inventory over the offered
  period, and the basis of that forecast;
- the methodology, version and geography behind the figure;
- whether the figure is modelled, measured or verified;
- the expected variance between forecast and settled figures, or an explicit
  statement that none is published;
- the play-to-audience ratio implied, so the agent can sanity-check the offer against
  other sellers (see **ADD-002**).

Sketch of the offer-side shape:

```json
{
  "pricing_basis": "audience_impressions",
  "audience_impressions": {
    "value": 4820000,
    "kind": "forecast",
    "fractional": true,
    "provenance": {
      "methodology": "<currency or model name>",
      "version": "<version>",
      "geography": "DE",
      "basis": "modelled",
      "expected_variance_pct": null
    }
  }
}
```

This is the same object as the programmatic binding's forecast, at a different
aggregation level — which is the intended outcome: one definition, two altitudes.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product / offer | `new-object` | Audience-impression object with provenance, as the pricing basis |
| AdCP | Media Buy → delivery reporting | `add-field` | Confirmed audience impressions, separate from plays (see **ADD-002**) |
| AdCP | Media Buy → pricing model | `extend-enum` | `audience_impression_cpm` as a distinct basis from `cpm` |
| AdCP | Signals | `clarify-semantics` | Audience provenance is measurement metadata, not an activatable audience — confirm this is the right home |
| AAMP | ARTF | `add-field` | Forecast audience impressions on the impression opportunity |
| AAMP | Agentic Audiences | `new-object` | Provenance schema for aggregate, ID-free audience figures |
| AAMP | Trust and Transparency | `add-field` | Modelled vs measured vs verified labelling |

## Partial conformance

- MAY omit `expected_variance_pct` if the seller does not publish one — but MUST then
  say so explicitly rather than omitting the field silently.
- MAY omit `version` where the methodology is unversioned.
- MUST NOT omit `basis` (modelled / measured / verified), and MUST NOT emit a bare
  numeric audience figure with no provenance object. That is the whole point of the
  addition.

## Open questions

- [ ] Is `totalaud` a per-play forecast or a screen/daypart average? Changes whether
      this is a prediction or a rate-card figure. (See `../analysis/open-gaps.md` §3.1.)
- [ ] What methodology backs it — "based on geospatial datasets" is not a provenance
      statement. (§3.2)
- [ ] Is the forecast-to-settled variance bounded? The Ströer DSP onboarding plan
      tests for variance but names no tolerance. (§3.3)
- [ ] Should the confirmed figure remain macro-delivered for RTB compatibility, or
      move wholly into a settlement record?
- [ ] Do fractional impressions break any existing AdCP or AAMP field typed as an
      integer? Needs checking against the schemas.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §1, §15
- Ströer PPV Implementation Guide v6, §3 (One to many), §4 (Impression reporting,
  CPM, Impressions)
- Ströer PPV Implementation Guide — Static Creatives, p. 3 (macros in `imptrackers`)
- DSP Integration Ströer SSP, "DOOH Impressions Variance Check"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.2.0 | 2026-08-27 | Verified against AdCP 3.2.0-beta.8 and AAMP; added protocol ownership and upstream status |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
