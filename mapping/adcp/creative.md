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

| Requirement | Target | Change type | Rationale | Confidence |
| --- | --- | --- | --- | --- |
| *TBD* | | | | |

## Open questions

- Is clearance a creative lifecycle state, or does it belong in Governance?
- Does the creative model support a hard duration constraint, or only a preference?
- How should a creative that spans multiple physical frames be expressed — one
  creative with parts, or a group of creatives with a synchronisation contract?
