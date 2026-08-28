# AdCP — Creative

> Status: **stub** — targets identified, mapping not yet written.
> Task and field names below are from public sources as of August 2026 and need
> verification against the current revision.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Creative format definitions | DOOH formats by property: pixel dimensions, orientation, aspect ratio, exact duration, silent, no click; static/print specs as a separate family |
| Creative build (`build_creative`) | Generating OOH-legal creative: safe areas, minimum type size, viewing distance, no-audio and no-click constraints |
| Creative preview (`preview_creative`) | Rendering a creative in the context of a real screen or frame set |
| Transformers (`list_transformers`) | Resize/re-encode paths between DOOH formats and their constraints |
| Multi-asset creative | Multi-frame and synchronised creative bound to specific physical frames |
| Dynamic creative | Template plus data feed plus trigger conditions |
| Approval state | Copy clearance by media owner, landlord and authority, including mid-campaign revocation |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 05 Creative & formats, parts of
08 Compliance.

## Mapping table

`P` = this surface is the addition's primary home (define the semantic here); `S` = secondary binding. Roles are from [`../../PLAN.md`](../../PLAN.md) §3. Target and change type are filled in once this surface is verified against the current upstream revision — see [`../../PLAN.md`](../../PLAN.md) §6.

| Addition (R1.0) | Role | Target | Change type | Confidence |
| --- | :-: | --- | --- | --- |
| [ADD-006](../../additions/adcp/ADD-006-creative-format-constraints.md) · Creative format constraints | `P` | | | unverified |
| [ADD-007](../../additions/adcp/ADD-007-synchronised-multi-screen-delivery.md) · Sync groups | `P` | | | unverified |
| [ADD-008](../../additions/adcp/ADD-008-creative-approval-lifecycle.md) · Creative approval lifecycle | `P` | | | unverified |
| [ADD-009](../../additions/adcp/ADD-009-creative-integrity-and-caching.md) · Creative integrity & caching | `P` | | | unverified |
| [ADD-010](../../additions/adcp/ADD-010-dynamic-creative-authorisation.md) · Dynamic creative authorisation | `P` | | | unverified |
| [ADD-011](../../additions/adcp/ADD-011-compliance-declarations.md) · Compliance declarations | `S` | | | unverified |

## Open questions

- Is clearance a creative lifecycle state, or does it belong in Governance?
- Does the creative model support a hard duration constraint, or only a preference?
- How should a creative that spans multiple physical frames be expressed — one
  creative with parts, or a group of creatives with a synchronisation contract?
