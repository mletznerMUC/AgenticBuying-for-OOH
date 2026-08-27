---
id: ADD-008
title: Creative Approval Lifecycle and SLA
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Public Video Creative Approval; v6 §8-§9; DSP Integration test plan"
targets:
  adcp: [creative, accounts-and-governance]
  aamp: [agentic-direct, trust-and-transparency]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-008 — Creative Approval Lifecycle and SLA

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Nothing plays on a Ströer public screen until it has passed both an automatic and a
**manual** human review: "Running DOOH .mp4 video- or .jpg/.png image-creatives in
public requires the application of special safety standards ... Only approved creatives
can broadcast in public."

Approval takes **up to 48 hours**. It is bound to the DSP creative ID. It can fail.
And it is a hard gate: an unapproved creative does not serve, no matter that the deal
is signed and the bid won.

Programmatic protocols model creative approval as an asynchronous formality that
resolves in seconds. Agentic protocols will inherit that assumption unless it is
challenged. The consequences for a buyer agent are concrete:

- A campaign cannot start less than two days after creative submission. An agent that
  books a flight starting tomorrow has produced an unexecutable plan.
- Approval status is reported through two unrelated channels — a separate REST API, or
  auction win/loss notifications — and the guide's own advice is to "reach out to your
  DSP representative to learn where to read the status information on your DSP user
  interface."
- The SLA is stated inconsistently in Ströer's own documents: 48 hours in the
  normative Creative Approval document, 24 hours in the best-practice section.
- Rejection reasons may not be machine-readable at all. The Pre-Approval API docs
  could not be retrieved (see `../analysis/open-gaps.md` §1), so this is unresolved.

## Semantic definition

1. Inventory MUST declare whether creative approval is **required before delivery**,
   and whether it includes human review.
2. Where approval is required, the seller MUST declare its **SLA** as a maximum
   duration, and SHOULD declare a typical duration.
3. Approval MUST have a defined state machine. The minimum states are
   `not_submitted`, `pending`, `approved`, `rejected`, `revoked`.
4. Approval is bound to a **creative identity**. The seller MUST declare what
   constitutes that identity (see **ADD-009**) and what changes invalidate an existing
   approval.
5. A rejection MUST carry a **machine-readable reason code** from a published
   taxonomy, plus optional human-readable detail. Prose alone is not conformant: a
   buyer agent must be able to decide whether to re-submit, alter the creative, or
   escalate to a human, without parsing free text.
6. Approval MAY be **revoked** after being granted. Sellers MUST support revocation
   notification, and buyers MUST handle it — a campaign can be stopped mid-flight by a
   landlord or an authority.
7. The seller MUST offer approval **ahead of campaign start**, decoupled from bidding,
   so that a scheduled start is achievable.
8. Approval lead time MUST compose with other lead times rather than replacing them.
   Where a separate authorisation is also required (see **ADD-010**), the effective
   lead time is the maximum of all applicable lead times, and the protocol MUST make
   both visible.
9. Status MUST be retrievable by the buyer on demand, not only pushed.

## Programmatic binding

**Today (Ströer):**

- Approval keyed on the DSP creative ID (`crid`). "Every creative must be tied to one
  DSP creative ID to pass Ströer SSP creative approval."
- Submission either through the Creative Pre-Approval API
  (`https://creative.api.adscale.de/v1/docs`, access token from a Ströer SSP
  representative, single and bulk submission and status calls) or implicitly by
  bidding.
- Status feedback via the Pre-Approval API or via auction win/loss notifications.
- Two approval buckets are assigned on approval: `Standard Creative with Caching`
  (default) or `Dynamic Creative for DCO` (see **ADD-010**).
- Onboarding test: a full round trip of rejection → re-submission → approval, with a
  token.

**Proposed:** approval state, SLA and reason taxonomy become part of the creative
object's lifecycle in the protocol, and the pre-approval submission becomes a defined
task rather than a vendor REST API discovered through a sales contact.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- that approval is required, and that it involves human review;
- the maximum and typical approval duration;
- the earliest achievable campaign start, given the current date and the approval SLA;
- the composed lead time including any authorisation process (**ADD-010**) and, for
  classic OOH, production and installation;
- what a rejection would mean for the flight, and whether inventory is held during
  re-submission.

Sketch:

```json
{
  "creative_approval": {
    "required": true,
    "human_review": true,
    "sla": { "max": "P2D", "typical": "P1D" },
    "pre_approval_available": true,
    "bound_to": "creative_identity",
    "revocable": true,
    "reason_codes_published": true,
    "earliest_start_from_submission": "P2D"
  }
}
```

`earliest_start_from_submission` is the field a planning agent actually needs. It is
derived, but deriving it is exactly the reasoning step that goes wrong when the inputs
are scattered across a PDF, a REST API and a sales e-mail.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Creative | `new-object` | Approval state machine on the creative; states, transitions, revocation |
| AdCP | Creative | `new-task` | Pre-approval submission and status, single and bulk |
| AdCP | Creative | `new-object` | Rejection reason-code taxonomy |
| AdCP | Media Buy → product / offer | `add-field` | Approval requirement, SLA, earliest achievable start |
| AdCP | Accounts / Governance | `clarify-semantics` | Approval as a location-bound compliance gate, not brand suitability |
| AAMP | Agentic Direct | `add-field` | Approval lead time as an offer and order term |
| AAMP | Trust and Transparency | `add-field` | Auditability of approval decisions and revocations |

## Partial conformance

- MAY omit `typical` and declare only `max`.
- MAY omit `pre_approval_available` if approval is synchronous (no OOH seller is).
- MUST NOT declare `required: true` without an SLA. An unbounded gate is not
  plannable.
- MUST NOT emit a rejection without a reason code once a taxonomy is published.
- MUST NOT bind approval to an identity whose definition is unpublished.

## Open questions

- [ ] **48 h or 24 h?** The source documents disagree. Recorded as 48 h; needs
      confirmation. (`../analysis/open-gaps.md` §2.1)
- [ ] Does the Pre-Approval API expose machine-readable rejection reason codes? This
      is the single most important unresolved question in release R1. (§1)
- [ ] Are approvals portable across deals, or scoped to one?
- [ ] Does approval expire?
- [ ] Is inventory held while a rejected creative is re-submitted?
- [ ] Should the reason-code taxonomy be OOH-specific or a general creative-rejection
      taxonomy? A general one would serve every channel with human review.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §6
- Public Video Creative Approval (also v6 Appendix B)
- Ströer PPV Implementation Guide v6, §8 (Creative Pre-Approval API), §9 (Consider
  creative approval delay)
- DSP Integration Ströer SSP, "Creative Pre-Approval Test", "Creative Approval"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer Creative Approval analysis |
