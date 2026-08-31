# AdCP proposals

Proposals targeting **AdCP** (`adcontextprotocol/adcp`), verified against
**3.2.0-beta.8**.

Naming: `OEP-ADCP-NNNN-slug.md`. Numbers are per protocol and permanent.

Upstream contribution route: schemas under `static/schemas/source/`, docs under
`docs/`. For anything genuinely OOH-only, AdCP has a first-class extension mechanism —
a file at `/schemas/extensions/ooh.json` declaring `valid_from`, with data carried at
`ext.ooh` (see [`../../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) §8).

## Index

The four confirmed gaps are written. Priority order follows
[`../../verification/verdicts.md`](../../verification/verdicts.md): gaps first, because
the foundations R1.0 planned to propose already exist upstream.

| OEP | Title | Bundles | Change type | Status |
| --- | --- | --- | --- | --- |
| [0001](OEP-ADCP-0001-location-disclosure-tiers.md) | Location disclosure tiers | ADD-005 | `new-object` + `add-field` | `draft` |
| [0002](OEP-ADCP-0002-separation-and-capacity-caps.md) | Advertiser separation and capacity caps | ADD-012 | `new-object` + `extend-enum` | `draft` |
| [0003](OEP-ADCP-0003-buyer-eligibility-and-obligations.md) | Buyer eligibility and response obligations | ADD-013, ADD-014 residue | `new-object` + `add-field` | `draft` |
| [0004](OEP-ADCP-0004-creative-integrity-policy.md) | Creative integrity policy | ADD-009 | `new-object` + `add-field` + `extend-enum` | `draft` |

All four propose **core** changes rather than an `ext.ooh` namespace. Each explains why
in a "Why core and not an OOH extension" section — in short, all four describe problems
that exist outside OOH (curated deals, CTV pods, contracted media generally, any
human-reviewed cached creative), and three of them must interact with core objects an
extension cannot constrain.

Each proposal states what already exists in AdCP 3.2 and why it is insufficient, with
schema paths, per the rule in [`../README.md`](../README.md).

## Planned
| 0005 | Approval SLA and earliest achievable start | ADD-008 | 🟡 States and reason codes exist; only the SLA is missing. |
| 0006 | Planning targets in briefs, and unmet-target responses | ADD-015 + ADD-002 forecast | 🟡 SOV exists in pricing; brief targets and `unmet_brief_targets` do not. |
| 0007 | DOOH creative formats | ADD-006 | 🟡 Needs a format family, `restricted_motion`, and landlord reason class. |

OEP-ADCP-0001 §Proposal rule 4 depends on 0006's unmet-target mechanism, but stands
without it. 0004 references ADD-010 (dynamic creative authorisation) as the
authorisation path for permitted asset rotation; that remains unwritten.

Not proposals — feedback and guidance instead:

| Addition | Instead of a proposal |
| --- | --- |
| ADD-007 | Review feedback on the experimental `coordinated_placements` format, validated against real DOOH sync groups |
| ADD-016 | Declare OOH conformance claims inside the existing `get_adcp_capabilities` |
