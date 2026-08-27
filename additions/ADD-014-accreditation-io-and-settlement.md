---
id: ADD-014
title: Accreditation, Insertion Order and Settlement
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "v6 Appendix (Public Video Private Auction step-by-step); DSP Integration"
targets:
  adcp: [accounts-and-governance, media-buy]
  aamp: [agentic-direct, agent-sdks-and-registry]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-014 — Accreditation, Insertion Order and Settlement

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

This is the addition that most changes how an agentic protocol should think about OOH.

**Programmatic DOOH sits inside a paper contract.** Ströer states it plainly: "Any deal
is contingent upon the issuance of an initial IO (Insertion Order) by Ströer Digital
Media (SDM) through Ströer sales." Buying pDOOH "requires a framework insertion order",
issued by a sales team, reached by e-mailing a named address to find the representative
for your agency or vertical.

The full sequence before a single bid request arrives:

1. **Accreditation** — billing registration, creative compliance declaration
   (**ADD-011**), instruction on dynamic creative rules (**ADD-010**).
2. **Contract** — Ströer SSP contract, an amendment, or registration as a Nautilus
   debtor if the buyer is DOOH-only.
3. **Insertion order** — framework IO issued by sales. The floor price is derived from
   the Public Video price list plus upgrades, and is "customized based on transparency
   level, audience pre-filtering and estimated budget" (see **ADD-005**).
4. **Deal setup** — seat setup and technical test, deal creation, creative approval,
   deal monitoring.
5. **Settlement** — invoices issued from Ströer SSP transactional data within three
   business days of month end, to the client, the agency, or the DSP on prior request.

Any model that treats pDOOH as self-serve is simply wrong about this market. And the
consequence for agentic buying is direct: a buyer agent that sends a brief to a seller
it has no IO with cannot receive a transactable offer at all. It needs to know that, and
know what to do about it, rather than producing a plan that dies at booking.

## Semantic definition

1. A seller MUST be able to declare its **commercial onboarding requirements** as
   structured prerequisites: accreditation, contract, order, billing registration, seat
   setup.
2. Each prerequisite MUST declare its **status for the requesting buyer**, its lead
   time, and how it is obtained.
3. Where an **order** (IO) is a precondition for transacting, it MUST be a
   protocol-visible object with an identifier, parties, validity period, and the terms
   it fixes.
4. Terms an order fixes MUST be enumerable, and MUST include at minimum: the pricing
   basis and floor, the disclosure tier (**ADD-005**), any audience pre-filtering, and
   the settlement terms. These are exactly the terms that determine what an offer
   *means*, so a buyer agent must be able to read them.
5. A seller MUST declare the **settlement model**: the billing entity, the invoicing
   cadence, the data source that settlement is computed from, and the permitted invoice
   recipients.
6. Where the invoice recipient is elective (buyer, agency or DSP), the seller MUST
   declare when the election must be made. Ströer's must be made before deal start,
   which an agent cannot infer.
7. The order MUST be able to express its relationship to executions under it: a
   framework order covering many deals, or an order per campaign.
8. A buyer agent MUST be able to determine, before briefing, whether it can transact
   with a seller at all — and if not, what is missing and how long it takes to obtain.

## Programmatic binding

**Today (Ströer):** none. Every element is out of band — e-mail, contracts, sales
representatives, a price list. The only trace in the transport is the existence of a
deal ID and a `wseat` entry, which is the *result* of the whole process.

**Proposed:** the programmatic layer does not need to carry the order. It needs to carry
a **reference** to it, so delivery and settlement are attributable, and so a deal can be
traced to the terms that govern it.

## Offer / IO binding

This addition is almost entirely an offer/IO concern, and it is the foundation the other
additions' offer bindings rest on.

From a seller's capability description — before any brief — a buyer agent MUST be able
to determine:

- whether it is already able to transact with this seller;
- if not, exactly which prerequisites are missing and the lead time for each;
- who to route a human-in-the-loop request to;
- what an order would fix, so the agent knows which terms are negotiable at brief time
  and which are already settled;
- the settlement model, so it can reconcile.

Sketch:

```json
{
  "commercial_onboarding": {
    "prerequisites": [
      { "type": "accreditation",        "status_for_buyer": "satisfied" },
      { "type": "framework_contract",   "status_for_buyer": "satisfied" },
      { "type": "insertion_order",      "status_for_buyer": "missing",
        "lead_time": "P10D", "obtained_via": "seller_sales_contact" },
      { "type": "seat_setup",           "status_for_buyer": "missing", "lead_time": "P3D" }
    ],
    "order": {
      "kind": "framework",
      "fixes_terms": ["pricing_basis", "floor_price", "location_disclosure_tier",
                      "audience_prefiltering", "settlement_terms"],
      "covers": "many_deals"
    },
    "settlement": {
      "billing_entity": "<seller billing entity>",
      "invoice_recipient_options": ["advertiser", "agency", "dsp"],
      "recipient_election_deadline": "before_deal_start",
      "cadence": "monthly",
      "issued_within": "P3D_after_month_end",
      "computed_from": "seller_transactional_data"
    }
  }
}
```

The critical field is `status_for_buyer: missing` with a lead time. That is what lets an
agent say to its principal: *I can plan this campaign, but we need an IO with this seller
and it takes about ten days — shall I start that?* — instead of producing a plan that
fails silently at booking.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Accounts | `new-object` | Commercial onboarding prerequisites with buyer-specific status |
| AdCP | Accounts | `new-object` | Order/IO object: parties, validity, fixed terms |
| AdCP | Accounts | `add-field` | Settlement model: entity, cadence, recipient options, data source |
| AdCP | Media Buy → deal | `add-field` | Order reference on the deal |
| AAMP | Agentic Direct | `new-object` | The order as a first-class step in brief → offer → order |
| AAMP | Registry / Seller Agent | `add-field` | Onboarding prerequisites in the seller's capability description |

## Partial conformance

- MAY omit `obtained_via` where a seller does not wish to publish a routing contact.
- MAY omit `order.fixes_terms` detail where terms are wholly bilateral — but SHOULD NOT,
  since these terms determine what an offer means.
- MUST NOT omit `status_for_buyer` on prerequisites. A static list of requirements the
  buyer cannot evaluate against itself is documentation, not protocol.
- MUST NOT present a deal as transactable while a prerequisite is unmet.

## Open questions

- [ ] Does a machine-readable IO exist anywhere today, in any form?
      (`../analysis/open-gaps.md` §3.7)
- [ ] What is the real lead time from first contact to a usable deal ID? The sketch's
      `P10D` is a placeholder and must be replaced with a measured figure.
- [ ] Is "audience pre-filtering" a distinct product feature? It appears once, as a
      floor-price input, and is not described anywhere in the analysed documents. It may
      warrant its own addition.
- [ ] How does the Nautilus debtor registration relate to the SSP contract — an
      alternative, or an additional step for DOOH-only buyers?
- [ ] Should the order object be OOH-specific, or is this a general agentic-commerce gap
      that AAMP's Agentic Direct pillar should own for all channels? Probably the
      latter, which would make this the strongest general contribution in release R1.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §12
- Ströer PPV Implementation Guide v6, Appendix (Public Video Private Auction: 1
  Accreditation, 2 Signing an IO, 3 Receiving a deal ID, 4 Billing & Invoicing)
- DSP Integration Ströer SSP, "Billing Instructions, Forms and Q&A", "Sign framework
  contract or implementation media order"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer accreditation and IO appendix |
