---
id: ADD-003
title: Delayed Play Confirmation and Settlement Latency
version: 0.2.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Ströer PPV Implementation Guide v6, §4 and §9"
targets:
  adcp: [media-buy]
  aamp: [artf, trust-and-transparency]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
protocol_ownership:
  owner: adcp
  secondary: [aamp]
upstream_status: partial
verified_against:
  adcp: 3.2.0-beta.8
  aamp: "agentic-direct/OpenDirect-2.1; ARTF/OpenRTB-2.6"
  date: 2026-08-27
---

# ADD-003 — Delayed Play Confirmation and Settlement Latency

> Version 0.2.0 · Status: `draft` · Since `R1.0`
>
> **Protocol owner: AdCP** · also binds into AAMP
>
> 🟡 **Verified partially exists upstream** against AdCP 3.2.0-beta.8 and AAMP (OpenDirect 2.1 / OpenRTB 2.6) on 2026-08-27.

## Verification

OpenRTB 2.6 `Imp.dt` covers the bid-time expectation of when a play occurs. A declared confirmation-latency distribution and provisional/final labelling remain absent.

Full evidence: [`../verification/verdicts.md`](../../verification/verdicts.md) · [`../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) · [`../verification/aamp.md`](../../verification/aamp.md)


## Problem

In DOOH the creative is pre-loaded onto players, sometimes well in advance, because
players have "slow, unreliable, restricted or even no direct access to the internet"
and cannot tolerate stutter. Confirmation of a play therefore arrives **up to 10
minutes** after the bid response; Ströer states 80% arrive within 3 minutes.

Every pacing, budget-control and reporting mechanism in programmatic assumes
confirmation is effectively immediate. The consequence is stated bluntly in Ströer's
best-practice guidance: do not use ASAP pacing. A buyer agent optimising on a
feedback loop that is minutes stale — and unbounded at the tail — will overspend.

The latency is not an implementation defect. It is a property of the medium, and it
must be declared rather than discovered.

## Semantic definition

1. A seller MUST declare its **play confirmation latency** as a distribution, not a
   single number: at minimum a typical value and a maximum.
2. A seller MUST declare whether a play that is never confirmed is billed. (It must
   not be.)
3. Delivery figures MUST be labelled **provisional** or **final**, and a seller MUST
   declare when provisional figures become final.
4. A buyer agent MUST NOT treat absence of confirmation within the typical latency as
   non-delivery.
5. A seller MUST declare which party performs pacing. Where the seller paces (as in
   programmatic guaranteed), the buyer's own pacing MUST NOT be the binding control,
   and the protocol MUST make that explicit rather than leaving both sides to pace
   independently.
6. Where a buyer is obliged to respond to every opportunity (see **ADD-013**), that
   obligation MUST be declared together with the pacing responsibility, since the two
   only make sense together.

## Programmatic binding

**Today (Ströer):**

- Latency stated in prose: up to 10 minutes, 80% under 3 minutes.
- Pacing guidance in prose: even pacing, never ASAP.
- For programmatic guaranteed, "Pacing by SSP; DSP to bid on every bid request with
  valid bid".
- Confirmation arrives via the VAST impression URL carrying `${TOTAL_IMP}`; the
  aggregation from slave players happens inside Ströer SSP.
- The DSP onboarding plan tests DSP pacing explicitly for overspend on a UAT private
  auction.

**Proposed:** latency and pacing ownership become declared properties of the
inventory or deal, readable before bidding, rather than tribal knowledge transmitted
through a "DooH checklist" from a DSP representative — which is how Ströer's own
best-practice section says buyers should obtain it.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- the confirmation latency distribution, so it can set its own control loop;
- who paces, and therefore what the agent is responsible for;
- when delivery figures settle, and how long provisional figures may move;
- the reconciliation and invoicing timetable (see **ADD-014**), which is the outer
  bound on settlement.

Sketch:

```json
{
  "delivery_timing": {
    "confirmation_latency": { "typical_seconds": 180, "max_seconds": 600, "p80_seconds": 180 },
    "unconfirmed_plays_billed": false,
    "figures_final_after": "P3D",
    "pacing_owner": "seller",
    "buyer_must_respond_to_all_opportunities": true
  }
}
```

For an IO buy the same object answers a different question — how long after the
flight ends the numbers stop moving — which is exactly what a buyer agent needs in
order to know when it may close the campaign out.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Media Buy → product / offer | `new-object` | Delivery-timing declaration |
| AdCP | Media Buy → delivery reporting | `add-field` | `provisional` / `final` labelling and settle-by time |
| AdCP | Media Buy → pacing | `clarify-semantics` | Pacing ownership; buyer pacing is advisory when the seller paces |
| AAMP | ARTF | `add-field` | Confirmation latency on the opportunity or deal |
| AAMP | Trust and Transparency | `add-field` | Provisional vs final delivery state |

## Partial conformance

- MAY omit percentile detail and declare only typical and maximum.
- MAY omit `figures_final_after` where reconciliation is contractual rather than
  scheduled — but MUST reference the contract term instead.
- MUST NOT omit `pacing_owner`. Ambiguous pacing ownership causes overspend, which is
  the concrete harm this addition exists to prevent.

## Open questions

- [ ] Is 10 minutes a hard timeout, or the observed tail? What happens to a
      confirmation that arrives after it?
- [ ] Are unconfirmed plays ever billed, and how are they reported?
- [ ] Does the latency differ by network — an elevator screen and a roadside screen
      are unlikely to have the same connectivity profile.
- [ ] Should provisional/final labelling be a general AdCP reporting concept rather
      than an OOH addition? It would benefit other latent-delivery channels.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §2
- Ströer PPV Implementation Guide v6, §4 (Impression reporting / billing notification
  delays; Pacing & ooH Latency), §4.1 (Fig. 1), §9 (Pace carefully; Request a DooH
  checklist)
- DSP Integration Ströer SSP, "Pacing", "DSP Pacing"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.2.0 | 2026-08-27 | Verified against AdCP 3.2.0-beta.8 and AAMP; added protocol ownership and upstream status |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer PPV v6 analysis |
