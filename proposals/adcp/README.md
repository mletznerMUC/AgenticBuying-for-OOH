# AdCP proposals

Proposals targeting **AdCP** (`adcontextprotocol/adcp`), verified against
**3.2.0-beta.8**.

Naming: `OEP-ADCP-NNNN-slug.md`. Numbers are per protocol and permanent.

Upstream contribution route: schemas under `static/schemas/source/`, docs under
`docs/`. For anything genuinely OOH-only, AdCP has a first-class extension mechanism —
a file at `/schemas/extensions/ooh.json` declaring `valid_from`, with data carried at
`ext.ooh` (see [`../../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) §8).

## Index

| OEP | Title | Bundles | Status |
| --- | --- | --- | --- |
| — | *none written yet* | | |

## Planned

Priority order follows [`../../verification/verdicts.md`](../../verification/verdicts.md):
confirmed gaps first, because the foundations R1.0 planned to propose already exist.

| # | Title | Bundles | Why |
| --- | --- | --- | --- |
| 0001 | Location disclosure tiers | ADD-005 | 🔴 Confirmed gap. Nothing comparable upstream. |
| 0002 | Loop separation and capacity caps | ADD-012 | 🔴 Confirmed gap. `exclusivity` is product-level and cannot express it. Blocks SOV targets. |
| 0003 | Buyer eligibility and response obligations | ADD-013 + ADD-014's residue | 🔴 Confirmed gap. Prerequisites with buyer-specific status. |
| 0004 | Creative integrity policy | ADD-009 | 🔴 Confirmed gap, and cheap — one policy object plus one reason-code value. |
| 0005 | Approval SLA and earliest achievable start | ADD-008 | 🟡 States and reason codes exist; only the SLA is missing. |
| 0006 | Planning targets in briefs, and unmet-target responses | ADD-015 + ADD-002 forecast | 🟡 SOV exists in pricing; brief targets and `unmet_brief_targets` do not. |
| 0007 | DOOH creative formats | ADD-006 | 🟡 Needs a format family, `restricted_motion`, and landlord reason class. |

Not proposals — feedback and guidance instead:

| Addition | Instead of a proposal |
| --- | --- |
| ADD-007 | Review feedback on the experimental `coordinated_placements` format, validated against real DOOH sync groups |
| ADD-016 | Declare OOH conformance claims inside the existing `get_adcp_capabilities` |
