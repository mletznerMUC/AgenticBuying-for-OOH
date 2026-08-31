---
id: ADD-011
title: Compliance Declarations and Youth Protection
version: 0.2.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "v6 Appendix (Accreditation); Public Video Creative Approval (DCO enrolment)"
targets:
  adcp: [accounts-and-governance, creative]
  aamp: [agentic-direct, trust-and-transparency]
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

# ADD-011 — Compliance Declarations and Youth Protection

> Version 0.2.0 · Status: `draft` · Since `R1.0`
>
> **Protocol owner: AdCP** · also binds into AAMP
>
> 🟡 **Verified partially exists upstream** against AdCP 3.2.0-beta.8 and AAMP (OpenDirect 2.1 / OpenRTB 2.6) on 2026-08-27.

## Verification

A `compliance/` domain, `enforced_policies`, and age-verification and attestation enums already exist. Unmet: a buyer agent checking its own declaration status before briefing.

Full evidence: [`../verification/verdicts.md`](../../verification/verdicts.md) · [`../verification/adcp-3.2.md`](../../verification/adcp-3.2.md) · [`../verification/aamp.md`](../../verification/aamp.md)


## Problem

Before a buyer may run anything on Ströer public screens, it must **declare** that it
will comply with "provisions of trade and industry law, the regulatory authorities and
the requirements of the laws for the protection of youths". This declaration is
required at accreditation, and again at DCO enrolment.

This is not brand safety. It is the inverse: a public screen is seen by everyone who
walks past, including minors, none of whom consented to anything. The legal exposure
runs to the media owner and, through the landlord, to the site. So the seller extracts
a binding declaration from the buyer, and gates access on it.

In an agentic world this becomes urgent rather than administrative. If an autonomous
agent books and delivers a campaign, who made the declaration? An agent cannot
meaningfully warrant compliance with youth-protection law. The declaration has to
attach to an accountable legal entity, and the protocol has to carry that binding —
otherwise the entire compliance model of public-space advertising has no anchor.

Today the declaration is paperwork, held out of band, invisible to any system.

## Semantic definition

1. Inventory MUST be able to declare the **declarations required** before a buyer may
   transact or deliver on it.
2. A declaration MUST identify: its subject matter, the jurisdiction and legal basis it
   references, the accountable party, and its validity period.
3. The **accountable party MUST be a legal entity**, not an agent, a seat, or a
   software system. Where an agent acts, the declaration MUST record the entity on
   whose behalf it acts.
4. A seller MUST be able to verify that a required declaration is on file before
   accepting a transaction, and a buyer agent MUST be able to check its own standing
   **before** briefing — so that "you are not accredited for this inventory" is
   discoverable rather than a surprise at booking.
5. Declarations MUST be referenceable from the objects they gate: the account, the
   order, the creative, and any authorisation (**ADD-010**).
6. Where a declaration concerns the protection of minors, the seller MUST be able to
   express the associated **content constraints** in machine-readable form, not only as
   an obligation the buyer asserts. An assertion is not a control.
7. Declarations MUST be revocable and expirable, and their withdrawal MUST invalidate
   the access they gate.

Requirement 6 is where this addition goes beyond Ströer's practice. Ströer obtains a
promise; an agentic protocol should also be able to state the rules that promise refers
to, so that a buyer agent can check its own creative against them rather than
attesting blindly.

## Programmatic binding

**Today (Ströer):** none. The declaration is part of accreditation paperwork and, for
DCO, part of an e-mail exchange. Nothing in the bid stream references it. Its effect is
visible only as access: an unaccredited buyer has no deal, and without a deal there are
no bid requests (**ADD-013**).

**Proposed:** a declaration record on the account, referenced by orders and creatives,
checkable through the protocol. The programmatic path does not need to carry the
declaration itself — only the assertion that it is satisfied for this deal.

## Offer / IO binding

This addition is primarily an offer/IO concern, and it is a gate on the whole
relationship rather than on a single buy.

From an offer — or before briefing at all — a buyer agent MUST be able to determine:

- which declarations this inventory requires;
- whether the buyer's principal has them on file, and until when;
- what each declaration commits the principal to, in referenceable terms;
- the content constraints that follow (age-restricted categories, proximity rules —
  see [`../ooh-specifics/08-compliance-and-content-restrictions.md`](../../ooh-specifics/08-compliance-and-content-restrictions.md));
- what it must do to obtain a missing declaration, and how long that takes.

Sketch:

```json
{
  "required_declarations": [{
    "id": "youth_protection",
    "subject": "protection_of_minors",
    "jurisdiction": "DE",
    "legal_basis": "<statute reference>",
    "accountable_party_type": "legal_entity",
    "status_for_buyer": "on_file",
    "valid_until": "2027-03-31",
    "gates": ["transaction", "delivery", "dynamic_creative_authorisation"],
    "content_constraints_ref": "<machine-readable ruleset>"
  }]
}
```

`status_for_buyer` is what makes this actionable: an agent can determine that it is not
yet accredited and escalate to a human **before** producing a plan that cannot execute.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Accounts | `new-object` | Declaration record on the account, with validity and accountable entity |
| AdCP | Governance | `new-object` | Machine-readable content constraints referenced by a declaration |
| AdCP | Governance | `clarify-semantics` | Location-bound rules protecting the public, distinct from brand suitability |
| AdCP | Creative | `add-field` | Declaration reference on submission |
| AAMP | Agentic Direct | `add-field` | Declarations as prerequisites in brief → offer → order |
| AAMP | Trust and Transparency | `new-object` | Accountability chain: which entity warranted what, and when |

## Partial conformance

- MAY omit `legal_basis` where the seller's requirement is contractual rather than
  statutory.
- MAY omit `content_constraints_ref` where the seller publishes only an obligation and
  no ruleset — this is the common case today.
- MUST NOT omit `accountable_party_type`, and MUST NOT accept an agent identity as the
  accountable party.
- MUST NOT gate access on a declaration the buyer cannot discover in advance.

## Open questions

- [ ] Which German statutes are referenced? The documents say "laws for the protection
      of youths" without citation.
- [ ] Can an agency declare on behalf of its clients, or is the declaration per
      advertiser?
- [ ] Does the declaration expire or need periodic renewal?
- [ ] **How should an autonomous agent's actions be covered by a human-warranted
      declaration?** This is a governance question well beyond schema design, and it
      needs the working groups rather than a mapping decision here.
- [ ] Should the content-constraint ruleset be OOH-specific, or shared with the wider
      Governance surface?

## Sources

- `../analysis/stroeer-ppv-baseline.md` §9
- Ströer PPV Implementation Guide v6, Appendix (Accreditation → Creative Compliance
  Declaration)
- Public Video Creative Approval (DCO enrolment → Enrollment and Compliance
  Declaration)

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.2.0 | 2026-08-27 | Verified against AdCP 3.2.0-beta.8 and AAMP; added protocol ownership and upstream status |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer accreditation analysis |
