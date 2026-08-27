# AAMP — Agentic Audiences

> Status: **stub** — targets identified, mapping not yet written.
> Component scope below is from public sources as of August 2026 and needs
> verification against the current revision.

Agentic Audiences standardises audience signals for agent use (formerly the User
Context Protocol). OOH's audience model is fundamentally different: aggregate,
modelled and ID-free.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Audience schema | Aggregate audience with no user or device identifier |
| Currency and provenance | Currency name, methodology version, geography, visibility basis, modelled/measured/verified status, confidence |
| Impression multiplier | Contacts per play, and its granularity (screen, venue type, daypart) |
| Reach and frequency | Non-additive reach across a panel set |
| Target-group indexing | Demographic indices against a currency panel rather than user attributes |
| Explicit non-addressability | A declared capability, so agents do not attempt identity operations |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 03 Audience & measurement,
09 Privacy & identity.

## Mapping table

| Requirement | Target | Change type | Rationale | Confidence |
| --- | --- | --- | --- | --- |
| *TBD* | | | | |

## Open questions

- Does the schema assume user-level context anywhere structurally, or only in
  optional fields?
- Should OOH audience data be modelled as a distinct audience *kind* rather than a
  variant of the existing one?
- Where does the provenance metadata belong so it survives being passed between
  agents?
