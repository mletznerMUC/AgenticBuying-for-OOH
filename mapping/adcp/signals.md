# AdCP — Signals

> Status: **stub** — targets identified, mapping not yet written.
> Task and field names below are from public sources as of August 2026 and need
> verification against the current revision.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Signal discovery (`get_signals`) | Discovering OOH audience currencies, venue-level audience models and target-group indices |
| Signal activation (`activate_signal`) | Applying an audience or moment condition to an OOH buy |
| Signal provenance | Currency name, methodology version, geography, visibility basis, modelled/measured/verified status |
| Contextual and moment signals | Weather, temperature, transit status, event schedules, results and price feeds as bookable conditions |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 03 Audience & measurement,
parts of 04 Targeting, parts of 09 Privacy.

## Mapping table

| Requirement | Target | Change type | Rationale | Confidence |
| --- | --- | --- | --- | --- |
| *TBD* | | | | |

## Open questions

- Are OOH audience currencies signals, or product metadata? They behave more like
  measurement provenance than like activatable audiences.
- Do moment triggers belong here or in Media Buy targeting? They are conditions on
  play-out, not audiences.
- Does the Signals model assume user-level addressability anywhere that OOH would
  have to work around?
