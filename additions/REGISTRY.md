# Addition registry

The index of all additions. **IDs are permanent** — see
[`../VERSIONING.md`](../VERSIONING.md).

Additions live in a directory named for the protocol that owns their **definition**:

```
additions/
├── adcp/     13 additions defined in AdCP
└── aamp/      3 additions defined in AAMP
```

Most additions still *bind into* both protocols; the directory says where the semantic
is defined, not where it is used. Each addition's `protocol_ownership` front matter
names the secondary bindings.

Verdicts come from [`../verification/verdicts.md`](../verification/verdicts.md),
checked 2026-08-27 against AdCP **3.2.0-beta.8** and AAMP
(**OpenDirect 2.1** / **OpenRTB 2.6**).

🟢 `exists` upstream · 🟡 `partial` · 🔴 confirmed `gap`

## Owned by AdCP — `additions/adcp/`

| ID | Title | Ver | Status | Upstream | Also binds |
| --- | --- | --- | --- | :-: | --- |
| [ADD-002](adcp/ADD-002-play-chain-and-player-model.md) | Play Chain and Master/Slave Player Model | 0.2.0 | `draft` | 🟡 partial | AAMP |
| [ADD-003](adcp/ADD-003-delayed-play-confirmation.md) | Delayed Play Confirmation and Settlement Latency | 0.2.0 | `draft` | 🟡 partial | AAMP |
| [ADD-005](adcp/ADD-005-location-disclosure-tiers.md) | Location Disclosure Tiers | 0.2.1 | `review` | 🔴 **gap** | AAMP |
| [ADD-006](adcp/ADD-006-creative-format-constraints.md) | Creative Format Constraints and Landlord Media-Type Restrictions | 0.2.0 | `draft` | 🟡 partial | AAMP |
| [ADD-007](adcp/ADD-007-synchronised-multi-screen-delivery.md) | Synchronised Multi-Screen Delivery (Sync Groups) | 0.2.0 | `draft` | 🟢 exists | — |
| [ADD-008](adcp/ADD-008-creative-approval-lifecycle.md) | Creative Approval Lifecycle and SLA | 0.2.0 | `draft` | 🟡 partial | AAMP |
| [ADD-009](adcp/ADD-009-creative-integrity-and-caching.md) | Creative Integrity and Caching | 0.2.1 | `review` | 🔴 **gap** | — |
| [ADD-010](adcp/ADD-010-dynamic-creative-authorisation.md) | Dynamic Creative Authorisation | 0.2.0 | `draft` | 🟡 partial | AAMP |
| [ADD-011](adcp/ADD-011-compliance-declarations.md) | Compliance Declarations and Youth Protection | 0.2.0 | `draft` | 🟡 partial | AAMP |
| [ADD-012](adcp/ADD-012-advertiser-loop-separation.md) | Advertiser Loop Separation | 0.2.1 | `review` | 🔴 **gap** | AAMP |
| [ADD-013](adcp/ADD-013-deal-access-and-response-obligation.md) | Deal Access and Guaranteed Response Obligation | 0.2.1 | `review` | 🔴 **gap** | AAMP |
| [ADD-015](adcp/ADD-015-ooh-planning-metrics.md) | OOH Planning Metrics in Briefs and Offers | 0.2.0 | `draft` | 🟡 partial | AAMP |
| [ADD-016](adcp/ADD-016-seller-conformance-profile.md) | Seller Conformance Profile and Capability Discovery | 0.2.0 | `draft` | 🟡 partial | AAMP |

## Owned by AAMP — `additions/aamp/`

| ID | Title | Ver | Status | Upstream | Also binds |
| --- | --- | --- | --- | :-: | --- |
| [ADD-001](aamp/ADD-001-total-audience-impressions.md) | Total Audience Impressions | 0.2.0 | `draft` | 🟢 exists | AdCP |
| [ADD-004](aamp/ADD-004-venue-and-network-taxonomy.md) | Venue and Network Taxonomy | 0.2.0 | `draft` | 🟢 exists | AdCP |
| [ADD-014](aamp/ADD-014-accreditation-io-and-settlement.md) | Accreditation, Insertion Order and Settlement | 0.2.0 | `draft` | 🟢 exists | AdCP |

All three AAMP-owned additions verified as already existing upstream. That is not a
coincidence: AAMP builds on OpenRTB 2.6 and OpenDirect 2.1, both of which have carried
OOH constructs for years. **The unsolved problems are on the AdCP side**, where the
agent-facing product and offer layer is newer.

## Where the value is

| Bucket | Additions | What to do |
| --- | --- | --- |
| 🔴 **Confirmed gaps** | ADD-005, ADD-009, ADD-012, ADD-013 | ✅ **Proposals written** — [`../proposals/adcp/`](../proposals/adcp/). All four now `review`. |
| 🟡 Partial | ADD-002, 003, 006, 008, 010, 011, 015, 016 | Narrow, specific asks against existing objects |
| 🟢 Exists | ADD-001, ADD-004, ADD-007, ADD-014 | Conformance and migration guidance, not proposals |

## Next free ID

`ADD-017`

## Retired, superseded and withdrawn

None. When an addition is retired its row moves here and keeps its ID forever.

## Coverage against `ooh-specifics/`

Corrected after verification — two R1.0 claims turned out to be wrong.

| `ooh-specifics/` area | Coverage |
| --- | --- |
| 01 Inventory & supply model | Partial — ADD-002, ADD-004 |
| 02 Trading & pricing models | Partial — ADD-001, ADD-013, ADD-014. ⚠️ **The doc's claim that panel-per-period pricing is inexpressible is wrong** — AdCP `time-option` prices per hour/day/week/month |
| 03 Audience & measurement | Partial — ADD-001, ADD-015 |
| 04 Targeting dimensions | Thin — ADD-004, ADD-005; no isochrone, POI or trigger targeting |
| 05 Creative & formats | Good — ADD-006 to ADD-010 |
| 06 Delivery & proof of play | Partial — ADD-002, ADD-003 |
| 07 Availability & booking lifecycle | Partial — ADD-013, ADD-014. ⚠️ **Soft holds exist**: `OpenDirect.Line.reservedexpirydate` |
| 08 Compliance & content restrictions | Partial — ADD-011, ADD-012 |
| 09 Privacy & identity | Not covered by an addition |
| 10 Sustainability | Not covered |

⚠️ **Classic/static OOH is no longer an open gap upstream.** AdCP 3.2 has an
experimental `ooh_metrics` with panel identifiers (Geopath, Route, plant face),
`estimation_basis`, and posting records as the settlement artifact — plus
`material_submission` for physical creative. R1.0 recorded this as the largest gap in
the repository; it is not. What remains is validating that work against real classic
OOH trading, which is a different and smaller job.
