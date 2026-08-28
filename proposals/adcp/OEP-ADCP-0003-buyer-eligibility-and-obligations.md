# OEP-ADCP-0003: Buyer eligibility and response obligations

| | |
| --- | --- |
| **Status** | `draft` |
| **Target protocol** | AdCP |
| **Target surface** | Accounts; Media Buy → product / deal; `get_adcp_capabilities` |
| **Target revision** | 3.2.0-beta.8, checked 2026-08-27 |
| **Additions** | [`ADD-013@0.2.0`](../../additions/adcp/ADD-013-deal-access-and-response-obligation.md), residue of [`ADD-014@0.2.0`](../../additions/aamp/ADD-014-accreditation-io-and-settlement.md) |
| **Requirements** | `R-TRD-*`, `R-BOOK-*` (pending) |
| **Placement** | **Core** — this is general agentic commerce, not OOH |
| **Created** | 2026-08-27 |
| **Upstream issue/PR** | — |

## Summary

A buyer agent cannot currently determine whether it is *able to transact with a seller
at all* before it briefs them. Where a signed order, an accreditation or a compliance
declaration is a precondition, the agent discovers this at booking — after producing a
plan that cannot execute.

This proposal adds (a) buyer-specific **prerequisite status** to the seller's
capability response, and (b) a declared **response obligation** on deals that require
the buyer to answer every opportunity.

## Motivation

### Discoverable is not transactable

AdCP models products as discoverable and buyable. In OOH — and in most contracted media
— there is a gate before either.

Ströer states it plainly: *"Any deal is contingent upon the issuance of an initial IO
(Insertion Order) by Ströer Digital Media through Ströer sales."* Before a single bid
request arrives a buyer must complete accreditation (billing registration, a compliance
declaration, dynamic-creative instruction), sign a framework contract or register as a
debtor, obtain a framework IO from a named sales contact, and have a seat configured
and tested.

A buyer agent that sends a brief to a seller it has no IO with will receive an offer it
cannot act on. Worse, the failure is silent and late: the plan looks fine, sign-off
happens, and the booking fails.

What the agent needs is narrow and specific: **"can I transact with you yet, and if
not, what is missing and how long does it take?"** — answerable before briefing, so the
agent can escalate to a human at the point where a human can still act.

### The obligation runs both ways

Programmatic guaranteed inverts the normal posture. Ströer: *"Programmatic Guaranteed
buyer must answer every bid request with a valid response"*, because the **seller**
paces. A bidder treating non-response as free silently breaches the deal.

This exists only in a best-practice bullet and an onboarding test plan. Nothing
declares it, so no agent can honour it.

## Current behaviour

AdCP has strong adjacent machinery and one precisely-shaped hole.

| What exists | Where | Why insufficient |
| --- | --- | --- |
| `allowed_actions[]` on products; `available_actions[]` on buys | `core/product.json`, buy responses | **The right pattern, wrong scope.** Resolves what a buyer may do *to an existing buy*, "against current buy state, account tier, and negotiated terms". Says nothing about whether a buy can be created at all. |
| `action-not-allowed-reason`: `wrong_status`, `not_supported_on_product`, `not_supported_on_buy`, `mode_mismatch` | `enums/action-not-allowed-reason.json` | `not_supported_on_buy` explicitly cites "account tier, **IO terms**, or buy-level override" — AdCP already knows IO terms gate capability, but only *after* a buy exists |
| `delivery_type`; OpenDirect `Product.deliverytype` | `enums/delivery-type.json` | Describes the *deal type* (guaranteed, PMP, open) — not the prerequisites to reach one |
| Accounts domain: `sync_accounts`, `list_accounts`, `report_usage` | `static/schemas/source/account/` | Manages accounts that already exist. No eligibility state per seller |
| `commercial-terms` with `invoice_recipient`, `purchase_order_ref`, `cancellation_terms` | `media-buy/commercial-terms.json` | Excellent for terms *of a proposal*; presupposes a relationship |
| `authorization-result.json` | `property/` | Property authorisation (does this seller represent this property), not buyer eligibility |
| OpenDirect `Order`, `Line`, `Account`, `ChangeRequest`, `reservedexpirydate` | AAMP Agentic Direct | The order object exists. Nothing exposes whether *this buyer* has one |
| `pacing` enum; `bidding-policy` | `enums/pacing.json`, `core/bidding-policy.json` | Configures pacing; does not say **who owns it**, nor impose a buyer-side response obligation |

