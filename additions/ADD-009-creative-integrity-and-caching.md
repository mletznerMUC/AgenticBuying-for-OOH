---
id: ADD-009
title: Creative Integrity and Caching
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Public Video Creative Approval; v6 §9"
targets:
  adcp: [creative]
  aamp: [artf, trust-and-transparency]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-009 — Creative Integrity and Caching

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Because approval involves a human looking at a file (**ADD-008**), the seller must
guarantee that the file which played is the file that was approved. Ströer does this by
caching:

- On first submission Ströer downloads the media file from the advertiser's host
  **once** and thereafter serves it from Ströer's own cache when the creative wins.
  All other trackers are preserved.
- Any swap of the MediaFile or MediaFileURL is "detected and treated as fraudulent
  behavior", causing immediate rejection of the DSP creative.
- Every permutation of a creative must be a separate DSP creative with a **new DSP
  creative ID** and a **unique MediaFile filename**.

This is a sound integrity model, and it is invisible in the protocol. The rules are
prose. The failure mode is a creative silently rejected as fraud. And the constraint is
the opposite of the digital norm, where rotating a creative URL behind a stable ID is
routine and expected — which is precisely why a buyer agent, reasoning from digital
defaults, will violate it.

The buyer-facing consequence is stated as folklore: "Do not override existing
creatives. Set up new creatives always (new name & creative ID) to avoid caching
related issues."

## Semantic definition

1. A seller MUST declare whether it caches approved creative assets, and whether the
   cached copy is authoritative at play time.
2. A seller MUST declare its **creative identity rule**: which properties, taken
   together, identify an approved creative. Ströer's rule is (creative ID, media file
   name).
3. A seller MUST declare its **mutability policy**: which properties of an approved
   creative may change without invalidating approval, and which may not.
4. A violation MUST produce a specific, distinguishable outcome. `integrity_violation`
   MUST be separable from an ordinary content rejection, because the buyer's remedy is
   completely different: re-submit under a new identity, rather than change the
   artwork.
5. Where mutation is legitimately required, it MUST be possible only under an explicit
   authorisation (see **ADD-010**), and the seller MUST declare that such a path
   exists.
6. A buyer agent MUST be able to determine, before submitting, whether its intended
   creative workflow — particularly any URL rotation — is permitted.

## Programmatic binding

**Today (Ströer):** enforced server-side, communicated in prose. Identity is
(`crid`, MediaFile filename). Violation results in creative rejection, reported through
the same channels as any other rejection (**ADD-008**), with no dedicated code that
distinguishes an integrity violation from a content problem.

**Proposed:** an integrity-policy declaration on the inventory or creative surface, and
a distinct rejection reason code for integrity violations within the **ADD-008**
taxonomy.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- that assets will be cached and that the cached copy is authoritative;
- what constitutes creative identity, so it can plan its creative naming and IDs;
- that URL rotation is prohibited without authorisation, and how to obtain it;
- how many distinct creatives it must therefore register — one per permutation, which
  directly affects both the approval lead time (**ADD-008**) and the production job.

Sketch:

```json
{
  "creative_integrity": {
    "caching": "seller_authoritative",
    "identity": ["creative_id", "media_file_name"],
    "immutable_after_approval": ["media_file_url", "media_file_bytes"],
    "mutable_after_approval": ["click_trackers", "impression_trackers"],
    "violation_outcome": "reject_and_flag",
    "mutation_authorisation": "ADD-010"
  }
}
```

For an IO buy the same declaration answers: how do I hand over assets, and what
happens if I need to change one mid-flight? Today that is an e-mail to operations.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Creative | `new-object` | Integrity-policy declaration: caching, identity, mutability |
| AdCP | Creative | `extend-enum` | `integrity_violation` in the rejection reason taxonomy (**ADD-008**) |
| AAMP | ARTF | `clarify-semantics` | Cached asset is authoritative; URL in the response is a source, not a runtime fetch |
| AAMP | Trust and Transparency | `add-field` | Asset integrity as a verifiable property of a play |

## Partial conformance

- MAY omit `mutable_after_approval` and declare only the immutable set.
- MAY omit `mutation_authorisation` where no such path exists — but MUST then say
  rotation is simply unavailable, rather than leaving it unstated.
- MUST NOT declare caching without declaring the identity rule.
- MUST NOT report an integrity violation as a generic rejection once codes exist.

## Open questions

- [ ] Is the identity rule exactly (creative ID, file name), or does Ströer also
      fingerprint content? A content hash would be a stronger and more portable
      identity.
- [ ] How long is a cached asset retained, and does re-submission of the same identity
      re-download?
- [ ] Does the integrity rule apply to the `iurl` banner path as well as the VAST path?
      The source documents only discuss VAST MediaFiles.
- [ ] Is a content hash a viable standard identity across sellers? It would remove the
      unique-filename requirement, which is a fragile convention.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §7
- Public Video Creative Approval ("How the caching works")
- Ströer PPV Implementation Guide v6, §8, §9 (Consider creative approval delay)
- DSP Integration Ströer SSP, "Cashing & DCO Approval"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer Creative Approval analysis |
