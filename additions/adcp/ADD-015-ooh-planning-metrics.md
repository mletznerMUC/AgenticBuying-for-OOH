---
id: ADD-015
title: OOH Planning Metrics in Briefs and Offers
version: 0.2.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §9 (Plan DooH)"
targets:
  adcp: [media-buy, signals]
  aamp: [agentic-direct, agentic-audiences]
applies_to: [io, programmatic]
target_revision_checked: 2026-08-27
protocol_ownership:
  owner: adcp
  secondary: [aamp]
upstream_status: partial
verified_against:
  adcp: 3.2.0-beta.8
  aamp: "agentic-direct/OpenDirect-2.1; ARTF/OpenRTB-2.6"
  date: 2026-08-27
---

# ADD-015 — OOH Planning Metrics in Briefs and Offers

> Version 0.2.0 · Status: `draft` · Since `R1.0`
>
> **Protocol owner: AdCP** · also binds into AAMP
>
> 🟡 **Verified partially exists upstream** against AdCP 3.2.0-beta.8 and AAMP (OpenDirect 2.1 / OpenRTB 2.6) on 2026-08-27.

## Verification

`flat-rate-option.DoohParameters` already carries `sov_percentage`, `loop_duration_seconds` and `min_plays_per_hour`; `cpp-option` covers cost per point. Unmet: planning metrics as **brief targets**, and `unmet_brief_targets` on an offer.

