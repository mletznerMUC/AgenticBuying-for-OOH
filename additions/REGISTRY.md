# Addition registry

The index of all additions. This table is the authoritative list of IDs; the
per-addition front matter is the authoritative source for each row's detail, and this
file should be regenerated from it rather than edited independently.

**IDs are permanent.** See [`../VERSIONING.md`](../VERSIONING.md).

## Release R1.0 — derived from the Ströer Public Video DSP integration

| ID | Title | Ver | Status | Applies to | AdCP targets | AAMP targets |
| --- | --- | --- | --- | --- | --- | --- |
| [ADD-001](ADD-001-total-audience-impressions.md) | Total Audience Impressions | 0.1.0 | `draft` | prog + IO | media-buy, signals | artf, agentic-audiences |
| [ADD-002](ADD-002-play-chain-and-player-model.md) | Play Chain and Master/Slave Player Model | 0.1.0 | `draft` | prog + IO | media-buy | artf, trust-and-transparency |
| [ADD-003](ADD-003-delayed-play-confirmation.md) | Delayed Play Confirmation and Settlement Latency | 0.1.0 | `draft` | prog + IO | media-buy | artf, trust-and-transparency |
| [ADD-004](ADD-004-venue-and-network-taxonomy.md) | Venue and Network Taxonomy | 0.1.0 | `draft` | prog + IO | media-buy, signals | artf, registry |
| [ADD-005](ADD-005-location-disclosure-tiers.md) | Location Disclosure Tiers | 0.1.0 | `draft` | prog + IO | media-buy, governance | artf, agentic-direct |
| [ADD-006](ADD-006-creative-format-constraints.md) | Creative Format Constraints and Landlord Media-Type Restrictions | 0.1.0 | `draft` | prog + IO | creative, media-buy | artf, agentic-direct |
| [ADD-007](ADD-007-synchronised-multi-screen-delivery.md) | Synchronised Multi-Screen Delivery (Sync Groups) | 0.1.0 | `draft` | prog + IO | creative, media-buy | artf |
| [ADD-008](ADD-008-creative-approval-lifecycle.md) | Creative Approval Lifecycle and SLA | 0.1.0 | `draft` | prog + IO | creative, governance | agentic-direct, trust-and-transparency |
| [ADD-009](ADD-009-creative-integrity-and-caching.md) | Creative Integrity and Caching | 0.1.0 | `draft` | prog + IO | creative | artf, trust-and-transparency |
| [ADD-010](ADD-010-dynamic-creative-authorisation.md) | Dynamic Creative Authorisation | 0.1.0 | `draft` | prog + IO | creative, governance | agentic-direct, trust-and-transparency |
| [ADD-011](ADD-011-compliance-declarations.md) | Compliance Declarations and Youth Protection | 0.1.0 | `draft` | prog + IO | accounts, governance, creative | agentic-direct, trust-and-transparency |
| [ADD-012](ADD-012-advertiser-loop-separation.md) | Advertiser Loop Separation | 0.1.0 | `draft` | prog + IO | governance, media-buy | artf |
| [ADD-013](ADD-013-deal-access-and-response-obligation.md) | Deal Access and Guaranteed Response Obligation | 0.1.0 | `draft` | prog + IO | media-buy, accounts | artf, agentic-direct |
| [ADD-014](ADD-014-accreditation-io-and-settlement.md) | Accreditation, Insertion Order and Settlement | 0.1.0 | `draft` | prog + IO | accounts, media-buy | agentic-direct, registry |
| [ADD-015](ADD-015-ooh-planning-metrics.md) | OOH Planning Metrics in Briefs and Offers | 0.1.0 | `draft` | **IO** + prog | media-buy, signals | agentic-direct, agentic-audiences |
| [ADD-016](ADD-016-seller-conformance-profile.md) | Seller Conformance Profile and Capability Discovery | 0.1.0 | `draft` | prog + IO | media-buy | registry, trust-and-transparency |

Every addition in R1.0 is at `0.1.0` / `draft`: the analysis is complete but nothing has
been verified against the current AdCP or AAMP revisions, and two source specifications
could not be retrieved (see [`../analysis/open-gaps.md`](../analysis/open-gaps.md)).
Nothing here should be implemented yet.

## Next free ID

`ADD-017`

## Retired, superseded and withdrawn

None yet. When an addition is retired its row moves here and keeps its ID forever.

## Coverage against `ooh-specifics/`

Release R1 comes from one media owner's programmatic integration, so its coverage of the
broader OOH requirement catalogue is deliberately uneven. Areas with little or no R1
coverage are where the next releases go.

| `ooh-specifics/` area | R1 coverage |
| --- | --- |
| 01 Inventory & supply model | Partial — ADD-002, ADD-004 |
| 02 Trading & pricing models | Partial — ADD-001, ADD-013, ADD-014 |
| 03 Audience & measurement | Partial — ADD-001, ADD-015 |
| 04 Targeting dimensions | Thin — ADD-004, ADD-005; no isochrone, POI or trigger targeting |
| 05 Creative & formats | Good — ADD-006 to ADD-010 |
| 06 Delivery & proof of play | Partial — ADD-002, ADD-003; no third-party verification |
| 07 Availability & booking lifecycle | **Weak** — ADD-014 only; no holds, no availability calendar |
| 08 Compliance & content restrictions | Partial — ADD-011, ADD-012 |
| 09 Privacy & identity | **Not covered** — noted in analysis, no addition yet |
| 10 Sustainability | **Not covered** |

Classic/static (printed) OOH is not covered at all: the source documents are entirely
about digital screens. That is the largest single gap in R1 and the obvious candidate
for R2.
