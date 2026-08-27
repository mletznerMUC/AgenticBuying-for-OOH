# AAMP — Trust and Transparency

> Status: **stub** — targets identified, mapping not yet written.
> Component scope below is from public sources as of August 2026 and needs
> verification against the current revision.

The Trust and Transparency pillar is where OOH's delivery-evidence problem belongs:
distinguishing what was played from what was seen, and making both auditable.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Delivery evidence | Proof-of-play logs, their integrity, and who attests to them |
| Modelled vs verified | Explicit labelling of plays (observed) versus contacts (modelled) versus independently verified figures |
| Third-party verification | Independent playout auditing and measurement verification |
| Discrepancy handling | Under-delivery, screen downtime, reconciliation, make-goods, credits |
| Static OOH evidence | Installation proof and photographic posting reports as first-class delivery evidence |
| Supply-chain transparency | Who owns the screen, who sold it, and what fees sit in between |
| Agent accountability | Which agent made a booking decision, and against which constraints |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 03 Audience, 06 Delivery,
parts of 08 Compliance.

## Mapping table

`P` = this surface is the addition's primary home (define the semantic here); `S` = secondary binding. Roles are from [`../../PLAN.md`](../../PLAN.md) §3. Target and change type are filled in once this surface is verified against the current upstream revision — see [`../../PLAN.md`](../../PLAN.md) §6.

| Addition (R1.0) | Role | Target | Change type | Confidence |
| --- | :-: | --- | --- | --- |
| [ADD-001](../../additions/ADD-001-total-audience-impressions.md) · Total Audience Impressions | `S` | | | unverified |
| [ADD-002](../../additions/ADD-002-play-chain-and-player-model.md) · Play chain / player model | `S` | | | unverified |
| [ADD-003](../../additions/ADD-003-delayed-play-confirmation.md) · Delayed play confirmation | `S` | | | unverified |
| [ADD-008](../../additions/ADD-008-creative-approval-lifecycle.md) · Creative approval lifecycle | `S` | | | unverified |
| [ADD-009](../../additions/ADD-009-creative-integrity-and-caching.md) · Creative integrity & caching | `S` | | | unverified |
| [ADD-010](../../additions/ADD-010-dynamic-creative-authorisation.md) · Dynamic creative authorisation | `S` | | | unverified |
| [ADD-011](../../additions/ADD-011-compliance-declarations.md) · Compliance declarations | `S` | | | unverified |
| [ADD-016](../../additions/ADD-016-seller-conformance-profile.md) · Seller conformance profile | `S` | | | unverified |

## Open questions

- What level of proof does the pillar currently expect for delivery, and can a
  batched, later-reconciled playout log meet it?
- Should photographic evidence be carried by the protocol or referenced?
- Who is the attesting party for an OOH play — the media owner, the player software,
  or an independent auditor?
