# OEP-ADCP-0002: Advertiser separation and capacity caps

| | |
| --- | --- |
| **Status** | `draft` |
| **Target protocol** | AdCP |
| **Target surface** | Media Buy → product / offer; `enums/exclusivity.json` |
| **Target revision** | 3.2.0-beta.8, checked 2026-08-27 |
| **Additions** | [`ADD-012@0.2.0`](../../additions/adcp/ADD-012-advertiser-loop-separation.md) |
| **Requirements** | `R-COMP-*` (pending) |
| **Placement** | **Core** — the concept generalises beyond OOH |
| **Created** | 2026-08-27 |
| **Upstream issue/PR** | — |

## Summary

Sellers cap how much of a rotation one advertiser may hold — never twice in a DOOH
loop, one brand per CTV pod, one per cinema reel. The cap bounds achievable share of
voice and frequency, so it determines whether a plan is deliverable. AdCP's
`exclusivity` enum describes whether a *product* is exclusive; it cannot express a
*proportional cap within a rotation*.

This proposal adds a `separation_policy` object declaring the entity basis, scope,
window and resulting capacity cap, plus a distinguishable loss reason.

## Motivation

A DOOH loop is a short repeating sequence of slots on one screen. If the same
advertiser appears twice in a 60-second loop, a passer-by sees the same ad twice in a
minute. Ströer therefore "prevents advertiser from looping on public video screens",
enforced server-side.

The buyer learns of it only obliquely: *"DSP bidder may listen to the `badv` or `bcat`
attribute to refrain from sending bids who can't win."* Generic block lists are being
used to hint at a seller-side rule the buyer cannot read. The rule's basis, scope and
window are never stated.

Two consequences, and the second is the serious one:

1. **A bidding agent sees unexplained losses** it cannot distinguish from price losses,
   so it cannot learn from them.
2. **A planning agent produces undeliverable plans.** If a screen will not sell one
   advertiser more than 25 % of its loop, a plan targeting 30 % share of voice cannot
   be delivered — and today nothing in the offer says so. The shortfall appears as
   under-delivery weeks later.

The same structure exists in CTV pods, audio breaks and cinema reels. OOH is where it
bites hardest because the loop is short and the cap is therefore tight.

## Current behaviour

| What exists | Where | Why insufficient |
| --- | --- | --- |
| `exclusivity`: `none` / `category` / `exclusive` | `enums/exclusivity.json` | **Product-level and binary-ish.** `category` means "only one advertiser per industry category" for the whole product; `exclusive` means sole sponsorship. Neither expresses "you may hold at most 25 % of each loop, and so may three competitors." |
| `frequency-cap-scope` | `enums/frequency-cap-scope.json` | Caps exposure *per person*, a buyer-side control. Separation is a seller-side *inventory* constraint on concurrent advertisers. Different axis. |
| `enforced_policies[]` | `core/product.json` | Registry policy IDs the seller enforces. Could *reference* a separation policy but carries no parameters — a buyer cannot read the cap. |
| `badv` / `bcat` | OpenRTB | Buyer-side block lists, repurposed as a hint. Communicates the effect, never the rule. |

**No capacity cap and no distinguishable separation loss exists in either protocol.**
Verified against AAMP as well.

## Proposal

**Change type:** `new-object`, plus `extend-enum` on loss/rejection reasons.

### Schema

```json
{
  "$id": "/schemas/core/separation-policy.json",
  "title": "Separation Policy",
  "description": "Seller-enforced limit on how much of a rotation, pod or location one advertiser may hold concurrently. Distinct from exclusivity (product-level) and from frequency capping (per-person).",
  "type": "object",
  "properties": {
    "entity_basis": {
      "type": "string",
      "enum": ["advertiser_domain", "brand", "industry_category", "buyer_seat"],
      "description": "What counts as 'the same advertiser' for this rule."
    },
    "scope": {
      "type": "string",
      "enum": ["loop", "pod", "break", "reel", "screen", "property", "venue", "geo_radius"],
      "description": "The unit within which the cap applies. 'loop' is the DOOH rotation; 'pod'/'break'/'reel' are the CTV, audio and cinema analogues."
    },
    "scope_radius_metres": {
      "type": "number",
      "description": "Required when scope is geo_radius."
    },
    "window": {
      "type": "object",
      "properties": {
        "unit": { "type": "string", "enum": ["rotation", "minutes", "hours", "plays"] },
        "count": { "type": "integer", "minimum": 1 }
      },
      "required": ["unit", "count"]
    },
    "max_share": {
      "type": "number",
      "minimum": 0, "maximum": 1,
      "description": "Maximum share of the scope one advertiser may hold, 0.0-1.0. Omit when the rule is absolute rather than proportional."
    },
    "max_occurrences": {
      "type": "integer",
      "minimum": 1,
      "description": "Absolute alternative to max_share, e.g. 1 = never twice within the window."
    },
    "enforcement": {
      "type": "string",
      "enum": ["seller_enforced", "buyer_responsible", "best_effort"]
    },
    "loss_reportable": {
      "type": "boolean",
      "description": "Whether a bid or booking rejected for separation is reported as such, distinguishably from a price loss."
    }
  },
  "required": ["entity_basis", "scope", "enforcement"],
  "additionalProperties": false
}
```

