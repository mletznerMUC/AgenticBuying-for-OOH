# AdCP — Accounts and Governance

> Status: **stub** — targets identified, mapping not yet written.
> Task and field names below are from public sources as of August 2026 and need
> verification against the current revision.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Content standards (`create_content_standards`) | Location-bound restrictions: legal category limits, proximity rules, landlord and transit-operator rules, public-space content standards |
| Content calibration (`calibrate_content`) | Checking a creative against the rules that apply to a specific panel set before booking |
| Competitive separation | Category exclusivity within a loop or a location, without disclosing other buyers |
| Accounts | Media-owner identity, contracting party, production and installation cost lines, invoicing against verified delivery |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 08 Compliance & content
restrictions, parts of 02 Trading, parts of 06 Delivery.

## Mapping table

`P` = this surface is the addition's primary home (define the semantic here); `S` = secondary binding. Roles are from [`../../PLAN.md`](../../PLAN.md) §3. Target and change type are filled in once this surface is verified against the current upstream revision — see [`../../PLAN.md`](../../PLAN.md) §6.

| Addition (R1.0) | Role | Target | Change type | Confidence |
| --- | :-: | --- | --- | --- |
| [ADD-011](../../additions/ADD-011-compliance-declarations.md) · Compliance declarations | `P` | | | unverified |
| [ADD-012](../../additions/ADD-012-advertiser-loop-separation.md) · Advertiser loop separation | `P` | | | unverified |
| [ADD-005](../../additions/ADD-005-location-disclosure-tiers.md) · Location disclosure tiers | `S` | | | unverified |
| [ADD-008](../../additions/ADD-008-creative-approval-lifecycle.md) · Creative approval lifecycle | `S` | | | unverified |
| [ADD-010](../../additions/ADD-010-dynamic-creative-authorisation.md) · Dynamic creative authorisation | `S` | | | unverified |
| [ADD-013](../../additions/ADD-013-deal-access-and-response-obligation.md) · Deal access & response obligation | `S` | | | unverified |
| [ADD-014](../../additions/ADD-014-accreditation-io-and-settlement.md) · Accreditation, IO & settlement | `S` | | | unverified |

## Open questions

- Governance appears oriented to *brand suitability* (protecting the advertiser from
  the context). OOH needs the inverse: protecting the *site and the public* from the
  ad. Does that fit the same objects, or does it need its own?
- Is competitive separation expressible without leaking commercially sensitive
  information about who else is on the loop?
