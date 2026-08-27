# AdCP — Trusted Match

> Status: **stub** — likely mostly out of scope, to be confirmed.
> Task and field names below are from public sources as of August 2026 and need
> verification against the current revision.

Trusted Match covers serve-time activation of pre-negotiated packages via context or
identity matching. OOH has **no user identity**, so most of the identity path does
not apply.

## What may still apply

| Surface | OOH relevance |
| --- | --- |
| Context matching at serve time | A screen has context — location, venue type, time, weather, current transit state — that could be matched at play-out time |
| Package activation | Pre-negotiated OOH deals activated at scheduling time rather than per impression |
| Non-addressable declaration | An explicit capability flag so agents stop attempting identity-based operations against OOH inventory |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 09 Privacy & identity, possibly
parts of 04 Targeting.

## Mapping table

| Requirement | Target | Change type | Rationale | Confidence |
| --- | --- | --- | --- | --- |
| *TBD* | | | | |

## Open questions

- Is an explicit "non-addressable channel" declaration better placed here, in Media
  Buy product metadata, or as a protocol-wide capability?
- Does screen context at play-out time genuinely fit Trusted Match's model, or is it
  a different mechanism that only looks similar?
