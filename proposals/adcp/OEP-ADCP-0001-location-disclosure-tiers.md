# OEP-ADCP-0001: Location disclosure tiers

| | |
| --- | --- |
| **Status** | `draft` |
| **Target protocol** | AdCP |
| **Target surface** | Media Buy → product / offer; `core/reporting-capabilities.json` |
| **Target revision** | 3.2.0-beta.8, checked 2026-08-27 |
| **Additions** | [`ADD-005@0.2.0`](../../additions/adcp/ADD-005-location-disclosure-tiers.md) |
| **Requirements** | `R-INV-*`, `R-TGT-*` (pending) |
| **Placement** | **Core**, not `ext.ooh` — see [Why core](#why-core-and-not-an-ooh-extension) |
| **Created** | 2026-08-27 |
| **Upstream issue/PR** | — |

## Summary

Sellers disclose *where* their inventory is at different levels of precision, and the
level is a commercial term: buyers pay more for more. AdCP has no way to declare that
level, so a buyer agent cannot tell, before transacting, whether an offer can satisfy a
brief's geographic targeting — or discover afterwards that the reporting it needs was
never included.

This proposal adds a `location_disclosure` declaration to products and offers: an
explicit tier, the manifest of location attributes it provides and withholds, and the
reporting granularity that follows.

## Motivation

In DOOH this is not an edge case, it is the standard commercial model. Ströer's
production integration sells three tiers, and the tier changes the shape of the data
the buyer receives:

| Tier | What the buyer gets |
| --- | --- |
| `transparent` | Site name, city and network, plus latitude/longitude and further geo fields |
| `semi-transparent` | City and network only |
| `intransparent` | Network name only |

The tier is priced — the floor price is "customized based on transparency level,
audience pre-filtering and estimated budget" — and it is fixed in the insertion order,
before any bid request exists.

Two failures follow for an agentic buyer:

1. **The tier is inferred, not declared.** Today it is encoded as *the presence or
   absence of fields*, and as how many hyphen-separated segments a synthetic hostname
   happens to have (`duesseldorfhbf-duesseldorf-sv.de`). A buyer agent has to
   reverse-engineer its own entitlement from the data it receives.
2. **A brief cannot be matched to an offer.** A brief saying "within 500 m of these 40
   stores" is unsatisfiable at `semi_transparent`, but nothing in an offer says so. The
   agent accepts, and discovers the mismatch after the campaign.

The same pattern exists outside OOH — publisher-transparency tiers in display and
audio, site-list masking in curated deals — but OOH is where it is most explicitly
priced and most consequential.

## Current behaviour

AdCP 3.2 has the ingredients but not the declaration.

| What exists | Where | Why insufficient |
| --- | --- | --- |
| `publisher_properties` on products | `core/product.json` | Lists properties when disclosed; nothing says disclosure is *limited*, or to what degree |
| `property_targeting_allowed` (boolean) | `core/product.json` | Says whether a buyer may *select* a subset. Orthogonal to how precisely properties are *described* |
| A whole `property/` domain — property lists, features, filters | `static/schemas/source/property/` | Models properties richly; assumes they are disclosed |
| `targeting_resolution` | `core/product-targeting-resolution.json` | Discloses how the seller resolved the brief's targeting, not what location fidelity the buyer is entitled to |
| `supports_geo_breakdown`, `supports_placement_breakdown` | `core/reporting-capabilities.json` | Booleans per dimension, unconnected to a disclosure tier — a seller can claim geo breakdown while withholding coordinates |
| `enums/geo-level.json` | | Names geographic levels; does not bind them to an entitlement |

**Nothing ties disclosure fidelity to price, to targeting feasibility, or to reporting
granularity.** There is no negotiated tier and no attribute manifest. Verified absent
from AAMP too ([`../../verification/aamp.md`](../../verification/aamp.md)).

## Proposal

**Change type:** `new-object` plus one `add-field` on reporting capabilities.

Add `location_disclosure` to the product/offer object.

### Schema

```json
{
  "$id": "/schemas/core/location-disclosure.json",
  "title": "Location Disclosure",
  "description": "Declares how precisely the seller discloses the physical or logical location of the inventory in this product, and the reporting granularity that follows. Absent means fully disclosed.",
  "type": "object",
  "properties": {
    "tier": {
      "type": "string",
      "description": "Seller-named tier. The attribute manifest is normative; the name is a label for negotiation."
    },
    "attributes_provided": {
      "type": "array",
      "items": { "$ref": "/schemas/enums/location-attribute.json" }
    },
    "attributes_withheld": {
      "type": "array",
      "items": { "$ref": "/schemas/enums/location-attribute.json" }
    },
    "property_level_reporting": {
      "type": "boolean",
      "description": "Whether delivery can be reported per property (screen, panel, site). Constrained by this tier."
    },
    "upgrade_available": {
      "type": "array",
      "description": "Higher tiers the seller will negotiate, and their price effect if published.",
      "items": {
        "type": "object",
        "properties": {
          "tier": { "type": "string" },
          "attributes_provided": { "type": "array", "items": { "$ref": "/schemas/enums/location-attribute.json" } },
          "price_effect": { "type": "string", "enum": ["floor_uplift", "fixed_uplift", "negotiable", "undisclosed"] }
        }
      }
    }
  },
  "required": ["attributes_provided"],
  "additionalProperties": false
}
```

New enum `/schemas/enums/location-attribute.json`:

`coordinates`, `street_address`, `postal_code`, `property_name`, `property_id`,
`city`, `region`, `country`, `venue_type`, `network`, `timezone`.

### Field reference

| Field | Required | Description |
| --- | :-: | --- |
| `tier` | no | Seller's label for the tier. Free-form because tier vocabularies differ by market; the manifest is what interoperates. |
| `attributes_provided` | **yes** | Exactly what the buyer will receive. A tier name alone is not interoperable. |
| `attributes_withheld` | no | Explicit is better than inferred, but derivable from the enum minus `attributes_provided`. |
| `property_level_reporting` | no | Defaults false when a tier withholds `property_id`. Prevents the contradiction of geo breakdown over undisclosed properties. |
| `upgrade_available[]` | no | Lets an agent evaluate the trade-off instead of negotiating out of band. |

### Normative rules

1. A withheld attribute MUST be **absent**, never approximated, fuzzed or filled with a
   placeholder. A buyer agent MUST be able to distinguish *not disclosed* from
   *unknown* from *zero*.
2. Location MUST be conveyed in fields whose declared purpose is location. It MUST NOT
   be encoded in a hostname, path or other identifier.
3. `reporting_capabilities.supports_geo_breakdown` and `supports_placement_breakdown`
   MUST NOT contradict this manifest. Where they do, `location_disclosure` wins.
4. A brief SHOULD be able to state a minimum required tier via its attribute manifest;
   an offer that cannot meet it SHOULD say so rather than returning silently.

Rule 4 depends on [OEP-ADCP-0006](README.md) for the unmet-target mechanism; this
proposal stands without it.

## Examples

A German transit and mall DOOH offer at the middle tier:

```json
{
  "product_id": "ppv-station-mall-de",
  "channels": ["dooh"],
  "location_disclosure": {
    "tier": "semi_transparent",
    "attributes_provided": ["city", "region", "country", "venue_type", "network", "timezone"],
    "attributes_withheld": ["coordinates", "street_address", "property_name", "property_id"],
    "property_level_reporting": false,
    "upgrade_available": [{
      "tier": "transparent",
      "attributes_provided": ["coordinates", "property_name", "property_id", "city",
                              "region", "country", "venue_type", "network", "timezone"],
      "price_effect": "floor_uplift"
    }]
  }
}
```

A buyer agent holding a brief that requires 500 m store proximity can now determine
mechanically that this offer cannot satisfy it, that an upgrade exists, and that the
upgrade raises the floor — and put that trade-off to a human instead of guessing.

## Why core and not an OOH extension

AdCP's `ext.{namespace}` mechanism would accept this, but it belongs in core:

- The problem is not OOH-specific. Curated display deals, audio site-list masking and
  publisher-anonymised inventory all withhold location or identity commercially.
- It must interact with core objects that an extension cannot constrain —
  `reporting_capabilities` and `property_targeting_allowed` in particular. Rule 3 is
  unenforceable from a namespace.
- `attributes_provided` is the kind of self-description the `property/` domain already
  aims at; putting it in an extension splits one concept across two places.

OOH-only attribute values, if any emerge, can still be added under `ext.ooh`.

## Alternatives considered

| Alternative | Why not |
| --- | --- |
| **Do nothing** — let buyers infer the tier from received fields | This is today's behaviour and it is the defect. Inference requires string surgery on synthetic hostnames, and cannot happen at brief time at all. |
| Reuse `property_targeting_allowed` | Different question: whether a buyer may *select* properties, not how precisely they are *described*. A product can allow targeting over properties it describes vaguely. |
| A closed tier enum (`transparent`/`semi_transparent`/`intransparent`) | Comparable across sellers but wrong: tier vocabularies differ by market and media owner, and a fixed enum would force sellers to mislabel. Free-form name plus a normative manifest gets comparability without the lie. |
| Express it only in `reporting_capabilities` | Covers reporting but not targeting feasibility, and does not exist at brief time. |
| An `ext.ooh` namespace | See above. |

## Compatibility

- **Fully backwards compatible.** The field is optional; absent means fully disclosed,
  which is today's implicit behaviour.
- A buyer that ignores it behaves exactly as now.
- A seller that adopts it makes an existing commercial term explicit; it changes no
  pricing and no delivery.
- Rule 3 could surface pre-existing contradictions in sellers' declared reporting
  capabilities. That is the point, and it is caught at declaration time rather than
  after a campaign.

## Market applicability

The three-tier structure is evidenced in **Germany** (Ströer Public Video). Tiering
itself is near-universal in OOH but the cut points differ by market, which is precisely
why the tier name is free-form and the manifest is normative. **Not yet verified
against a second media owner or market** — see
[`../../verification/README.md`](../../verification/README.md).

## Privacy and compliance

None. OOH is non-addressable; this concerns disclosure of *inventory* location, not
people. It has a mild privacy benefit: a seller withholding precise screen coordinates
must now do so explicitly rather than by silently omitting fields.

## Open questions

- [ ] Should `attributes_provided` be per-property rather than per-product? A product
      may mix disclosure levels across networks.
- [ ] Does the `property/` domain's `property-feature` mechanism
      (`feature_id`/`value`/`source`) subsume the manifest? It is close, and reusing it
      would be cleaner if features can be declared as *absent by policy*.
- [ ] Should `price_effect` carry an amount when the seller is willing to publish one?
- [ ] Is a minimum-tier constraint better expressed in the brief or as a filter on
      `get_products`?
