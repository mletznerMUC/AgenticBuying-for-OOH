---
id: ADD-012
title: Advertiser Loop Separation
version: 0.2.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §4"
targets:
  adcp: [accounts-and-governance, media-buy]
  aamp: [artf]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
protocol_ownership:
  owner: adcp
  secondary: [aamp]
upstream_status: gap
verified_against:
  adcp: 3.2.0-beta.8
  aamp: "agentic-direct/OpenDirect-2.1; ARTF/OpenRTB-2.6"
  date: 2026-08-27
---

# ADD-012 — Advertiser Loop Separation

> Version 0.2.0 · Status: `draft` · Since `R1.0`
>
> **Protocol owner: AdCP** · also binds into AAMP
>
> 🔴 **Verified confirmed gap** against AdCP 3.2.0-beta.8 and AAMP (OpenDirect 2.1 / OpenRTB 2.6) on 2026-08-27.

## Verification

**Confirmed absent.** `exclusivity` (`none`/`category`/`exclusive`) is product-level and cannot express a capacity cap within a loop. Blocks ADD-015's SOV targets.

Full evidence: [`../verification/verdicts.md`](../../verification/verdicts.md) · [`../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) · [`../verification/aamp.md`](../../verification/aamp.md)


## Problem

A DOOH loop is a short repeating sequence of slots on one screen. If the same
advertiser appears twice in a 60-second loop, a passer-by sees the same ad twice in a
minute — which devalues the inventory and annoys the audience. Ströer therefore
"prevents advertiser from looping on public video screens", enforced server-side.

The buyer learns about it obliquely: "DSP bidder may listen to the `badv` or `bcat`
attribute to refrain from sending bids who can't win." Standard block lists are being
used to hint at a seller-side separation rule that the buyer cannot see. The rule
itself — its window, its granularity, whether it operates on advertiser domain or
brand or category — is never stated.

For a bidding agent this produces unexplained losses. For a planning agent it is worse:
loop separation caps how much of a screen's capacity one advertiser can buy, which
directly bounds achievable share of voice (**ADD-015**). An agent that plans 40% SOV
against inventory that will not sell one advertiser more than 25% of a loop has
produced an undeliverable plan, and will only find out from delivery shortfall.

## Semantic definition

1. A seller MUST declare whether it enforces **advertiser separation** within a loop or
   a location.
2. The declaration MUST state:
   - the **entity basis** — advertiser domain, brand, category, or buyer seat;
   - the **scope** — loop, screen, sync group, venue, or geographic radius;
   - the **window** — one loop, a time period, or a play count;
   - the resulting **capacity cap** per advertiser, where one exists.
3. Enforcement MUST be distinguishable in outcome. A bid or booking rejected for
   separation MUST be reportable as such, separately from a price loss.
4. A separation rule MUST NOT require disclosure of **who else** is on the loop. The
   rule and its effect on the buyer are disclosable; the identity of competing buyers is
   not.
5. Where separation caps capacity, the cap MUST be discoverable at brief time, since it
   bounds achievable share of voice and frequency.
6. A buyer MAY additionally request **category exclusivity** — a stronger guarantee
   than separation — and a seller MUST be able to declare whether it offers it and on
   what terms.

## Programmatic binding

**Today (Ströer):** enforced silently. Signalled indirectly through `badv` (advertiser
domains) and `bcat` (IAB content categories). The bid response carries `bid.ext.avn`
and `bid.ext.agn` (advertiser and agency domains, on the evidence of the code
examples), which is presumably what the separation logic keys on — but this is
inference, not documentation.

**Proposed:** a separation-policy declaration on the inventory, plus a distinguishable
loss/rejection reason. Neither requires exposing competitors.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- that separation is enforced, on what basis and at what scope;
- the maximum share of a loop, screen or venue one advertiser may hold;
- therefore the maximum achievable share of voice and frequency for the offer;
- whether category exclusivity is purchasable, and at what premium.

Sketch:

```json
{
  "advertiser_separation": {
    "enforced": true,
    "entity_basis": "advertiser_domain",
    "scope": "loop",
    "window": { "unit": "loop", "count": 1 },
    "max_share_per_advertiser": { "scope": "loop", "value": 0.25 },
    "rejection_reportable": true,
    "category_exclusivity": { "offered": true, "terms": "on_request" }
  }
}
```

`max_share_per_advertiser` is the field that makes an OOH plan checkable. It is the
bridge between this addition and **ADD-015**: without it, an SOV target in a brief
cannot be validated against the offer.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product / offer | `new-object` | Separation policy with capacity cap |
| AdCP | Accounts / Governance | `clarify-semantics` | Competitive separation as a seller-side rule, distinct from buyer block lists |
| AdCP | Media Buy → delivery reporting | `add-field` | Separation-attributable shortfall |
| AAMP | ARTF | `extend-enum` | Loss reason: lost to advertiser separation |

## Partial conformance

- MAY omit `max_share_per_advertiser` where the rule is absolute (never twice in a
  loop) rather than proportional.
- MAY omit `category_exclusivity` where it is not offered.
- MUST NOT declare `enforced: true` without stating entity basis and scope — a buyer
  cannot act on an unspecified rule.
- MUST NOT disclose competing advertisers in order to satisfy this addition.

## Open questions

- [ ] What is Ströer's actual rule — never twice per loop, or a proportional cap?
- [ ] Does it key on `adomain`, on `bid.ext.avn`, or on an internal advertiser record?
- [ ] Is there a distinguishable loss code today? (`../analysis/open-gaps.md` §3.6)
- [ ] Does separation apply across a sync group (**ADD-007**) as one unit or per
      member?
- [ ] Is category separation offered in addition to advertiser separation? Ströer
      mentions `bcat` but not a category rule.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §10
- Ströer PPV Implementation Guide v6, §4 (badv / bcat)
- Code example, v6 §7.2 (`bid.ext.avn`, `bid.ext.agn`)

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.2.0 | 2026-08-27 | Verified against AdCP 3.2.0-beta.8 and AAMP; added protocol ownership and upstream status |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
