---
id: ADD-007
title: Synchronised Multi-Screen Delivery (Sync Groups)
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §7.1-7.2; DSP Integration test plan"
targets:
  adcp: [creative, media-buy]
  aamp: [artf]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-007 — Synchronised Multi-Screen Delivery (Sync Groups)

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Ströer's Mall Video inventory is sold as a **sync group**: one physical moment across
adjacent screens of different aspect ratios. A single bid request carries two `imp`
entries — one 1080×1920 portrait, one 1920×1080 landscape — sharing a `tagid`, both
with `sequence: 1`, and the DSP is expected to answer both, with two different
creatives, in one response.

The coupling is the whole product. Winning one screen and not the other produces a
broken execution: half a synchronised installation showing an unrelated ad. Yet
nothing in the request expresses the constraint. `tagid` means "ad tag identifier" and
`sequence` means "position in a sequence of video ads"; neither defines a
must-win-together contract. The obligation exists only as a line in an onboarding test
plan: "Two items on one request and response compliance; one 16:9 and one 9:16 in sync
group."

A buyer agent cannot discover that this inventory requires paired creatives, cannot
tell whether a partial win is permitted, and — at brief time — cannot know it needs to
produce two aspect ratios of every creative.

## Semantic definition

1. Where inventory is only sellable as a coordinated set, the seller MUST declare a
   **sync group**: an identified set of slots that constitute one delivery moment.
2. A sync group MUST declare its **win semantics**: `all_or_nothing` (the set is void
   unless every member is filled) or `partial_permitted` (with the declared fallback
   for unfilled members).
3. Each member MUST declare its own format specification. Members of a sync group
   commonly differ in orientation and dimensions; they are not interchangeable.
4. A sync group MUST declare its **member roles** where they differ (e.g. primary and
   companion), so a buyer agent can assign creatives deliberately rather than by index.
5. Sync-group membership MUST be discoverable at brief time, since it determines the
   buyer's creative production requirements.
6. Delivery reporting for a sync group MUST report at member level and MUST make the
   grouping recoverable, so that a buyer can verify the set actually played together.
7. A sync group is a **delivery-moment** grouping. It MUST NOT be conflated with the
   player-group fan-out in **ADD-002**, which is a distribution concept.

## Programmatic binding

**Today (Ströer):**

- Two `imp` entries in one bid request, same `tagid` (`84288` in the example), both
  `sequence: 1`, differing in `w`/`h` (1080×1920 and 1920×1080).
- Response: two bids, `impid` `"1"` and `"2"`, distinct `crid`/`adid` values that
  encode the ratio by convention in the creative name (`A2-9-16_...`, `A1-16-9_...`),
  same `cid`, same `dealid`.
- The obligation to answer both is stated in the onboarding test plan and in the
  best-practice note that a programmatic guaranteed buyer must answer every bid request
  with a valid response.
- "Mall Video dual creative setup" is listed as something to ask a DSP representative
  about.

**Proposed:** an explicit sync-group object on the bid request, naming the group, its
members, their roles and the win semantics — so a bidder can honour the contract
without knowing the convention, and so a non-compliant response can be rejected with a
meaningful reason.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- that part of the inventory is sold as sync groups;
- the group composition: how many members, which format each requires, which roles;
- the win semantics, and what happens to a partially filled group;
- how many creative variants it must therefore produce.

Sketch:

```json
{
  "sync_groups": [{
    "group_type": "mall_dual",
    "win_semantics": "all_or_nothing",
    "members": [
      { "role": "primary",   "w": 1080, "h": 1920, "orientation": "portrait" },
      { "role": "companion", "w": 1920, "h": 1080, "orientation": "landscape" }
    ],
    "groups_in_offer": 118
  }]
}
```

For an IO buy this is what tells the buyer's creative team that the job is two
deliverables, not one — a fact currently transmitted by asking a sales representative.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product / offer | `new-object` | Sync-group declaration with members, roles, win semantics |
| AdCP | Creative | `new-object` | Multi-part creative bound to sync-group roles |
| AdCP | Media Buy → delivery reporting | `add-field` | Member-level reporting with recoverable grouping |
| AAMP | ARTF | `new-object` | Sync group on the bid request; response validation against win semantics |

## Partial conformance

- MAY omit `role` where members are genuinely interchangeable (rare).
- MAY omit `groups_in_offer` where the count is not known at offer time.
- MUST NOT omit `win_semantics`. A buyer that does not know whether a partial win is
  permitted cannot bid correctly.
- MUST NOT express grouping only through shared identifiers whose declared meaning is
  something else.

## Open questions

- [ ] Can a Ströer sync group be partially won today, and what plays if so?
      (`../analysis/open-gaps.md` §3.4)
- [ ] Are groups always exactly two members, or can they be larger?
- [ ] Is the group stable over time, or composed per play?
- [ ] Does the concept extend to genuine roadblocks (all frames in a location) and to
      creative that spans several frames as one image? Those are related but not
      identical — a spanning creative is one asset, a sync group is several.
- [ ] Should win semantics support `best_effort_with_fallback`, naming a house or
      default creative?

## Sources

- `../analysis/stroeer-ppv-baseline.md` §5
- Ströer PPV Implementation Guide v6, §7.1 (bid request example), §7.2 (bid response
  example), §9
- DSP Integration Ströer SSP, "PV Mall Multi-Format Bidding"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
