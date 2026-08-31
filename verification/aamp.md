# AAMP — findings

Sources read 2026-08-27: `IABTechLab/AAMP` (hub), `IABTechLab/agentic-direct`,
`IABTechLab/agentic-rtb-framework`.

## Structure, confirmed

The hub README confirms the six component repositories R1.0 recorded, and the
versioning model: **independent semantic versioning per repository**, releases via
GitHub tags, cross-repository alignment by governance coordination. Contributions go to
the child repository; architectural proposals may start in the hub.

That last point is operationally useful: an OOH proposal spanning ARTF and Agentic
Direct should open in the **hub**, not in one child.

| Repository | What it actually is |
| --- | --- |
| `agentic-direct` | **OpenDirect v2.1** exposed as MCP tools + A2A agent, with AdCOM and OpenRTB objects |
| `agentic-rtb-framework` (ARTF) | v1.0 spec over **OpenRTB 2.6** protobuf; Go and Rust reference implementations |
| `buyer-agent`, `seller-agent`, `registry-agent-example` | Reference implementations — **not examined in this pass** |
| `agentic-audiences` | **Not examined in this pass** |

## Finding 1 — OpenRTB 2.6 already standardises the audience multiplier

This is the most consequential finding of the whole verification pass.

ARTF is built on the official OpenRTB 2.6 protobuf
(`proto/com/iabtechlab/openrtb/v2/openrtb.proto`). That specification contains
`Imp.Qty`:

```protobuf
// ...out-of-home and CTV, with an impression being a unique member of the
// audience viewing it. Therefore, a standard means of passing a multiplier
// in the bid request, representing the total quantity of impressions, is
// required. This object includes the impression multiplier, and describes
// the source of the multiplier value.
message Qty {
  // The quantity of billable events which will be deemed to have occurred
  // if this item is purchased. For example, a DOOH opportunity may be
  // considered to be 14.2 impressions. Equivalent to qtyflt in OpenRTB 3.0.
  optional double multiplier = 1;

  // The source type of the quantity measurement, ie. publisher.
  // Refer to enum ...DOOHMultiplierMeasurementSourceType
  optional int32 sourcetype = 2;

  // The top level business domain name of the measurement vendor providing
  // the quantity measurement.
  // REQUIRED ... if sourcetype is equal to 1.
  optional string vendor = 3;
}
```

Compare against what **ADD-001** proposed to add:

| ADD-001 requirement | OpenRTB 2.6 |
| --- | --- |
| Fractional audience count per opportunity | `Qty.multiplier` (double) — "may be considered to be 14.2 impressions" |
| Measurement provenance | `Qty.sourcetype` (`DOOHMultiplierMeasurementSourceType`) |
| Named measurement vendor | `Qty.vendor`, required when sourcetype is a vendor |

**Ströer's `imp.ext.totalaud` is a pre-2.6 workaround for a gap that has since been
closed.** The Ströer guide states it targets OpenRTB **2.5**, which predates `Qty`.

The practical consequence reverses our recommendation: for this part, the ask upstream
is not an extension. It is a **migration**, plus conformance guidance on mapping
`totalaud` → `Imp.Qty`.

## Finding 2 — OpenRTB 2.6 has a DOOH object with a venue taxonomy

`Imp` sits under a `Dooh` object that is a peer of `Site` and `App`:

```protobuf
// Out-Of-Home screen. A bid request with a DOOH object must not contain a
// site or app object.
message Dooh {
  optional string id = 1;            // placement or logical grouping of placements
  optional string name = 2;
  repeated string venuetype = 3;     // ...DOOHVenueType
  optional int32 venuetypetax = 4 [default = 1];   // ...DOOHVenueTaxonomy
  optional Publisher publisher = 5;
  optional string domain = 6;
  optional string keywords = 7;
  optional Content content = 8;
}
```

> "The taxonomy to be used is defined by the venuetax field. If no venuetax field is
> supplied, **The OpenOOH Venue Taxonomy is assumed.**"

So **ADD-004** is largely solved upstream: a venue type, an explicitly versioned
taxonomy field, and a placement-grouping `id`.

This also indicts the Ströer encoding precisely. A bid request with a `Dooh` object
*must not* contain a `site` object — yet Ströer puts a screen in `site` with a
synthetic `page` URL, because it is on 2.5. Migrating to 2.6 removes the synthetic
hostname problem (`../analysis/stroeer-ppv-baseline.md` §15) at a stroke.

`Dooh.id` — "placement or **logical grouping** of placements" — is also a candidate
home for the seller-network concept in ADD-004, though it does not carry a commercial
network name.

