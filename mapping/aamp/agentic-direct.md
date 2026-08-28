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

`P` = this surface is the addition's primary home (define the semantic here); `S` = secondary binding. Roles are from [`../../PLAN.md`](../../PLAN.md) §3. Target and change type are filled in once this surface is verified against the current upstream revision — see [`../../PLAN.md`](../../PLAN.md) §6.

| Addition (R1.0) | Role | Target | Change type | Confidence |
| --- | :-: | --- | --- | --- |
| [ADD-014](../../additions/aamp/ADD-014-accreditation-io-and-settlement.md) · Accreditation, IO & settlement | `P` | | | unverified |
| [ADD-015](../../additions/adcp/ADD-015-ooh-planning-metrics.md) · OOH planning metrics | `P` | | | unverified |
| [ADD-003](../../additions/adcp/ADD-003-delayed-play-confirmation.md) · Delayed play confirmation | `S` | | | unverified |
| [ADD-005](../../additions/adcp/ADD-005-location-disclosure-tiers.md) · Location disclosure tiers | `S` | | | unverified |
| [ADD-006](../../additions/adcp/ADD-006-creative-format-constraints.md) · Creative format constraints | `S` | | | unverified |
| [ADD-008](../../additions/adcp/ADD-008-creative-approval-lifecycle.md) · Creative approval lifecycle | `S` | | | unverified |
| [ADD-010](../../additions/adcp/ADD-010-dynamic-creative-authorisation.md) · Dynamic creative authorisation | `S` | | | unverified |
| [ADD-011](../../additions/adcp/ADD-011-compliance-declarations.md) · Compliance declarations | `S` | | | unverified |
| [ADD-013](../../additions/adcp/ADD-013-deal-access-and-response-obligation.md) · Deal access & response obligation | `S` | | | unverified |

## Open questions

- How far does Agentic Direct already model a negotiation with holds and lead times?
  If it does, OOH may need little more than vocabulary.
- Is physical fulfilment (print, logistics, installation) in scope for AAMP at all,
  or does the protocol stop at the booking?
