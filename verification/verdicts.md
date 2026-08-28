# Verdicts

Each R1.0 addition checked against AdCP 3.2.0-beta.8 and AAMP (Agentic Direct /
OpenDirect v2.1, ARTF / OpenRTB 2.6), 2026-08-27.

| Verdict | Meaning |
| --- | --- |
| **exists** | Upstream already covers the requirement. Our work is conformance, mapping and migration guidance — not a proposal. |
| **partial** | Substantial prior art. The ask shrinks to a specific field, enum value or clarification. |
| **gap** | Confirmed absent from both protocols. This is where the value is. |

## Summary

| ID | Addition | Owner | Verdict | What the ask becomes |
| --- | --- | :-: | :-: | --- |
| ADD-001 | Total Audience Impressions | **AAMP** | `exists` | Migration guidance: `imp.ext.totalaud` → OpenRTB 2.6 `Imp.Qty`; settled-figure provenance on the AdCP side |
| ADD-002 | Play chain / player model | **AdCP** | `partial` | Forecast-side fan-out; delivery side already exists |
| ADD-003 | Delayed play confirmation | **AdCP** | `partial` | Latency declaration + provisional/final labelling |
| ADD-004 | Venue & network taxonomy | **AAMP** | `exists` | Migration to `Dooh.venuetype`; only the commercial *network* concept is unmet |
| ADD-005 | Location disclosure tiers | **AdCP** | **`gap`** | Full proposal — nothing upstream |
| ADD-006 | Creative format constraints | **AdCP** | `partial` | DOOH format family, `restricted_motion`, landlord reason class |
| ADD-007 | Sync groups | **AdCP** | `exists` | Validate `coordinated_placements` for DOOH; add role semantics |
| ADD-008 | Creative approval lifecycle | **AdCP** | `partial` | SLA and earliest-achievable-start only; states and reason codes exist |
| ADD-009 | Creative integrity & caching | **AdCP** | **`gap`** | Integrity policy + one reason-code value |
| ADD-010 | Dynamic creative authorisation | **AdCP** | `partial` | Model on the existing identity-authorisation pattern |
| ADD-011 | Compliance declarations | **AdCP** | `partial` | Buyer-facing declaration status; policy machinery exists |
| ADD-012 | Advertiser loop separation | **AdCP** | **`gap`** | Capacity cap within a loop — `exclusivity` cannot express it |
| ADD-013 | Deal access & response obligation | **AdCP** | **`gap`** | Prerequisites with buyer-specific status; response obligation |
| ADD-014 | Accreditation, IO & settlement | **AAMP** | `exists` | Order objects exist; only prerequisite *status* is unmet |
| ADD-015 | OOH planning metrics | **AdCP** | `partial` | GRP/OTS/dwell as brief targets; `unmet_brief_targets` |
| ADD-016 | Seller conformance profile | **AdCP** | `partial` | Declare OOH claims inside `get_adcp_capabilities` |

Owner = the protocol that should carry the **definition**. Most additions still bind
into both; see each addition's `protocol_ownership` front matter.

## Detail

### ADD-001 — `exists` · owner AAMP

OpenRTB 2.6 `Imp.Qty` carries `multiplier` (double), `sourcetype`
(`DOOHMultiplierMeasurementSourceType`) and `vendor`. AdCP carries `plays` vs
`impressions` vs `measured_impressions` with `measurement_source`, and
`measurement_terms.billing_measurement`.

Ströer's `imp.ext.totalaud` is a **pre-2.6 workaround**, not a standards gap. The
remaining unmet piece is small: the *settled* figure is still macro-delivered and has
no provenance at settlement time.

→ [`aamp.md`](aamp.md) §1, [`adcp-3.2.md`](adcp-3.2.md) §2

### ADD-002 — `partial` · owner AdCP

`delivery-metrics.dooh_metrics` already reports `loop_plays`, `screens_used`,
`screen_time_seconds`, `sov_achieved` and `venue_breakdown`, and `plays` is explicitly
"raw play count before any impression multiplier". The delivery half of the chain is
done. **The forecast half is not**: nothing declares expected fan-out before the buy.

### ADD-003 — `partial` · owner AdCP

OpenRTB 2.6 `Imp.dt` gives the bid-time expectation of when a play will occur. Nothing
declares a confirmation-latency distribution, and nothing labels delivery figures
provisional versus final. Both survive as asks — and both generalise beyond OOH.

### ADD-004 — `exists` · owner AAMP

`Dooh.venuetype` + `venuetypetax`, defaulting to the OpenOOH Venue Taxonomy;
AdCP `property-type: dooh` and `identifier-types: venue_id | screen_id |
openooh_venue_type`. The taxonomy problem is solved.

What is **not** solved: the seller's **commercial network** as a first-class grouping
with a published mapping to venue types. `Dooh.id` ("placement or logical grouping")
is the nearest thing and carries no name or mapping.

### ADD-005 — **`gap`** · owner AdCP

Searched both protocols: no concept of a negotiated location-disclosure tier, no
attribute manifest, nothing tying disclosure fidelity to price or to reporting
granularity. **Confirmed absent.** Proceed as a full proposal.

### ADD-006 — `partial` · owner AdCP

`core/product.json` has `creative_policy` and `material_submission` (explicitly for
"print, static OOH, cinema"). `formats/canonical/` has image, video and display
families. Missing: a DOOH format family with exact duration and orientation, a
`restricted_motion` (cinemagraph) form, and any way to say *why* a form is excluded —
the landlord reason class.

### ADD-007 — `exists` (experimental) · owner AdCP

