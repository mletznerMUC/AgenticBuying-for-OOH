---
id: ADD-013
title: Deal Access and Guaranteed Response Obligation
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §4, §5, §9"
targets:
  adcp: [media-buy, accounts-and-governance]
  aamp: [artf, agentic-direct]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-013 — Deal Access and Guaranteed Response Obligation

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Ströer Public Video is not openly biddable. "Bids on PPV are only considered for deals
as indicated in the bid request, ie., no open auction bids are considered." Access is
fixed-price deals and private auctions only, and every deal is preceded by
accreditation and an insertion order (**ADD-014**).

Running the other way, programmatic guaranteed carries an obligation **on the buyer**:
"Programmatic Guaranteed buyer must answer every bid request with a valid response."
The seller paces; the buyer's job is to always be there. This inverts the normal
programmatic posture, where a bidder may decline anything for any reason and non-
response is free.

Neither side of this is declared in a way an agent can read:

- The closed-access model appears as `pmp.private_auction: 1` — a flag whose meaning
  ("private auction") does not convey "there is no open path to this inventory at all,
  and you must sign a contract first".
- The must-respond obligation appears only in a best-practice bullet and an onboarding
  test. An agent that treats non-response as free will silently breach the deal.

## Semantic definition

1. Inventory MUST declare its **access model**: `open`, `private_auction`,
   `fixed_price_deal`, `guaranteed`, or a set of these.
2. Where access requires prerequisites — accreditation, declarations (**ADD-011**), a
   signed order (**ADD-014**) — the inventory MUST declare them, and a buyer agent MUST
   be able to check its own eligibility **before** briefing.
3. Where a deal imposes a **response obligation** on the buyer, that obligation MUST be
   declared explicitly, with its consequence for non-compliance.
4. A response obligation MUST be declared together with the pacing owner (**ADD-003**).
   The two are only coherent as a pair: the buyer is required to always respond
   *because* the seller controls delivery volume.
5. Inventory that cannot be reached without a prior contract MUST NOT be presented as
   discoverable-and-transactable. Discovery and transactability are separate
   properties, and a buyer agent must be able to tell them apart.
6. A seller SHOULD declare how a buyer becomes eligible, and the lead time for doing
   so.

## Programmatic binding

**Today (Ströer):**

- `pmp.private_auction: 1` on every request.
- `pmp.deals[].at: 3` (fixed price) with `bidfloor` and `bidfloorcur: EUR`.
- `pmp.deals[].ext.guaranteed: 1` marks a programmatic guaranteed deal.
- `wseat` restricts which seats may bid.
- Request identification, since PPV traffic must be recognised before it can be
  treated correctly: UA always
  `Mozilla/5.0 (PPV; X11; Linux armv7l) AppleWebKit/537.42 ... Safari/537.42`;
  `publisher.id` `17409` production and `17387` sandbox; `imp.ext.totalaud` present
  only on PPV traffic.
- The must-respond obligation exists only in prose and in the onboarding test plan.
- `tmax: 200` ms.

**Proposed:** an access-model declaration with prerequisites, and an explicit
response-obligation field on the deal. Also worth noting: the need for buyers to
*fingerprint* PPV traffic by user-agent string is itself a symptom — inventory should
declare its channel, not be recognised by a browser string that has nothing to do with
a browser.

## Offer / IO binding

From an offer, or before briefing, a buyer agent MUST be able to determine:

- how this inventory can be transacted at all;
- what it must have in place first, and whether it has it;
- whether accepting the deal commits it to responding to every opportunity;
- what happens if it does not;
- who paces, and therefore what it is accountable for.

Sketch:

```json
{
  "access": {
    "models": ["fixed_price_deal", "private_auction"],
    "open_auction": false,
    "prerequisites": [
      { "type": "accreditation", "status_for_buyer": "satisfied" },
      { "type": "declaration", "ref": "youth_protection", "status_for_buyer": "satisfied" },
      { "type": "insertion_order", "status_for_buyer": "required", "lead_time": "P10D" }
    ],
    "response_obligation": {
      "required": true,
      "scope": "every_opportunity",
      "consequence": "deal_underdelivery_attributed_to_buyer"
    },
    "pacing_owner": "seller"
  }
}
```

`prerequisites[].status_for_buyer` turns a static description into something an agent
can act on: it can see that it needs an IO, that it takes ten days, and that it should
therefore raise this with a human now rather than at flight start.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product / offer | `new-object` | Access model with prerequisites and buyer-specific status |
| AdCP | Media Buy → deal | `add-field` | Response obligation and its consequence |
| AdCP | Accounts | `add-field` | Buyer eligibility state per seller |
| AdCP | Media Buy → product discovery | `clarify-semantics` | Discoverable ≠ transactable |
| AAMP | ARTF | `add-field` | Response obligation on the deal; declared channel instead of UA fingerprinting |
| AAMP | Agentic Direct | `add-field` | Prerequisites as gates in brief → offer → order |

## Partial conformance

- MAY omit `lead_time` on prerequisites where it is genuinely variable.
- MAY omit `consequence` where no penalty attaches.
- MUST NOT declare a response obligation without also declaring the pacing owner.
- MUST NOT present inventory as transactable when a contract is a precondition.

## Open questions

- [ ] What is the actual consequence of missing bid requests on a PG deal — attributed
      under-delivery, deal termination, or nothing formal?
- [ ] Is `ext.guaranteed` documented in the DSP adapter spec, or example-only?
      (`../analysis/open-gaps.md` §1)
- [ ] Should "must respond to every opportunity" be modelled as an obligation, or as an
      SLA with a tolerance? A 100% response requirement is unusual and probably has
      practical slack.
- [ ] Does a 200 ms `tmax` interact with the response obligation in a way that needs
      stating?

## Sources

- `../analysis/stroeer-ppv-baseline.md` §11
- Ströer PPV Implementation Guide v6, §4 (Deal-Only Bidding), §5 (Identify PPV bid
  requests), §9 (Note on PG; Fix price deal and private auction only)
- Static Creatives pp. 4–5 (`deals[].ext.guaranteed`)
- DSP Integration Ströer SSP, "Pacing"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