Carried as `separation_policy` (array) on the product/offer — several rules can apply
at once, e.g. never twice per loop *and* at most 25 % of a venue's daily plays.

Also add `lost_to_separation` to the loss/rejection reason vocabulary so a bidding
agent can tell a separation loss from a price loss.

### Normative rules

1. A seller declaring `enforcement: seller_enforced` MUST also declare `entity_basis`
   and `scope`. An unspecified rule is not actionable.
2. Exactly one of `max_share` or `max_occurrences` MUST be present.
3. A separation policy MUST NOT require disclosure of **which other advertisers** hold
   the scope. The rule and its effect on this buyer are disclosable; competitors are
   not.
4. Where `max_share` bounds achievable share of voice, an offer responding to a brief
   with an SOV target SHOULD reference the policy as the cause of any shortfall.

## Examples

German DOOH station and mall networks, never twice in a loop and at most a quarter of
any screen's daily plays:

```json
{
  "product_id": "ppv-station-de",
  "channels": ["dooh"],
  "exclusivity": "none",
  "separation_policy": [
    {
      "entity_basis": "advertiser_domain",
      "scope": "loop",
      "window": { "unit": "rotation", "count": 1 },
      "max_occurrences": 1,
      "enforcement": "seller_enforced",
      "loss_reportable": true
    },
    {
      "entity_basis": "advertiser_domain",
      "scope": "screen",
      "window": { "unit": "hours", "count": 24 },
      "max_share": 0.25,
      "enforcement": "seller_enforced",
      "loss_reportable": true
    }
  ]
}
```

A planning agent holding a 30 % SOV brief can now determine before booking that 25 %
is the ceiling, and say so — rather than discovering a 5-point shortfall in the
post-campaign report.

Non-OOH, same object — one advertiser per CTV pod:

```json
{
  "entity_basis": "industry_category",
  "scope": "pod",
  "window": { "unit": "rotation", "count": 1 },
  "max_occurrences": 1,
  "enforcement": "seller_enforced"
}
```

## Relationship to `exclusivity`

They compose and should both be present:

| | `exclusivity` | `separation_policy` |
| --- | --- | --- |
| Question | Can anyone else buy this product? | How much of a rotation may one advertiser hold? |
| Granularity | Product | Loop / pod / screen / venue |
| Typical value | `none` | "never twice per loop" |
| Buyer effect | Whether the product is available | Whether an SOV target is achievable |

A product with `exclusivity: none` can still carry a strict separation policy — which
is exactly the Ströer case, and is inexpressible today.

## Alternatives considered

| Alternative | Why not |
| --- | --- |
| **Do nothing** | Today's behaviour: undeliverable plans discovered from delivery shortfall, and unexplained bid losses. |
| Extend the `exclusivity` enum with values like `loop_once` | Overloads a product-level enum with rotation-level semantics and cannot carry parameters (which scope? what window? what share?). Enum growth without expressiveness. |
| Use `enforced_policies[]` with a registry policy ID | Viable for *referencing* a rule, but the buyer still cannot read the cap. Could complement this: the policy ID names the rule, `separation_policy` gives its parameters. |
| Express only as a frequency cap | Wrong axis — frequency caps limit exposure per person, this limits concurrent advertisers per inventory unit. |
| An `ext.ooh` namespace | The concept is not OOH-specific (pods, breaks, reels), and it must be readable by generic planning logic. |

## Compatibility

- **Fully backwards compatible.** Optional array; absent means no declared separation,
  today's implicit state.
- Adding `lost_to_separation` to a reason vocabulary is additive; consumers that do not
  recognise it fall back to a generic loss.
- No change to `exclusivity` semantics.
- Sellers already enforcing separation server-side start describing existing behaviour
  rather than changing it.

## Market applicability

Evidenced in **Germany** (Ströer, DOOH). Loop separation is standard OOH practice
across markets, but the specific rule — absolute versus proportional — is unverified
even for Ströer (see [`../../analysis/open-gaps.md`](../../analysis/open-gaps.md) §3.6).
The schema deliberately supports both. Pod and reel analogues are asserted from general
industry practice, **not verified against a CTV or cinema seller**.

## Privacy and compliance

None. Rule 3 exists to keep it that way: the policy discloses the constraint, never the
competitors subject to it.

## Open questions

- [ ] Is Ströer's rule absolute (never twice per loop) or proportional? Unresolved —
      `../../analysis/open-gaps.md` §3.6.
- [ ] Does separation apply across a sync group ([ADD-007](../../additions/adcp/ADD-007-synchronised-multi-screen-delivery.md))
      as one unit or per member?
- [ ] Should `entity_basis: brand` resolve through AdCP's Brand domain rather than a
      bare domain string?
- [ ] Should the reason value be `lost_to_separation` on the bidding side and something
      distinct on the booking side, or one value for both?
- [ ] Should sellers be able to declare a cap they will *negotiate* upward, as
      [OEP-ADCP-0001](OEP-ADCP-0001-location-disclosure-tiers.md) does for disclosure?