`formats/canonical/coordinated_placements.json`, `since_version: 3.2`: `components[]`
with `required`, `sequence`, `placement_ref`, `composition_model: deterministic`, and
`shared_slots`. `required` gives all-or-nothing win semantics.

Our contribution changes character entirely: **validate an experimental format against
real DOOH sync groups**, and supply role semantics (primary/companion). That is
feedback a maintainer of an experimental feature actively wants.

### ADD-008 — `partial` · owner AdCP

`creative-approval-status` (`pending_review`, `approved`, `partially_approved`,
`rejected`) plus 17 `creative-event-reason-code` values including `policy_revocation`.
`partially_approved` + `approval_scopes` fits per-landlord OOH approval better than
what ADD-008 proposed.

Remaining ask is narrow: **declare the SLA** (max/typical) and the derived earliest
achievable start. `OpenDirect.Product.leadtime` is the analogous field on the direct
side.

R1.0 called the reason taxonomy "the single most important unknown in this release".
It is specified upstream. That blocker is largely dissolved.

### ADD-009 — **`gap`** · owner AdCP

No integrity, caching-authority or asset-swap concept in either protocol.
`content_drift` is adjacent but concerns landing pages, not the media file.
**Confirmed absent** — and cheap: an integrity-policy object plus one new reason-code
value.

### ADD-010 — `partial` · owner AdCP

`identity_authorization_revoked` and `identity_authorization_expired` prove an
**authorisation-with-expiry** concept already exists for identity and post references.
ADD-010 should generalise that pattern to asset mutation rather than invent a parallel
one. Reframing it this way makes it a much smaller, much more acceptable ask.

### ADD-011 — `partial` · owner AdCP

A `compliance/` domain, `content-standards/`, `enforced_policies` on the product, and
enums for `age-verification-method`, `age-determination-basis`, `attestation-claim`,
`consent-basis`. Substantial machinery.

Unmet: a buyer agent asking **"do I have the declarations this inventory requires, and
until when?"** before briefing.

### ADD-012 — **`gap`** · owner AdCP

`exclusivity` is `none | category | exclusive` at **product** level. ADD-012 is a
**capacity cap within a loop** — what share of a rotation one advertiser may hold.
Different concept, not expressible. **Confirmed absent**, and it is the constraint that
makes an SOV target achievable or not, so it blocks ADD-015 too.

### ADD-013 — **`gap`** · owner AdCP

`OpenDirect.Product.deliverytype` and AdCP `delivery_type` describe the *deal* type,
not the *prerequisites* to reach one. Nothing lets a buyer agent determine its own
eligibility before briefing, and nothing expresses a buyer-side obligation to respond
to every opportunity. **Confirmed absent.**

### ADD-014 — `exists` · owner AAMP

`OpenDirect.Order`, `Line`, `Account`, `ChangeRequest`, `Message` all exist, with
`Order.preferredbillingmethod`, `Product.leadtime`/`minspend`/`minflight`/`maxflight`,
and **`Line.reservedexpirydate`** (soft holds). AdCP `commercial-terms` adds
`invoice_recipient`, `purchase_order_ref` and `cancellation_terms`.

R1.0's plan called this "probably the most valuable single contribution in R1". That
was wrong: the order object exists in both protocols. What survives is one specific,
still-valuable thing — **prerequisites with buyer-specific status**, which merges into
ADD-013.

### ADD-015 — `partial` · owner AdCP

`flat-rate-option.DoohParameters` already carries `sov_percentage`,
`loop_duration_seconds`, `min_plays_per_hour`, `venue_package`, `duration_hours`,
`daypart`; `dooh_metrics.sov_achieved` reports against it; `cpp-option` covers cost per
point.

So **share of voice already exists** on the pricing side. Unmet: SOV/GRP/OTS/dwell as
*brief targets* with provenance, and the ability for an offer to state
`unmet_brief_targets` — which remains, on this evidence, absent from both protocols and
is the most valuable part of ADD-015.

### ADD-016 — `partial` · owner AdCP

`get_adcp_capabilities` exists, and measurement methodology is already declared on
`get_adcp_capabilities.measurement.metrics[]`. AAMP's registry-agent was not examined.
Ask becomes: declare OOH conformance claims inside the existing capability surface.

## Consequences for the plan

1. **The extension-strategy question is settled.** AdCP's `ext.{namespace}` mechanism
   is first-class, versioned (`valid_from`) and auto-discovered. Genuinely OOH-only
   concepts ship as a registered `ooh` namespace; the rest go to core.
2. **Four confirmed gaps carry the value** — ADD-005, ADD-009, ADD-012, ADD-013. They
   should be the first proposals, not the foundational-inventory bundle R1.0 planned,
   because the foundation already exists.
3. **ADD-014 drops out as a headline** and merges its surviving requirement into
   ADD-013.
4. **Two migration notes replace two proposals.** ADD-001 and ADD-004 become guidance
   for DOOH sellers on OpenRTB 2.5 → 2.6, which is arguably more immediately useful to
   Ströer than any upstream proposal.
5. **Two new findings are worth raising on their own**, independent of any addition:
   - Agentic Direct references the **DP-AA DOOH Extension** but implements none of it.
   - **ARTF and Agentic Direct disagree about whether DOOH exists** — ARTF has
     OpenRTB 2.6's `Dooh` object; Agentic Direct's object set has no DOOH placement at
     all.
6. **Read the DP-AA DOOH Extension before proposing anything to Agentic Direct.** It is
   now the highest-priority outstanding research item, ahead of the two blocked Ströer
   specs.