**Verified absent from both protocols**: buyer-specific prerequisite status, and any
declared response obligation.

## Proposal

Two independent, small additions.

### Part A — prerequisite status

Add `transaction_prerequisites` to the seller capability response
(`get_adcp_capabilities`), resolved **for the requesting account**.

```json
{
  "$id": "/schemas/core/transaction-prerequisites.json",
  "title": "Transaction Prerequisites",
  "description": "What the requesting buyer must have in place before it can transact with this seller, and whether it has it. Resolved per requesting account.",
  "type": "object",
  "properties": {
    "eligible": {
      "type": "boolean",
      "description": "Whether the requesting buyer can transact today. False when any prerequisite is unmet."
    },
    "prerequisites": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "type": "string",
            "enum": ["accreditation", "framework_contract", "insertion_order",
                     "billing_registration", "seat_setup", "declaration",
                     "certification", "credit_approval"]
          },
          "ref": { "type": "string", "description": "Identifier of the specific requirement, e.g. a declaration id" },
          "status": {
            "type": "string",
            "enum": ["satisfied", "pending", "missing", "expired", "unknown"]
          },
          "valid_until": { "type": "string", "format": "date-time" },
          "typical_lead_time": { "type": "string", "description": "ISO 8601 duration" },
          "lead_time_basis": { "type": "string", "enum": ["calendar_days", "business_days"] },
          "obtained_via": {
            "type": "string",
            "enum": ["seller_sales_contact", "self_service", "seller_operations", "third_party"]
          },
          "contact_uri": { "type": "string", "format": "uri" }
        },
        "required": ["type", "status"]
      }
    }
  },
  "required": ["eligible"],
  "additionalProperties": false
}
```

`lead_time_basis` is load-bearing. A three-**business**-day lead time requested on a
Thursday lands on the following Tuesday; an agent treating it as 72 hours promises a
start date the seller cannot honour.

Products MAY additionally reference the prerequisite types they require, so a buyer can
filter discovery to inventory it is eligible for.

### Part B — response obligation

Add to the deal object:

```json
{
  "response_obligation": {
    "type": "object",
    "properties": {
      "required": { "type": "boolean" },
      "scope": { "type": "string", "enum": ["every_opportunity", "sampled", "none"] },
      "consequence": {
        "type": "string",
        "enum": ["none", "underdelivery_attributed_to_buyer", "deal_suspension", "contractual"]
      }
    },
    "required": ["required"]
  },
  "pacing_owner": { "type": "string", "enum": ["seller", "buyer", "shared"] }
}
```

**`pacing_owner` and `response_obligation` MUST be declared together.** They are only
coherent as a pair: the buyer is required to always respond *because* the seller
controls delivery volume. Declaring an obligation without naming the pacing owner
leaves both sides pacing independently, which is how budgets get overspent.

### Normative rules

1. A seller MUST NOT present a product as transactable while a prerequisite is unmet
   for the requesting buyer. It MAY still present it as discoverable, with `eligible:
   false`.
2. `status` MUST be resolved for the requesting account. A static list of requirements
   the buyer cannot evaluate against itself is documentation, not protocol.
3. A seller declaring `response_obligation.required: true` MUST also declare
   `pacing_owner`.
4. Where a prerequisite requires a human (a sales contact, a signature), the seller
   SHOULD provide `contact_uri` so an agent can route the escalation rather than
   stalling.

## Examples

An accredited buyer with no IO yet:

```json
{
  "transaction_prerequisites": {
    "eligible": false,
    "prerequisites": [
      { "type": "accreditation",        "status": "satisfied" },
      { "type": "framework_contract",   "status": "satisfied" },
      { "type": "declaration", "ref": "youth_protection", "status": "satisfied",
        "valid_until": "2027-03-31T00:00:00Z" },
      { "type": "insertion_order",      "status": "missing",
        "typical_lead_time": "P10D", "lead_time_basis": "business_days",
        "obtained_via": "seller_sales_contact",
        "contact_uri": "mailto:dooh-deals@example.com" },
      { "type": "seat_setup",           "status": "missing",
        "typical_lead_time": "P3D", "lead_time_basis": "business_days",
        "obtained_via": "seller_operations" }
    ]
  }
}
```

The agent can now tell its principal: *I can plan this, but we need an IO with this
seller — about ten business days, via their sales contact. Shall I start that now?*
Today that conversation happens after the plan is signed off.

A programmatic guaranteed deal:

```json
{
  "deal_id": "ppv-pg-q4",
  "pacing_owner": "seller",
  "response_obligation": {
    "required": true,
    "scope": "every_opportunity",
    "consequence": "underdelivery_attributed_to_buyer"
  }
}
```

## Why core and not an OOH extension

This is the least OOH-specific proposal in the set. Accreditation gates, framework
orders, credit approval and seat setup precede transacting in TV, cinema, print, audio
and most contracted digital. AdCP's own `action-not-allowed-reason` already references
"IO terms".

OOH is simply where the gate is unavoidable — Ströer gates *programmatic* on a paper
IO — which makes it good evidence for a general improvement.

## Alternatives considered

| Alternative | Why not |
| --- | --- |
| **Do nothing** | Plans fail at booking. The failure is silent, late, and lands on a human with no time left. |
| Extend `allowed_actions[]` to cover buy creation | Closest existing pattern, and worth considering. But `allowed_actions` is product-scoped and buy-lifecycle-shaped; eligibility is account-and-seller-scoped and precedes any product. Conflating them makes both harder to reason about. |
| Return an error at `create_media_buy` | Already what happens. Errors at commit time are exactly the wrong moment: the agent has done the work and a human has approved it. |
| Put prerequisites on each product | Duplicated across every product, and does not answer the buyer-specific question — the interesting part is `status`, not the list. |
| Model the obligation as an SLA with a tolerance | Possibly more honest than a 100 % requirement — see open questions. Deferred: declare the obligation first, refine to a tolerance if sellers report one. |
| An `ext.ooh` namespace | Would hide a general gap inside a channel extension. |

## Compatibility

- **Fully backwards compatible.** Both parts optional; absent means today's behaviour
  (assume eligible, no declared obligation).
- Part A adds a field to a capability response buyers already call.
- Part B is additive on deals; a bidder ignoring it behaves as now, which is the
  current — undeclared — risk.
- Rule 1 codifies existing seller behaviour rather than changing it.

## Market applicability

Evidenced in **Germany** (Ströer, DOOH). The accreditation-and-IO gate is asserted to be
general across contracted media, **but not verified against a second seller or
market**. The prerequisite `type` enum is drawn from one integration and will likely
need extending; it is deliberately a closed enum so gaps surface as proposals rather
than as free-text drift.

## Privacy and compliance

`transaction_prerequisites` is resolved per requesting account, so a seller must
identify the requester — which it already does for authenticated capability calls. It
exposes **the buyer's own** standing to the buyer, and no third-party data. Sellers
SHOULD NOT include the identity of the human contacts behind `obtained_via` beyond a
role-based `contact_uri`.

## Open questions

- [ ] Is a 100 % response requirement real, or does it have practical slack? Ströer
      states it absolutely; the consequence is undocumented
      ([`../../analysis/open-gaps.md`](../../analysis/open-gaps.md)).
- [ ] Should `eligible` be per-product rather than per-seller? A seller may gate premium
      inventory more strictly.
- [ ] Should this live on `get_adcp_capabilities` or a dedicated task? Capabilities is
      already the pre-transaction call, which argues for it.
- [ ] How does this interact with AAMP's registry-agent discovery? **Unverified** — that
      repository was not examined.
- [ ] Should `declaration` prerequisites link to the compliance machinery
      (`enforced_policies`, `attestation-claim`) rather than being a bare `ref`? Likely
      yes; depends on [ADD-011](../../additions/adcp/ADD-011-compliance-declarations.md).