## Finding 3 — delivery timing is partly modelled

`Imp.dt`:

> "Timestamp when the item is estimated to be fulfilled (**e.g. when a DOOH impression
> will be displayed**) in Unix format."

Together with `Imp.exp`, this covers the *forward* half of ADD-003: the bid-time
expectation of when the play will occur. It does **not** cover the reverse half — a
declared confirmation-latency distribution, or provisional-versus-final labelling of
delivery figures. ADD-003 remains a partial gap, but a narrower one.

## Finding 4 — Agentic Direct is OpenDirect v2.1, and the order objects already exist

`agentic-direct/opendirect.json` is an MCP server manifest exposing OpenDirect v2.1.
Schemas present: `OpenDirect.Account`, `Order`, `Line`, `Product`, `Creative`,
`Assignment`, `Organization`, `Address`, `Contact`, **`ChangeRequest`**, `Message`,
`Placement`, `AdUnit`, plus AdCOM and OpenRTB objects. Tools cover full CRUD on each.

Against **ADD-014**, which proposed "the order as a first-class protocol object":

| ADD-014 requirement | OpenDirect v2.1 |
| --- | --- |
| An order object with parties and validity | `Order` — `accountid`, `publisherid`, `brand`, `budget`, `startdate`, `enddate`, `orderexpirydate`, `contacts` |
| Invoice recipient election | `Order.preferredbillingmethod` |
| Terms fixed by the order | `Line` — `ratetype`, `rate`, `quantity`, `cost`, `targeting` |
| Amendments | `ChangeRequest` — "Request to modify an existing order" |
| Buyer↔seller correspondence | `Message` |
| Lead time | `Product.leadtime` — "Days from today that line can begin" |
| Minimum commitments | `Product.minspend`, `minflight`, `maxflight` |
| **Soft holds** | **`Line.reservedexpirydate`** |

`Line.reservedexpirydate` is worth calling out: it answers the hold/option question
that [`../ooh-specifics/07-availability-and-booking-lifecycle.md`](../ooh-specifics/07-availability-and-booking-lifecycle.md)
raises and that R1.0 listed as uncovered.

`Product.deliverytype` enumerates `Exclusive`, `Guaranteed`, `PMP - Prioritized`,
`PMP - Non-prioritized`, `PMP - First Look`, `OpenRTB - Deal`,
`OpenRTB - Guaranteed Deal` — relevant to ADD-013's access model, though it describes
the *deal* type rather than the *prerequisites* to reach one.

`Product.ratetype`: `CPM`, `CPMV`, `CPC`, `CPD`, `FlatRate`. `CPD` (cost per day) and
`FlatRate` cover period-based OOH buying.

**So ADD-014's central ask is already met.** What survives is narrow and specific:
prerequisites with a *buyer-specific status* — the ability for a buyer agent to ask
"can I transact with you yet, and if not what is missing and how long does it take?".
Nothing in OpenDirect answers that.

## Finding 5 — OpenDirect references a DOOH extension that Agentic Direct does not carry

`opendirect.json` declares its `referencedSpecifications` as:

```json
["AdCOM", "OpenRTB", "DP-AA DOOH Extension"]
```

**A DOOH extension to OpenDirect exists as prior art** — and the Agentic Direct MCP
schema references it without implementing any of it. No schema, field or enum in the
repository mentions DOOH beyond that one string.

Two consequences:

1. We must find and read the DP-AA DOOH Extension before proposing anything to Agentic
   Direct, or we will duplicate it. This is now the highest-priority outstanding
   research item.
2. "Agentic Direct references a DOOH extension it does not implement" is itself a
   clean, well-evidenced contribution to open in the AAMP hub.

## Finding 6 — the Agentic Direct object set has no DOOH placement

`AdCOM.Device`, `AdCOM.Geo`, `AdCOM.Site`, `AdCOM.App` are present;
**there is no `AdCOM.DOOH` or `Dooh` object.** `OpenDirect.Placement` is
`{id, lineid, adunitid, creativespec}` — no venue, no screen, no loop.

So the direct/IO side of AAMP reproduces exactly the modelling error the Ströer
integration was forced into: a screen has to be described as a site or an ad unit. ARTF
has moved to 2.6 and has a `Dooh` object; Agentic Direct has not. **The two halves of
AAMP disagree about whether DOOH exists.**

That inconsistency, evidenced, is probably the strongest single thing we can take to
the AAMP hub.

## Not examined

`buyer-agent`, `seller-agent`, `registry-agent-example`, `agentic-audiences`. ADD-016's
placement and the Agentic Audiences half of ADD-001 and ADD-015 remain unverified, and
are marked as such.
