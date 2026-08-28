---
id: ADD-016
title: Seller Conformance Profile and Capability Discovery
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "DSP Integration Ströer SSP (onboarding and test plan)"
targets:
  adcp: [media-buy]
  aamp: [agent-sdks-and-registry, trust-and-transparency]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-016 — Seller Conformance Profile and Capability Discovery

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Ströer's DSP integration document is, in effect, a **conformance suite** — a phased test
plan a DSP must pass before it can transact:

| Phase | Tests |
| --- | --- |
| Discovery | Spec review and Q&A; billing instructions and forms |
| Negotiation | Framework contract / media order / Nautilus debtor registration |
| PG on PV Mall | Creative pre-approval round trip (reject → resubmit → approve); creative approval and VAST inspection; caching and DCO approval; multi-format sync bidding; impression variance check; pacing; creative-targeting A/B |
| PA on PV Roadside | Static creative compliance; DSP pacing without overspend |

Every test maps precisely onto one of the additions in this release. That is strong
evidence the additions describe the real integration surface — and it makes the test
plan a natural conformance definition.

But today this is a slide deck, run manually, per DSP, per media owner. Every buyer
integrating with every seller rediscovers the same requirements through Q&A sessions.
For agentic buying that model does not scale at all: a buyer agent cannot sit in a
kick-off call. It needs to ask a seller what it supports and get a machine-readable
answer.

## Semantic definition

1. A seller MUST be able to publish a **capability profile**: which additions it
   implements, at which versions, using the conformance claims in
   [`../VERSIONING.md`](../VERSIONING.md) §4.
2. A capability profile MUST be retrievable by a buyer agent **before** any transaction
   or contract.
3. A profile MUST distinguish **implemented**, **partially implemented** (with the
   addition's own partial-conformance terms) and **not implemented**.
4. A profile SHOULD declare the inventory scope each claim applies to. Claims commonly
   differ by network — Ströer's static-creative rules apply to Roadside, City, City
   Tower and Giant but not to Station or Mall.
5. A seller SHOULD publish a **test environment** where a buyer can exercise the claimed
   capabilities. Ströer has one (`publisher.id 17387`); it is discoverable only by
   reading a PDF.
6. Where a seller requires a buyer to pass certification before production access, that
   requirement MUST be declared as a prerequisite (see **ADD-014**), with its phases and
   lead time.
7. A conformance claim MUST be **falsifiable**: each addition SHOULD define at least one
   observable check that verifies the claim. A claim nobody can test is marketing.
8. Buyer agents SHOULD publish the reciprocal profile. Obligations run both ways — the
   response obligation in **ADD-013** and the reporting obligation in **ADD-001** are
   requirements *on the buyer*.

## Programmatic binding

**Today (Ströer):** the sandbox is identified by `publisher.id 17387` versus `17409` for
production. Everything else is manual: documents, Q&A sessions, a status-tracked
checklist maintained by hand.

**Proposed:** capability discovery does not belong in the bid stream. Its programmatic
relevance is the test environment and the fact that a seller's claims determine which
request shapes a bidder must be able to handle.

## Offer / IO binding

Before briefing, a buyer agent MUST be able to determine:

- which of these additions the seller implements, and at what versions;
- which parts of the seller's inventory each claim covers;
- what the buyer itself must implement in order to transact;
- whether certification is required, what it involves, and how long it takes;
- where to test.

Sketch:

```json
{
  "conformance": {
    "claims": [
      { "claim": "oohstd:ADD-001@0.1", "level": "implemented" },
      { "claim": "oohstd:ADD-006@0.1", "level": "implemented",
        "scope": { "seller_networks": ["rss", "cs", "ct", "gou", "gin"] } },
      { "claim": "oohstd:ADD-010@0.1", "level": "partial",
        "note": "authorisation issued out of band" },
      { "claim": "oohstd:ADD-015@0.1", "level": "not_implemented" }
    ],
    "buyer_requirements": ["oohstd:ADD-001@0.1", "oohstd:ADD-013@0.1"],
    "certification": {
      "required": true,
      "phases": ["discovery", "negotiation", "guaranteed_deal_test", "auction_deal_test"],
      "lead_time": "P30D"
    },
    "test_environment": { "available": true, "identifier": "<sandbox id>" }
  }
}
```

`buyer_requirements` is the reciprocal half, and it is what makes the profile a
handshake rather than a brochure: the seller states what it will do *and* what it needs
the buyer to do.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product discovery | `add-field` | Capability claims on the seller or product |
| AdCP | — | `new-task` | Retrieve a seller capability profile |
| AAMP | Registry / Seller Agent | `new-object` | Capability profile with scoped claims |
| AAMP | Buyer Agent | `new-object` | Reciprocal buyer profile |
| AAMP | Trust and Transparency | `add-field` | Certification state and falsifiable claim checks |

## Partial conformance

- MAY omit `test_environment` where none exists.
- MAY omit `scope` where a claim applies to all inventory.
- MUST NOT claim `implemented` for an addition whose MUST-level requirements are not
  met; use `partial` with a note.
- MUST NOT publish a profile that cannot be retrieved before contracting — that defeats
  the purpose.

## Open questions

- [ ] Should the conformance-claim string format be defined here or in `VERSIONING.md`?
      Currently in `VERSIONING.md` §4; this addition consumes it.
- [ ] Who arbitrates a disputed claim? Self-declaration is the only realistic starting
      point, but it invites drift.
- [ ] Should each addition carry an executable conformance test, and if so in what form?
- [ ] Does AAMP's registry already provide a capability mechanism we should extend rather
      than duplicate? Needs verification against the current revision.
- [ ] How does a profile version relative to the release it claims — can a seller claim
      `R1.0` with per-addition exceptions? (`VERSIONING.md` §4 says yes; needs an
      example.)

## Sources

- `../analysis/stroeer-ppv-baseline.md` §14
- DSP Integration Ströer SSP (full phase and task table)
- Ströer PPV Implementation Guide v6, §5 (sandbox publisher ID), Appendix (Seat Setup,
  deal setup and testing)

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer DSP integration plan |
