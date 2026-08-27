---
id: ADD-005
title: Location Disclosure Tiers
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §4 (Location Targeting) and §5"
targets:
  adcp: [media-buy, accounts-and-governance]
  aamp: [artf, agentic-direct]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-005 — Location Disclosure Tiers

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

How precisely a seller reveals where its screens are is a **commercial** decision,
and in Ströer's model it changes the shape of the data the buyer receives:

| Tier | What the buyer gets |
| --- | --- |
| `transparent` | `{sitename}-{city}-{networkid}.de` plus lat/lon and further geo fields |
| `semi-transparent` | `{city}-{networkid}.de` |
| `intransparent` | `{networkname}.de` |

The tier is set commercially — Ströer states the floor price is "customized based on
transparency level, audience pre-filtering and estimated budget". So location fidelity
is something the buyer pays for, and the price and the schema move together.

Two problems follow. First, the tier is encoded as *the presence or absence of
fields*, and as *how many hyphen-separated segments a fake hostname happens to have* —
a buyer agent must reverse-engineer its own entitlement. Second, and worse for
agentic buying: the tier is fixed in the IO, so at brief time an agent cannot know
what fidelity an offer will actually deliver, which means it cannot judge whether the
offer can satisfy the brief's targeting at all.

## Semantic definition

1. A seller MUST declare, as an explicit enumerated value, the **location disclosure
   tier** applying to an offer or deal.
2. The tier MUST be declared **before** the transaction, at brief/offer time, not
   inferred from the data received afterwards.
3. For each tier the seller MUST declare which location attributes are provided:
   coordinates, street address, site name, city, administrative region, country,
   network, venue type.
4. Withheld attributes MUST be **absent**, never approximated, obfuscated or filled
   with placeholder values. A buyer agent MUST be able to distinguish "not disclosed"
   from "unknown" and from "zero".
5. Location MUST be conveyed in fields whose declared purpose is location. It MUST NOT
   be encoded in a hostname or other identifier.
6. Where the tier is priced, the offer SHOULD express the relationship, so that a
   buyer agent can evaluate the trade-off rather than negotiate it out of band.
7. The tier MUST also govern **reporting** granularity, and the seller MUST say so:
   a buyer that cannot see screen locations cannot receive per-screen delivery
   reports either (see **ADD-002**).

## Programmatic binding

**Today (Ströer):**

- `site.domain` and `site.page` carry the synthetic hostname, whose segment count
  implies the tier. Examples: `duesseldorfhbf-duesseldorf-sv.de`,
  `stuttgarthbf-stuttgart-sv.de`, `ekzalstertaleinkaufszentrumhamburg-hamburg-mv.de`.
- `device.geo` on the transparent tier: `lat`, `lon`, `type` (required; defaults to 3,
  "user provided"), `country` (ISO-3166-1-alpha-3, e.g. `DEU`), `region`
  (ISO-3166-2, e.g. `BW`, `HH`), `city` (UN/LOCODE, e.g. `DESTR`, `DEHAM`),
  `utcoffset` (minutes, e.g. `60`, `120`).
- No field names the tier. The buyer infers it.
- Note the `geo.type` problem: a fixed, surveyed screen location is reported as "user
  provided", because OpenRTB has no value meaning "fixed installation".

**Proposed:** an explicit tier declaration on the deal or opportunity, plus location
in real location fields. A new `geo.type` value for a surveyed fixed installation is a
small, clean upstream ask that benefits every DOOH seller.

## Offer / IO binding

This is the binding that matters most for this addition, because the tier is an IO
term today.

From an offer, a buyer agent MUST be able to determine:

- the disclosure tier, by name;
- exactly which location attributes it will receive, per tier;
- whether per-screen reporting is included;
- what a higher tier would cost, where the seller is willing to state it;
- and therefore whether the offer can satisfy a brief that requires, say, targeting
  within 500 m of a set of stores.

Sketch:

```json
{
  "location_disclosure": {
    "tier": "semi_transparent",
    "attributes_provided": ["city", "region", "country", "network", "venue_type"],
    "attributes_withheld": ["coordinates", "site_name", "address"],
    "screen_level_reporting": false,
    "upgrade": { "tier": "transparent", "price_effect": "floor_cpm_uplift" }
  }
}
```

A brief should be able to state a **minimum** required tier. An offer below that
minimum is not a valid response to the brief, and a buyer agent should be able to
determine that mechanically instead of discovering it after the campaign.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product / offer | `new-object` | Disclosure-tier declaration with attribute manifest |
| AdCP | Media Buy → targeting | `clarify-semantics` | A brief may require a minimum tier; geospatial targeting is only meaningful at sufficient tiers |
| AdCP | Media Buy → delivery reporting | `add-field` | Tier governs reporting granularity |
| AdCP | Accounts / Governance | `clarify-semantics` | Tier as a commercial term of the deal |
| AAMP | ARTF | `add-field` | Tier on the opportunity; proper location fields |
| AAMP | Agentic Direct | `add-field` | Tier as a negotiable term in brief → offer → order |
| OpenRTB / AdCOM | `geo.type` | `extend-enum` | A value for a surveyed fixed installation |

## Partial conformance

- MAY omit `upgrade` — sellers are not obliged to publish an upgrade path.
- MAY use seller-specific tier names if they are declared with their attribute
  manifest; the manifest is normative, the name is a label.
- MUST NOT omit `attributes_provided`. A tier name alone is not interoperable.
- MUST NOT approximate a withheld coordinate. Absent, not fuzzed.

## Open questions

- [ ] Is the tier discoverable before a deal exists today, or only from the IO?
      (`../analysis/open-gaps.md` §3.5)
- [ ] Should tiers be a standard enum (three tiers) or free-form with a mandatory
      manifest? The manifest approach is more honest but harder to compare.
- [ ] Do the German tier definitions generalise? Other markets may cut disclosure
      differently.
- [ ] How does the tier interact with **ADD-012** (advertiser loop separation)? A
      buyer that cannot see the screen cannot verify separation either.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §3, §15
- Ströer PPV Implementation Guide v6, §4 (Location Targeting), §5 (Geo object table),
  §9, Appendix (floor price customised by transparency level)
- Code examples, v6 §7.1 and Static Creatives pp. 4–5

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
