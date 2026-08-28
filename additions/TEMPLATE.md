---
id: ADD-NNN
title: Short title
version: 0.1.0
status: draft
since: null
supersedes: []
superseded_by: null
origin: "Source document and section"
targets:
  adcp: []
  aamp: []
applies_to: [programmatic, io]
target_revision_checked: null
protocol_ownership:
  owner: adcp          # adcp | aamp — the protocol that owns the DEFINITION.
  secondary: []        # other protocols this binds into
upstream_status: gap   # exists | partial | gap — from verification/
verified_against:
  adcp: null
  aamp: null
  date: null
---

# ADD-NNN — Short title

> Version 0.1.0 · Status: `draft` · Not in a release yet
>
> **Protocol owner: AdCP** · also binds into …
>
> 🔴 **Verified confirmed gap** against AdCP <rev> and AAMP <rev> on <date>.

## Verification

What already exists upstream, and what therefore remains to be asked for. **Check
before writing the rest of this document** — verification found that most R1.0
additions proposed things the protocols already had.

Full evidence: `../../verification/verdicts.md` (relative to `additions/<owner>/`)

## Problem

What breaks today. Be concrete: the field that is missing, the concept that has no
home, the thing a buyer agent cannot discover. Name the market and the media owner
if the problem is specific to them.

## Semantic definition

The concept, defined without reference to any transport. This section is the
normative core — the bindings below are derived from it, not the other way round.

Use MUST / SHOULD / MAY deliberately.

## Programmatic binding

How the concept is carried in a real-time transaction.

**Today (Ströer):** the existing proprietary encoding, verbatim.

**Already upstream:** the existing standard field or object, cited by schema path.

**Proposed:** what remains to be added, and which upstream object it attaches to.

## Offer / IO binding

How the concept appears when there is no bid request: in a response to a buyer
agent's brief, in an offer, and in an order.

State what a buyer agent must be able to conclude from the offer alone.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | | | |
| AAMP | | | |

Change types: `extend-enum`, `add-field`, `new-object`, `new-task`,
`clarify-semantics`, `out-of-scope`.

## Partial conformance

What an implementer may omit while still claiming `oohstd:ADD-NNN@x.y/partial`, and
what it may never omit.

## Open questions

- [ ] …

## Sources

- `../analysis/stroeer-ppv-baseline.md` §…
- Source document, section/page

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | YYYY-MM-DD | Initial draft |