Full evidence: [`../verification/verdicts.md`](../../verification/verdicts.md) · [`../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) · [`../verification/aamp.md`](../../verification/aamp.md)


## Problem

Ströer tells buyers to plan in OOH terms: "Apply ooH planning tactics in order to
generate a meaningful advertising pressure (**Share of Voice, OTP, GRP, Dwell time**).
In case of small budgets focus on location targeting."

Not one of those four metrics is expressible in any programmatic field. The planning
vocabulary and the transaction vocabulary are completely disjoint. A buyer sets a CPM
and a budget; the seller advises them to think about share of voice and advertising
pressure; nothing connects the two.

This is the single largest gap for agentic buying, because **a brief is written in
planning terms**. A buyer agent given "achieve 30% SOV against commuters in the top
five German cities for two weeks" has no way to express that as a request, and no way to
evaluate whether an offer satisfies it. It can only translate down to a budget and a
CPM and hope — losing exactly the intent that made the brief a brief.

It also interacts with **ADD-012**: loop separation caps achievable SOV, so an SOV
target may be structurally undeliverable on some inventory. Neither the target nor the
cap is currently expressible.

## Semantic definition

1. A brief MUST be able to state OOH planning objectives as first-class targets, at
   minimum:
   - **share of voice** — share of loop slots or loop time, with the basis stated
     (slots or time) and the scope (loop, screen, network, campaign);
   - **gross rating points** — with the target-group definition and the market currency
     they are computed against;
   - **opportunity to see / opportunity to perceive** — with the visibility basis;
   - **average frequency** and **reach**, with the population base;
   - **dwell time**, where the venue makes it meaningful.
2. Every metric MUST carry its **basis and provenance**: which currency, which
   methodology version, which population, which geography. Unqualified metrics are not
   comparable and MUST NOT be treated as such.
3. An offer MUST be able to respond in the same metrics, as forecasts, so that a buyer
   agent can evaluate fit mechanically.
4. A seller MUST declare which metrics it can forecast and which it can report
   post-campaign. These sets differ, and the difference is material to a brief that
   asks for guaranteed outcomes.
5. Where a structural constraint caps a metric — advertiser separation limiting SOV
   (**ADD-012**), loop capacity limiting frequency — the offer MUST surface the cap
   rather than silently under-delivering.
6. Delivery reporting SHOULD report achieved values for the metrics the offer forecast,
   on the same basis, so that plan and outcome are comparable.
7. These metrics are **planning** quantities. They MUST NOT be conflated with the
   settlement basis in **ADD-001**: a campaign may be planned on SOV and billed on
   audience impressions, and both must be expressible at once.

## Programmatic binding

**Today (Ströer):** absent. The transport carries CPM, floor price, and audience
impressions. Planning metrics appear only as advice in a best-practice section, with the
suggestion to request a "DooH checklist" from a DSP representative.

**Proposed:** planning metrics do not belong in the bid request. Their programmatic
relevance is indirect: an SOV commitment constrains how the seller schedules, and a
share-of-voice target is a pacing input rather than a bid parameter. The `applies_to`
ordering for this addition is deliberately `[io, programmatic]` — the offer layer is
primary here.

## Offer / IO binding

This is the addition's real home, and it is what makes a brief answerable.

A brief MUST be able to say: 30% share of voice, by loop time, on station and mall
networks, in these five cities, for these two weeks, against a commuter target group.

An offer MUST be able to answer: here is the inventory, here is the forecast SOV we can
guarantee, here is the cap that prevents more, here are the forecast GRPs against that
target group on this currency, and here is what we will report afterwards.

Sketch — brief side:

```json
{
  "planning_targets": [
    { "metric": "share_of_voice", "basis": "loop_time", "scope": "network",
      "value": 0.30, "type": "minimum" },
    { "metric": "grp", "value": 120, "type": "minimum",
      "target_group": "<definition>", "currency": "<market currency>" }
  ]
}
```

Offer side:

```json
{
  "planning_forecast": [
    { "metric": "share_of_voice", "basis": "loop_time", "scope": "network",
      "value": 0.25, "guaranteed": true,
      "capped_by": { "ref": "ADD-012", "reason": "advertiser_separation" } },
    { "metric": "grp", "value": 118, "guaranteed": false,
      "provenance": { "currency": "<name>", "version": "<version>",
                      "target_group": "<definition>", "geography": "DE" } }
  ],
  "reportable_post_campaign": ["share_of_voice", "audience_impressions"]
}
```

That `capped_by` link is the payoff: the offer does not merely fall short of the brief,
it says *why*, in a form the agent can act on — by widening the network set, extending
the period, or taking the shortfall to a human.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → brief / RFP | `new-object` | Planning targets with basis and provenance |
| AdCP | Media Buy → product / offer | `new-object` | Planning forecasts, with guarantee flag and cap references |
| AdCP | Media Buy → delivery reporting | `add-field` | Achieved planning metrics on the forecast basis |
| AdCP | Signals | `clarify-semantics` | Target-group definitions against a market currency, not user attributes |
| AAMP | Agentic Direct | `new-object` | Planning metrics as the language of brief → offer |
| AAMP | Agentic Audiences | `add-field` | Currency and target-group provenance for GRP/OTS figures |

## Partial conformance

- MAY support a subset of metrics — most sellers cannot forecast all of them — but MUST
  declare which subset.
- MAY omit `guaranteed` where nothing is guaranteed, provided the default is documented.
- MUST NOT emit a planning metric without its basis and provenance.
- MUST NOT silently return an offer that cannot meet a stated target; the shortfall and
  its cause MUST be expressed.

## Open questions

- [ ] Does "OTP" in the source mean opportunity-to-perceive, or opportunity-to-purchase?
      German OOH practice suggests the former, but it is not defined in the document.
- [ ] Which German currency should GRP be computed against, and how is the target group
      expressed? Ties into
      [`../docs/measurement-currencies.md`](../../docs/measurement-currencies.md).
- [ ] Is SOV by slot count or by time the more common trading basis? Both exist; the
      protocol must carry the basis either way.
- [ ] Should these metrics be OOH-specific, or generalised for all reach-and-frequency
      channels (TV, cinema, audio)? Generalising is more valuable and much harder to get
      accepted.
- [ ] Can an SOV commitment be guaranteed in a biddable environment at all, or only
      under a reserved deal?

## Sources

- `../analysis/stroeer-ppv-baseline.md` §13
- Ströer PPV Implementation Guide v6, §9 (Plan DooH; Request a DooH checklist from your
  DSP rep)
- Ströer PPV Implementation Guide v6, Appendix (audience pre-filtering as a floor-price
  input)

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.2.0 | 2026-08-27 | Verified against AdCP 3.2.0-beta.8 and AAMP; added protocol ownership and upstream status |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 best-practice analysis |
