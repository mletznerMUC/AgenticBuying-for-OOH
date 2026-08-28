# AdCP 3.2 — findings

Source: `adcontextprotocol/adcp` at **3.2.0-beta.8**, read 2026-08-27. Paths below are
relative to that repository. Schemas were treated as normative.

## Structure, corrected

R1.0 recorded six AdCP domains. There are **eight**:

| Domain | R1.0 knew about it |
| --- | :-: |
| Media Buy | yes |
| Creative | yes |
| Signals | yes |
| Accounts | yes |
| Governance | yes |
| Trusted Match | yes |
| **Brand** | **no** |
| **Sponsored Intelligence** | **no** |

Additional surfaces R1.0 had no idea existed, and which turn out to matter:

- **`property/`** — a whole domain for inventory properties: property lists,
  per-property features, delivery records, `validate_property_delivery`.
- **`pricing-options/`** — twelve pricing models as separate schemas.
- **`extensions/`** — a first-class, versioned extension mechanism.
- **`compliance/`**, **`content-standards/`**, **`registries/`**, **`collection/`**.

## Finding 1 — AdCP already knows about OOH

`static/schemas/source/enums/channels.json` carries **both** OOH channels:

| Value | Description |
| --- | --- |
| `dooh` | "Digital out-of-home screens in public spaces" |
| `ooh` | "Classic out-of-home (physical billboards, transit, etc.)" |

And OOH identity is modelled throughout:

| Where | What |
| --- | --- |
| `enums/property-type.json` | `dooh` — "Digital out-of-home screen networks, identified by network/venue IDs" |
| `enums/device-type.json` | `dooh` |
| `enums/identifier-types.json` | `venue_id`, `screen_id`, **`openooh_venue_type`** |
| `enums/available-metric.json` | `dooh_metrics`, `ooh_metrics` container tokens |

## Finding 2 — the play/impression distinction already exists

This was the core of ADD-001 and ADD-002.

`enums/forecastable-metric.json`, on `plays`:

> "Number of times the ad creative is displayed on a DOOH screen or played in a loop.
> **Raw play count before any impression multiplier is applied.** Use alongside
> impressions or measured_impressions when buyers need both the play count and the
> multiplied audience figure."

`core/delivery-metrics.json` repeats it for delivery, and adds a full `dooh_metrics`
object:

| Field | Meaning |
| --- | --- |
| `loop_plays` | Times played in rotation |
| `screens_used` | Unique screens displaying the ad |
| `screen_time_seconds` | Total display time |
| `sov_achieved` | Actual share of voice delivered (0.0–1.0) |
| `venue_breakdown` | Per-venue performance breakdown |
| `calculation_notes` | Row-level methodology notes for DOOH impression calculation |

`measured_impressions` exists alongside `impressions`, distinguishing "the ad-server
delivery count" from "the third-party currency count", with a `measurement_source`.

**So the fan-out that ADD-002 proposed to invent is largely present on the delivery
side.** What is absent is the *forecast* fan-out at bid time.

## Finding 3 — classic OOH is present, experimentally

R1.0's largest declared gap ("no classic OOH anywhere") is wrong.
`core/delivery-metrics.json` has an experimental `ooh_metrics`:

> "Classic (static) OOH metrics — printed bulletins, posters, transit, and street
> furniture... Experimental in AdCP 3.2. Static units have no play event: the delivery
> number is a period-level modeled audience estimate whose methodology tier is declared
> in `estimation_basis`... and the settlement artifact is the **posting record** — it
> proves the posting period, not an airing."

It carries `panels[]`, each with multiple `identifiers` and an `id_type` of `geopath`,
`route_frame`, `plant_face` or `other` — noting that OOH contracts key line items on
the measurement-currency panel number *and* the operator's panel number together.

`core/product.json` also has **`material_submission`** — "Instructions for submitting
physical creative materials (print, static OOH, cinema)... Never auto-submit without
human confirmation."

## Finding 4 — share of voice already exists

This was the heart of ADD-015. `pricing-options/flat-rate-option.json` carries a
`DoohParameters` object:

| Field | Meaning |
| --- | --- |
| `sov_percentage` | **Guaranteed share of voice as a percentage (0–100)** |
| `loop_duration_seconds` | Duration of the ad loop rotation |
| `min_plays_per_hour` | Minimum plays per hour guaranteed |
| `venue_package` | Named collection of screens included in this buy |
| `duration_hours` | Duration of the DOOH slot |
| `daypart` | Named daypart |
| `estimated_impressions` | Estimated audience impressions (informational, not a guarantee) |

`pricing-options/cpp-option.json` covers cost per point (GRP). And
`pricing-options/time-option.json` prices per `hour`/`day`/`week`/`month` with
`min_duration`/`max_duration` — **which is exactly the classic-OOH "panel per booking
period" model that [`../ooh-specifics/02-trading-and-pricing-models.md`](../ooh-specifics/02-trading-and-pricing-models.md)
claims cannot be expressed.** That claim needs correcting.

