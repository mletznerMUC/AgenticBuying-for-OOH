# AAMP — Buyer, Seller and Registry Agents

> Status: **stub** — targets identified, mapping not yet written.
> Component scope below is from public sources as of August 2026 and needs
> verification against the current revision.

The Buyer Agent, Seller Agent and Registry Agent repositories provide reference
implementations and discovery patterns. For OOH the question is how a media owner
advertises what it can actually do, and how a buying agent finds it.

## Candidate target surfaces

| Surface | OOH work |
| --- | --- |
| Registry entries | Media owners, screen networks and specialists as discoverable counterparties, with the markets and geographies they cover |
| Seller capability advertisement | Which trading units, targeting dimensions, booking flows, reporting granularity and clearance workflows a seller supports |
| Buyer agent expectations | What an OOH-capable buying agent must be able to reason about (capacity, lead times, holds, clearance) |
| Reference implementation | An OOH seller agent example, to prove the extensions are implementable |

## Requirements this surface must carry

From [`../../ooh-specifics/`](../../ooh-specifics/): 01 Inventory, 02 Trading,
07 Booking.

## Mapping table

`P` = this surface is the addition's primary home (define the semantic here); `S` = secondary binding. Roles are from [`../../PLAN.md`](../../PLAN.md) §3. Target and change type are filled in once this surface is verified against the current upstream revision — see [`../../PLAN.md`](../../PLAN.md) §6.

| Addition (R1.0) | Role | Target | Change type | Confidence |
| --- | :-: | --- | --- | --- |
| [ADD-016](../../additions/ADD-016-seller-conformance-profile.md) · Seller conformance profile | `P` | | | unverified |
| [ADD-004](../../additions/ADD-004-venue-and-network-taxonomy.md) · Venue & network taxonomy | `S` | | | unverified |
| [ADD-014](../../additions/ADD-014-accreditation-io-and-settlement.md) · Accreditation, IO & settlement | `S` | | | unverified |

## Open questions

- Is there an existing capability-declaration mechanism we can extend, or do OOH
  capabilities need a new descriptor?
- Should we build a reference OOH seller agent as part of this work? It is the most
  convincing argument to a working group that the extensions are workable.
