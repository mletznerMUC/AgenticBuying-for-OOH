# AAMP — Agentic Direct

> Status: **stub** — targets identified, mapping not yet written.
> Component scope below is from public sources as of August 2026 and needs
> verification against the current revision.

Agentic Direct covers orchestration and agent-to-agent communication for
non-auction transactions. This is the natural home for **classic OOH and reserved
DOOH**, which is still where the majority of OOH spend sits.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Brief and RFP exchange | An OOH brief: geography, target group, period, budget, venue preferences, format constraints |
| Availability response | Calendar-based availability per panel/screen and daypart, with capacity limits |
| Proposal / plan | A panel list with modelled reach and frequency, pricing per unit, production costs |
| Hold / option lifecycle | Soft holds, expiry, first refusal |
| Booking and contracting | Firm commitment, fixed period starts, minimums, cancellation terms |
| Fulfilment | Creative delivery, clearance, print and installation milestones |
| Post-campaign | Posting reports, proof of play, photographic evidence, reconciliation |
| Multi-seller coordination | One campaign across several media owners |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 02 Trading, 06 Delivery,
07 Booking, parts of 05 Creative and 08 Compliance.

## Mapping table

| Requirement | Target | Change type | Rationale | Confidence |
| --- | --- | --- | --- | --- |
| *TBD* | | | | |

## Open questions

- How far does Agentic Direct already model a negotiation with holds and lead times?
  If it does, OOH may need little more than vocabulary.
- Is physical fulfilment (print, logistics, installation) in scope for AAMP at all,
  or does the protocol stop at the booking?