## Finding 5 — creative approval and its reason codes already exist

The R1.0 release notes called the rejection reason taxonomy "the single most important
unknown". It is not unknown — it is specified.

`enums/creative-approval-status.json`: `pending_review`, `approved`,
**`partially_approved`** ("eligible in some but not all scopes; requires inspection of
`approval_scopes`"), `rejected` (with `rejection_reason`).

`partially_approved` with `approval_scopes` maps neatly onto per-landlord and
per-screen OOH approval, which is a better fit than anything ADD-008 proposed.

`enums/creative-event-reason-code.json` has **17** codes, including `review_failure`,
`processing_failure`, `seller_rereview`, **`policy_revocation`** ("seller
content-policy decision applied after initial approval" — ADD-008's revocation
requirement), `content_drift`, `takedown_request`, `advertiser_request`,
`identity_authorization_revoked`, `identity_authorization_expired`.

Those last two are notable: **an authorisation-with-expiry concept already exists** for
identity and post references. ADD-010 should model on it rather than invent one.

## Finding 6 — the negotiation and order layer is in AdCP, not only AAMP

R1.0's plan assigned brief → offer → order to AAMP Agentic Direct. AdCP Media Buy has
the whole flow:

`request_proposals`, `refine_proposals`, `accept_proposal`, `decline_proposals`,
`buy_products`, `control_media_buy`, plus `proposal-budget-constraint.json`,
`proposal-refinement.json`, `product-refinement.json`, `outcome-target.json`.

`media-buy/commercial-terms.json` — "Complete typed commercial envelope for a
compact-lifecycle proposal. This is the authoritative audit and refinement snapshot" —
carries `invoice_recipient` (a `business-entity`), `purchase_order_ref`,
`agency_estimate_number`, `cancellation_terms` (with `effective_at` and fee),
`reporting_commitments`, `pacing`, `budget_allocation`, `daily_budget_cap`.

**`invoice_recipient` directly matches Ströer's advertiser/agency/DSP election**
(ADD-014). `enums/billing-party.json` exists too.

`core/product.json` additionally carries `cancellation_policy`, `creative_policy`,
`enforced_policies`, `measurement_terms` (billing measurement + makegood policy),
`performance_standards`, `reporting_capabilities`, `installments` and `exclusivity`.

## Finding 7 — coordinated placements ≈ sync groups

`formats/canonical/coordinated_placements.json` (experimental, `since_version: 3.2`):

> "One creative manifest atomically supplies assets for multiple declared product
> placements."

`components[]` (min 2), each with `component_id`, `placement_ref`, **`required`**
(boolean — the all-or-nothing semantic ADD-007 asked for), `sequence`,
`serving_policy`, `canvas_constraints`, and a format binding.
`composition_model: deterministic`. Plus `shared_slots` for assets consumed by several
components.

This is ADD-007, already drafted, by someone else, for the general case. Our
contribution becomes validating it against real DOOH sync groups and supplying the
missing role semantics.

## Finding 8 — the extension mechanism is first-class and versioned

`extensions/extension-meta.json` defines how extensions work:

- Extension data lives at **`ext.{namespace}`**; `core/product.json` has an `ext` field.
- Each extension is a file at `/schemas/extensions/{namespace}.json`.
- It declares **`valid_from`** (minimum AdCP version, e.g. `"2.5"`) and optional
  `valid_until`, plus a `docs_url`.
- Extensions are **auto-discovered** and included in versioned schema builds by
  version range.

This settles the strategy question that [`../PLAN.md`](../PLAN.md) §1 left open and
that [`../mapping/adcp/README.md`](../mapping/adcp/README.md) posed. There is a
supported, versioned, discoverable way to ship an `ooh` namespace — and it carries its
own compatibility metadata, which happens to line up with our own versioning scheme.

## Finding 9 — exclusivity exists, but is not loop separation

`enums/exclusivity.json`: `none`, `category` ("only one advertiser per industry
category"), `exclusive` ("sole sponsorship").

This is **product-level** exclusivity. ADD-012 is about a **capacity cap within a
loop** — how much of a rotation one advertiser may hold — which `exclusivity` cannot
express. Adjacent prior art, not a substitute. ADD-012 stands as a confirmed gap.

## Finding 10 — capability discovery exists

`get_adcp_capabilities` is a task, and measurement methodology is declared on
`get_adcp_capabilities.measurement.metrics[]`, "discoverable once and inherited across
delivery rows". `adagents.json` and a `registries/` domain exist.

ADD-016 therefore does not need a new mechanism; it needs OOH conformance claims
declared inside the existing one.
