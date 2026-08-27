---
id: ADD-010
title: Dynamic Creative Authorisation
version: 0.1.0
status: draft
since: R1.0
supersedes: []
superseded_by: null
origin: "Public Video Creative Approval (Dynamic Creative for DCO); v6 §8"
targets:
  adcp: [creative, accounts-and-governance]
  aamp: [agentic-direct, trust-and-transparency]
applies_to: [programmatic, io]
target_revision_checked: 2026-08-27
---

# ADD-010 — Dynamic Creative Authorisation

> Version 0.1.0 · Status: `draft` · Since `R1.0`

## Problem

Dynamic creative optimisation rotates the media file URL. The integrity model in
**ADD-009** classifies exactly that as fraud. The two requirements are in direct
conflict, and Ströer resolves it with a bespoke authorisation:

1. The buyer contacts Ströer Public Video Operations **at least three weekdays**
   before campaign start and declares compliance with trade and industry law, the
   regulatory authorities, and youth-protection law.
2. The buyer hands over **mockups and a concept**.
3. Ströer approves them and issues a **`DCO-ID` by e-mail**.
4. The buyer writes that DCO-ID **into the file name** of every DOOH creative file.
   Ströer reads it from the file name and serves from the advertiser's ad server
   instead of from cache.

This works, and it is the clearest example in the whole corpus of a concept with no
home in the protocol. An authorisation grant — a security capability — is transported
as a substring of a file name and issued over e-mail. There is no way for a buyer
agent to request it, check its status, discover its scope, or learn that it has
expired. A concept that gates whether a campaign can run at all is entirely outside
the machine-readable world.

## Semantic definition

1. Where a seller's integrity policy (**ADD-009**) prohibits asset mutation, the
   seller MUST declare whether an **authorisation** exists that permits it, and if so
   how it is obtained.
2. An authorisation MUST be a first-class object with: an identifier, a scope, a
   validity period, an issuer, and a status.
3. **Scope** MUST be explicit: which advertiser, campaign, creative set, inventory and
   date range the authorisation covers.
4. An authorisation MUST be **requestable and checkable** through the protocol. A
   human process behind it is acceptable; an opaque one is not — the buyer agent must
   be able to submit the request, see it pending, and see it granted or refused.
5. The seller MUST declare the **lead time** for authorisation, which composes with
   the approval SLA in **ADD-008**; the effective lead time is the maximum.
6. The seller MUST declare what the authorisation requires the buyer to supply
   (mockups, concept, compliance declaration — see **ADD-011**).
7. An authorisation reference MUST be carried in a field designated for it. It MUST NOT
   be embedded in a file name, URL path or other identifier whose declared purpose is
   something else.
8. An authorisation MUST be revocable, and revocation MUST be notifiable.

Requirement 7 is the crux. Requirements 4 and 8 are what make it usable by an agent
rather than by a person with an inbox.

## Programmatic binding

**Today (Ströer):**

- A `DCO-ID` string embedded in the media file name. Presence of the token is what
  switches Ströer from cache-serving to origin-serving.
- Issued by e-mail after a manual review of mockups and concept.
- Enrolment at least three weekdays before campaign start.
- Also referenced in v6 §8: "Swapping creative files on the VAST creatives commonly
  used for Dynamic Creative Rendering (DCR) requires prior case by case approval
  through Ströer Sales & Activation Management or Operations plus an issued valid
  access token."
- Reflected in the approval bucket assigned to the creative:
  `Dynamic Creative for DCO`.

**Proposed:** an authorisation object referenced explicitly from the creative, and a
task to request and check it. The file-name token can persist as a transport detail
for backwards compatibility, but it must stop being the authorisation's only
representation.

## Offer / IO binding

From an offer, a buyer agent MUST be able to determine:

- whether dynamic creative is permitted on this inventory at all;
- what the authorisation process requires and how long it takes;
- the composed lead time to campaign start, including approval (**ADD-008**);
- what the authorisation will cover, and what it will not;
- whether an existing authorisation can be reused for this offer.

Sketch:

```json
{
  "dynamic_creative": {
    "permitted": true,
    "requires_authorisation": true,
    "authorisation": {
      "lead_time": "P3D",
      "lead_time_basis": "weekdays",
      "requires": ["compliance_declaration", "mockups", "concept"],
      "scope_dimensions": ["advertiser", "campaign", "date_range"],
      "revocable": true,
      "issuer": "seller_operations"
    }
  }
}
```

Note `lead_time_basis: weekdays`: a three-weekday lead time requested on a Thursday
lands on the following Tuesday. A planning agent that treats it as 72 hours will
promise a start date the seller cannot honour. Business-day semantics have to be
explicit.

## Proposed placement

| Protocol | Surface | Change type | Notes |
| --- | --- | --- | --- |
| AdCP | Creative | `new-object` | Authorisation object: id, scope, validity, issuer, status |
| AdCP | Creative | `new-task` | Request an authorisation; check its status |
| AdCP | Creative | `add-field` | Authorisation reference on the creative |
| AdCP | Accounts / Governance | `clarify-semantics` | Authorisation as a compliance grant tied to declarations (**ADD-011**) |
| AAMP | Agentic Direct | `add-field` | Authorisation lead time as an offer/order term |
| AAMP | Trust and Transparency | `add-field` | Auditability: which authorisation permitted a given mutation |

## Partial conformance

- MAY keep a human review behind the request task — the process need not be automated,
  only observable.
- MAY omit `scope_dimensions` if authorisations are always advertiser-wide, but MUST
  then state that.
- MUST NOT carry the authorisation reference only inside a file name or URL.
- MUST NOT declare `permitted: true` without either an authorisation path or an
  explicit statement that none is needed.

## Open questions

- [ ] What is a DCO-ID's actual scope — advertiser, campaign, creative set? The source
      documents do not say.
- [ ] Does it expire?
- [ ] Can it be revoked mid-campaign, and how would the buyer learn?
- [ ] Is the "access token" in v6 §8 the same thing as the DCO-ID, or a second
      credential? The wording suggests they may differ.
- [ ] Should this generalise beyond DCO — is it really "authorisation to deviate from a
      seller policy", of which DCO is one case? A general shape would also cover
      category exceptions and content waivers.

## Sources

- `../analysis/stroeer-ppv-baseline.md` §8
- Public Video Creative Approval ("Dynamic Creative for DCO")
- Ströer PPV Implementation Guide v6, §8
- DSP Integration Ströer SSP, "Cashing & DCO Approval"

## Changelog

| Version | Date | Change |
| --- | --- | --- |
| 0.1.0 | 2026-08-27 | Initial draft from Ströer Creative Approval analysis |
