---
id: ADD-006
title: Creative Format Constraints and Landlord Media-Type Restrictions
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide - Static Creatives; v6 §9"
targets:
  adcp: [creative, media-buy]
  aamp: [artf, agentic-direct]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-006 — Creative Format Constraints and Landlord Media-Type Restrictions

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Some Ströer screens legally cannot show moving images. The reason is explicit:
"Based on the rules set by the publisher landlords some time only static creatives
(jpeg/png) are allowed — especially when the screens are next to the road."

This is a legal and contractual restriction on a physical site. It reaches the buyer
as **a mime-type list**. If `video.mimes` contains only `image/jpeg` and `image/png`,
the buyer is expected to infer that this is a static-only screen and respond with an
image. Nothing states that a restriction exists, why, or that it is permanent.

Layered on top:

- Some Roadside screens allow **"Cinemagraph"** only — technically an MP4, but with
  limits on animation. There is no mime type for "MP4 with restricted motion", so this
  constraint cannot be expressed at all.
- The affected-network list in the source document is dated **August 2022** — four
  years stale — which shows why the restriction must be a per-screen property rather
  than a hard-coded network list.
- Duration is set by the buyer in one implementation option and by the seller out of
  band in the other (see below), for the same physical play.
- The `video` object is always present, even on image-only inventory, because there
  was nowhere else to put the mime list.

A buyer agent cannot plan a DOOH campaign without knowing, at brief time, that part
of the inventory will reject its video creative.

## Semantic definition

1. Inventory MUST declare its accepted creative forms explicitly and positively:
   `static_image`, `video`, `restricted_motion` (cinemagraph-class), or a combination.
   This MUST NOT be inferred from a mime-type list.
2. Where a form is disallowed, the seller SHOULD declare the **reason class** —
   `landlord_restriction`, `regulatory`, `technical`, `venue_operator` — without
   requiring disclosure of the underlying contract.
3. A declared restriction MUST carry its scope: which screens or networks it applies
   to, and whether it is permanent or time-bounded.
4. `restricted_motion` MUST be a distinct declared form with its own machine-readable
   constraint parameters, not a video format the buyer must know is special.
5. Format specifications MUST include, per accepted form: pixel dimensions,
   orientation, accepted file types, and **exact permitted duration** — not only min
   and max.
6. **Play duration is a property of the offered slot, not of the creative.** Where
   duration is fixed by the seller, the seller MUST declare it in the offer. Where the
   buyer declares it, the permitted values MUST be enumerated by the seller.
7. Audio MUST be declared explicitly as unsupported where it is unsupported, rather
   than left to convention.

## Programmatic binding

**Today (Ströer):** two implementation options, both routed through OpenRTB objects
carrying a meaning they were not designed for.

*Option 1 — static image in the video object:*
- The `video` object is always present, even for image-only requests.
- Image-only requests list only `image/jpeg`, `image/png` (examples also show
  `image/bmp`). Image+video requests list standard video mimes plus the image types.
- Response: a VAST with an ImageURL in `MediaFile`, **exactly one** ImageURL per VAST
  ("we need to be 100% certain which file is intended to be played"), an explicit
  duration as for video, w/h as for video, all tracking events as for video, and a
  VAST `mimeType` matching the file.

*Option 2 — static image in the banner object:*
- Both `banner` and `video` objects present.
- Response uses `iurl`; the file type is conveyed by the **`Content-Type` metadata of
  the `iurl` link**, not a field.
- **Duration is "agreed at the time of creating the deal/campaign and inserted
  manually later by us"** — there is no field for it.
- Trackers go in `bid.ext.imptrackers`, and must carry both `${TOTAL_IMP}` and
  `${AUCTION_PRICE}`.

Infoscreen, Station Video and Mall Video always show standard video mimes only.

**Proposed:** a declared format-constraint object on the impression opportunity, with
accepted forms, reason class and exact duration. The mime list stays as the wire-level
filter for compatibility, but stops being the only channel for a legal restriction.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- which creative forms each part of the offer accepts, and which are excluded;
- why they are excluded, at reason-class granularity;
- the exact format specification per accepted form, including permitted durations;
- what share of the offered inventory is static-only — this changes the creative
  production brief, and therefore the cost of running the campaign at all;
- whether it must supply more than one creative variant to cover the offer.

Sketch:

```json
{
  "creative_constraints": [{
    "scope": { "seller_network": "rss", "screens": 240 },
    "accepted_forms": ["static_image", "restricted_motion"],
    "excluded_forms": [{ "form": "video", "reason_class": "landlord_restriction", "permanent": true }],
    "restricted_motion": { "container": "mp4", "constraint": "<machine-readable motion limits>" },
    "specs": [{
      "form": "static_image",
      "w": 1080, "h": 1920, "orientation": "portrait",
      "file_types": ["image/jpeg", "image/png"],
      "duration_seconds": 10,
      "duration_set_by": "seller",
      "audio": "unsupported"
    }]
  }]
}
```

An offer covering mixed inventory carries several such entries. A buyer agent can then
answer, before committing: *do I have the creative assets this offer needs?*

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Creative → format definitions | `new-object` | OOH format family: forms, exact duration, orientation, audio-unsupported |
| AdCP | Creative → format definitions | `extend-enum` | `restricted_motion` as a distinct creative form |
| AdCP | Media Buy → product / offer | `add-field` | Format-constraint manifest with scope and reason class |
| AdCP | Accounts / Governance | `clarify-semantics` | Landlord restriction as a location-bound rule (see **ADD-011**) |
| AAMP | ARTF | `add-field` | Declared accepted forms on the opportunity, alongside the mime list |
| AAMP | Agentic Direct | `add-field` | Format constraints as offer terms; duration as a negotiated slot property |

## Partial conformance

- MAY omit `reason_class` — the restriction itself is the load-bearing part.
- MAY omit `restricted_motion` parameters if the seller does not offer that form.
- MUST NOT rely on the mime list alone to express a legal restriction.
- MUST NOT omit `duration_seconds` and `duration_set_by`. The current split — buyer
  declares in one binding, seller sets manually in the other — is the exact ambiguity
  this addition removes.

## Open questions

- [ ] What is the machine-readable definition of a cinemagraph constraint? Frame-rate
      cap, motion-area percentage, luminance-change limit? Ströer's specs page would
      say; it was not among the analysed documents.
- [ ] Is `image/bmp` genuinely supported? It appears only in code examples.
      (`../analysis/open-gaps.md` §2.6)
- [ ] Is the static-only restriction per screen or per network in reality? The dated
      network list suggests per screen. (§2.7)
- [ ] What does `maxduration: 3600` mean on the Mall sync example? Probably
      unconstrained, but if slot length is genuinely not communicated, this addition
      must say so. (§2.3)
- [ ] Should the exact-duration requirement extend to a permitted-values list, for
      screens accepting several slot lengths?

## Sources

- `../analysis/stroeer-ppv-baseline.md` §4
- Ströer PPV Implementation Guide — Static Creatives, pp. 1, 3 (both options,
  cinemagraph, affected networks), pp. 4–6 (code examples)
- Ströer PPV Implementation Guide v6, §9 (Request a DooH checklist: creative
  format/framerate/media type, Mall Video dual creative setup)

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer Static Creatives analysis |
