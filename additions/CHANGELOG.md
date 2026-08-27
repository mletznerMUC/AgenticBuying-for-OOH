# Changelog

Release-level history. Per-addition history lives in each addition's own `## Changelog`
section. See [`../VERSIONING.md`](../VERSIONING.md) for the scheme.

## Unreleased

Nothing yet.

## R1.0 — 2026-08-27

First release. Sixteen additions, all at `0.1.0` / `draft`, derived from analysis of
Ströer's production DSP integration standards for Public Video (DOOH).

Manifest: [`releases/R1.0.md`](releases/R1.0.md)

### Added

| ID | Title |
| --- | --- |
| ADD-001 | Total Audience Impressions |
| ADD-002 | Play Chain and Master/Slave Player Model |
| ADD-003 | Delayed Play Confirmation and Settlement Latency |
| ADD-004 | Venue and Network Taxonomy |
| ADD-005 | Location Disclosure Tiers |
| ADD-006 | Creative Format Constraints and Landlord Media-Type Restrictions |
| ADD-007 | Synchronised Multi-Screen Delivery (Sync Groups) |
| ADD-008 | Creative Approval Lifecycle and SLA |
| ADD-009 | Creative Integrity and Caching |
| ADD-010 | Dynamic Creative Authorisation |
| ADD-011 | Compliance Declarations and Youth Protection |
| ADD-012 | Advertiser Loop Separation |
| ADD-013 | Deal Access and Guaranteed Response Obligation |
| ADD-014 | Accreditation, Insertion Order and Settlement |
| ADD-015 | OOH Planning Metrics in Briefs and Offers |
| ADD-016 | Seller Conformance Profile and Capability Discovery |

### Notes

- Every addition carries both a programmatic and an offer/IO binding. The offer/IO
  binding is new work — none of it exists in the source material, which is entirely
  transport-level.
- No addition has been verified against a current AdCP or AAMP revision. All placements
  are proposals.
- Two source specifications could not be retrieved (network egress policy) and are
  tracked in [`../analysis/open-gaps.md`](../analysis/open-gaps.md). ADD-008 is the most
  affected: the rejection reason-code taxonomy is unknown.
- Eight internal inconsistencies in the source documents are recorded rather than
  silently resolved. The creative-approval SLA (24 h vs 48 h) is the one that most needs
  an answer.
