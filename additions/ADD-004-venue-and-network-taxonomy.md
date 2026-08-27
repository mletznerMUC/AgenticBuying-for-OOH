---
id: ADD-004
title: Venue and Network Taxonomy
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §6; Static Creatives pp. 4-5"
targets:
  adcp: [media-buy, signals]
  aamp: [artf, agent-sdks-and-registry]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-004 — Venue and Network Taxonomy

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Ströer sells twelve distinct DOOH networks — Infoscreen, Station, Mall, Cinema, City,
City Tower, Elevator, Retail, Roadside, Giant Indoor, Giant Outdoor, Scene — each with
different audiences, formats, restrictions and prices. In the bid stream they are
identifiable only as a two- or three-letter code (`inf`, `sv`, `mv`, `cc`, `cs`, `ct`,
`elv`, `ret`, `rss`, `gou`, `gin`, `sce`) **embedded in a synthetic domain name**.

A standard venue-taxonomy ID does exist in the request — `device.ext.dooh.venuetypeid`
— but it lives in a vendor extension on the device object, its taxonomy version is
never stated, and the mapping between Ströer's commercial network names and the
standard venue types is published nowhere.

So a buyer agent has two vocabularies, neither usable: a proprietary code it must
learn by asking a sales rep, and a standard code with no declared version.

The commercial layer makes this worse rather than better. Network membership is what
the buyer actually reasons about — it determines whether static-only rules apply
(**ADD-006**), whether screens come in synchronised pairs (**ADD-007**), and what the
floor price is (**ADD-014**) — and it is precisely the layer with no standard
representation.

## Semantic definition

1. Every unit of OOH inventory MUST declare its **venue type** using a named,
   versioned public taxonomy. The taxonomy name and version MUST both be present; a
   bare numeric ID is not conformant.
2. Inventory MAY additionally declare a **seller network**: the media owner's own
   commercial grouping, with a stable identifier and a human-readable name.
3. Where a seller network is declared, the seller MUST publish its mapping to venue
   types. A network MAY map to several venue types.
4. A seller network identifier MUST be resolvable without parsing any other field. It
   MUST NOT be encoded inside a hostname, path, or other field whose declared purpose
   is something else.
5. Venue type MUST be expressible as a targeting dimension, in both inclusion and
   exclusion form, at brief time and at bid time.
6. A buyer agent MUST be able to enumerate a seller's networks and venue types
   **before** transacting.

Requirements 3, 4 and 6 are the substantive additions: Ströer supplies the codes but
not the mapping, buries the network in a hostname, and offers no enumeration
mechanism other than "read the bid stream or request a domain list".

## Programmatic binding

**Today (Ströer):**

- `networkid` — proprietary code, obtainable only by parsing `site.domain` /
  `site.page`, which is constructed as
  `{sitename.cleaned}-{city.cleaned}-{networkid}.de`.
- `device.ext.dooh.venuetypeid` — e.g. `106`. Taxonomy and version unstated.
- Network semantics documented as a table of URLs to German-language marketing pages.
- Discovery guidance: "Read the bid stream or request a domain list in order to white
  list targeting", plus "Set up a fall back line item to buy inventory from new train
  stations/malls Ströer may add to the portfolio" — an explicit admission that the
  inventory set is not enumerable through the protocol.

**Proposed:** venue type and seller network become first-class typed fields on the
impression opportunity, with taxonomy provenance. If the transport supports the
OpenRTB 2.6 `dooh` object, that is the correct home and the `device.ext` extension
should be retired — this needs confirming against the DSP adapter spec (see
`../analysis/open-gaps.md` §1).

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- which seller networks the offer covers, by stable ID and name;
- the venue types those networks resolve to, with taxonomy and version;
- the screen count per network (see **ADD-002**);
- which network-level restrictions attach (static-only, sync groups, approval rules);
- and it MUST be able to obtain the full network and venue-type catalogue before
  sending a brief, so that the brief can name them.

Sketch:

```json
{
  "venue": {
    "taxonomy": { "name": "openooh", "version": "<version>" },
    "types": [{ "id": 106, "name": "<label>" }]
  },
  "seller_network": {
    "id": "sv",
    "name": "Public Video Station",
    "seller": "stroeer",
    "maps_to_venue_types": [106]
  }
}
```

The catalogue itself — every network, its venue types, screen count, and attached
restrictions — is what a buyer agent needs at brief time. That makes network
enumeration a **discovery** obligation, not just a field: see **ADD-016**.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product discovery | `add-field` | Venue type with taxonomy provenance; seller network object |
| AdCP | Media Buy → targeting | `add-field` | Venue type and network as inclusion/exclusion dimensions |
| AdCP | Signals | `clarify-semantics` | Venue type is inventory metadata, not an audience signal — confirm placement |
| AAMP | ARTF | `add-field` | Venue type and network on the opportunity; retire the `device.ext` workaround |
| AAMP | Registry / Seller Agent | `new-task` | Network and venue-type catalogue enumeration |

## Partial conformance

- MAY omit `seller_network` entirely — venue type alone is conformant.
- MAY omit the venue-type label if the taxonomy is named and versioned, since the
  label is derivable.
- MUST NOT emit a venue-type ID without taxonomy name and version.
- MUST NOT require a buyer to parse a hostname, path or file name to recover the
  network. Anything that requires string surgery on a field with a different declared
  purpose is non-conformant by construction.

## Open questions

- [ ] Which OpenOOH taxonomy version does `venuetypeid: 106` follow? (`../analysis/open-gaps.md` §3.8)
- [ ] Is the Ströer network → venue type mapping published anywhere?
- [ ] Does the DSP adapter spec offer an OpenRTB 2.6 `dooh` path? Decides whether this
      is an extension or a migration.
- [ ] Should seller networks be standardised at all, or only required to be
      self-describing? Standardising commercial groupings across media owners is
      probably neither achievable nor desirable.
- [ ] How is a network's composition change (new stations, new malls) communicated?
      Ströer's answer today is a fallback line item, which an agent cannot infer.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §3, §15
- Ströer PPV Implementation Guide v6, §6 (Ströer networkid and DOOH Networks), §4
  (Location Targeting), §9 (Target High-Impact Ad Locations)
- Ströer PPV Implementation Guide — Static Creatives, pp. 4–5 (`device.ext.dooh.venuetypeid`)

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
