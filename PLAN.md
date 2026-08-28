# Plan — taking OOH additions into AdCP and AAMP

Scope: release **R1.0** (16 additions, see [`additions/REGISTRY.md`](additions/REGISTRY.md)).
Derived from analysis of Ströer's production DOOH integration standards
([`analysis/`](analysis/)).

This document answers three questions:

1. **Which protocol owns what?** AdCP and AAMP overlap; putting an addition in the wrong
   one wastes a submission.
2. **In what order?** Some additions are prerequisites for others being meaningful.
3. **How does this work for insertion-order buying**, not just programmatic — so that a
   buyer agent sending a brief can understand the offer it gets back?

---

## 1. The division of labour between AdCP and AAMP

The two protocols are not competitors for these additions; they sit at different
altitudes, and most additions need both.

| Layer | Owner | What belongs here |
| --- | --- | --- |
| **Product & offer** — what is for sale, described so an agent can plan | **AdCP** (Media Buy, Creative) | Inventory shape, format constraints, audience basis, approval lifecycle, planning forecasts |
| **Negotiation & order** — brief → offer → order, with human gates | **AAMP Agentic Direct** | The IO, prerequisites, lead times, negotiated terms |
| **Real-time transport** — one opportunity, one bid | **AAMP ARTF** | Per-opportunity fields: audience forecast, venue, sync group, response obligation |
| **Audience semantics** | **AAMP Agentic Audiences** | ID-free aggregate audience, currency provenance |
| **Discovery & capability** | **AAMP Registry / Seller Agent** | Network catalogue, conformance profile |
| **Verification** | **AAMP Trust & Transparency** | Plays vs contacts, provisional vs final, approval and mutation audit |

The practical rule we are applying:

> **Define the semantic once, at the offer layer in AdCP. Bind it down into ARTF for the
> real-time path and into Agentic Direct for the contracted path.**

The failure mode to avoid is what the source material already demonstrates: defining a
concept only in the transport, where it is invisible to any agent that has not yet bid.

### Where AdCP needs a decision from us first

[`mapping/adcp/README.md`](mapping/adcp/README.md) poses this and it now has to be
settled, because 12 of the 16 additions depend on the answer:

- **(a) channel extensions** — an `ooh` block on products, creatives and reports.
  Fastest to accept, least valuable, entrenches OOH as a special case.
- **(b) an OOH profile** — parallel objects reusing the envelope. Risks a second-class
  channel.
- **(c) generalise the core** — make the core less impression-first so OOH falls out
  naturally.

**Recommendation: (c) for the six additions that are not really OOH-specific, (a) for the
rest.** Six of these additions describe problems that exist in cinema, audio, TV and any
channel with human creative review or contracted access:

| Addition | Why it is not OOH-specific |
| --- | --- |
| ADD-003 Delayed confirmation | Any channel with latent delivery confirmation |
| ADD-008 Creative approval SLA | Any channel with human review before broadcast |
| ADD-011 Compliance declarations | Any channel where a legal entity must warrant compliance |
| ADD-014 Accreditation & IO | **All** contracted media buying |
| ADD-015 Planning metrics | Every reach-and-frequency channel |
| ADD-016 Conformance profile | Every agent-to-agent integration |

Arguing these as general improvements rather than OOH pleading is both more honest and
more likely to be accepted. ADD-014 in particular is probably the most valuable single
contribution in R1, and it is not an OOH addition at all — OOH is just where the gap is
impossible to ignore.

---

## 2. Prioritisation

Ranked by one criterion: **does its absence stop a buyer agent from producing an
executable plan?**

| Wave | Additions | Why now |
| --- | --- | --- |
| **1 — Describe the inventory** | ADD-001, ADD-004, ADD-006, ADD-013 | Without audience basis, venue type, format constraints and access model, an OOH product cannot be described at all. Everything else builds on these. |
| **2 — Make a brief answerable** | ADD-015, ADD-005, ADD-014, ADD-008 | The brief → offer path. Planning language, location fidelity, the contractual gate, and the approval lead time that determines the earliest possible start date. |
| **3 — Make execution correct** | ADD-002, ADD-003, ADD-007, ADD-012 | Prevents plans that look fine and then under-deliver: fan-out, pacing latency, sync groups, separation caps. |
| **4 — Integrity, governance, scale** | ADD-009, ADD-010, ADD-011, ADD-016 | Necessary for production trust, but a plan can be produced without them. |

### Dependencies

```
ADD-001 (audience basis) ──┬──> ADD-002 (fan-out decomposes the audience figure)
                           └──> ADD-015 (planning metrics vs settlement basis)

ADD-004 (venue/network) ───┬──> ADD-005 (disclosure tier scopes what venue data is given)
                           ├──> ADD-006 (format constraints are scoped per network)
                           └──> ADD-016 (network catalogue is part of capability discovery)

ADD-008 (approval) ────────┬──> ADD-009 (integrity exists to protect approval)
                           └──> ADD-010 (authorisation is an exception to integrity)

ADD-013 (access model) ────────> ADD-014 (prerequisites are the access gate in detail)

ADD-012 (separation cap) ──────> ADD-015 (the cap bounds achievable SOV)

ADD-003 (pacing owner) <───────> ADD-013 (response obligation only makes sense paired)
```

Two of these are hard couplings that must not be split across submissions:
**ADD-003 ↔ ADD-013** (pacing ownership and response obligation are incoherent apart) and
**ADD-008 → ADD-009 → ADD-010** (approval, the integrity model protecting it, and the
authorised exception to that model are one story).

---

## 3. Full placement matrix

`P` = primary home (define the semantic here). `S` = secondary binding.

| Addition | AdCP Media Buy | AdCP Creative | AdCP Accts/Gov | AAMP ARTF | AAMP Direct | AAMP Audiences | AAMP Registry | AAMP Trust | Wave |
| --- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| ADD-001 Total Audience Impressions | **P** | | | S | S | S | | S | 1 |
| ADD-002 Play chain | **P** | | | S | | | | S | 3 |
| ADD-003 Delayed confirmation | **P** | | | S | S | | | S | 3 |
| ADD-004 Venue & network taxonomy | **P** | | | S | | | S | | 1 |
| ADD-005 Disclosure tiers | **P** | | S | S | S | | | | 2 |
| ADD-006 Format constraints | S | **P** | S | S | S | | | | 1 |
| ADD-007 Sync groups | S | **P** | | S | | | | | 3 |
| ADD-008 Approval lifecycle | S | **P** | S | | S | | | S | 2 |
| ADD-009 Creative integrity | | **P** | | S | | | | S | 4 |
| ADD-010 Dynamic creative auth. | | **P** | S | | S | | | S | 4 |
| ADD-011 Compliance declarations | | S | **P** | | S | | | S | 4 |
| ADD-012 Advertiser separation | S | | **P** | S | | | | | 3 |
| ADD-013 Deal access & obligation | **P** | | S | S | S | | | | 1 |
| ADD-014 Accreditation, IO, settlement | S | | S | | **P** | | S | | 2 |
| ADD-015 Planning metrics | S | | | | **P** | S | | | 2 |
| ADD-016 Conformance profile | S | | | | | | **P** | S | 4 |

Note the shape: **AdCP Media Buy and Creative carry the descriptive layer; AAMP Agentic
Direct carries everything that involves a contract or a negotiation.** ARTF is almost
entirely secondary — it receives bindings, it defines nothing on its own. That is the
right outcome, and the opposite of where the industry's OOH knowledge sits today.

---

## 4. The insertion-order expansion

**The requirement:** a buyer agent sends a brief; it must understand the offer it gets
back, using the standard additions, without any programmatic transaction having occurred.

This is not a secondary use case. In Ströer's model **every** deal — programmatic
included — is contingent on an IO issued by sales (ADD-014). The contracted path is the
main path, and the programmatic path runs inside it.

### The four-step model the additions have to serve

```
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ 0. DISCOVER  │──>│ 1. BRIEF     │──>│ 2. OFFER     │──>│ 3. ORDER     │
   │ capability   │   │ objectives   │   │ what is      │   │ terms fixed, │
   │ & catalogue  │   │ & constraints│   │ available    │   │ then execute │
   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
    ADD-016            ADD-015            ADD-001..013       ADD-014
    ADD-004            ADD-005            ADD-015            ADD-011
    ADD-014                               ADD-012
```

**Step 0 — Discover.** Before briefing, an agent must learn: can I transact with this
seller at all (ADD-014 prerequisites with `status_for_buyer`), what does it support
(ADD-016 conformance profile), and what is its inventory catalogue (ADD-004 networks and
venue types). Without step 0 an agent will brief sellers it cannot buy from and produce
plans that die at booking.

**Step 1 — Brief.** The brief must be expressible in **planning** language (ADD-015):
share of voice, GRP, OTS, dwell, reach and frequency, with target-group and currency
provenance — plus constraints: minimum disclosure tier (ADD-005), venue types to include
or exclude (ADD-004), creative forms available (ADD-006).

**Step 2 — Offer.** The offer must be **self-describing** against the additions. This is
the crux of the requirement, so it is spelled out below.

**Step 3 — Order.** The order fixes the terms that determine what the offer meant:
pricing basis and floor, disclosure tier, settlement (ADD-014), and the declarations
gating delivery (ADD-011).

### What an offer must let a buyer agent conclude

An agent reading an offer must be able to answer all of these mechanically. Each row is a
question, the addition that answers it, and what goes wrong today without it.

| The agent must know | Addition | Consequence if absent |
| --- | --- | --- |
| What am I billed on, and is the figure modelled? | ADD-001 | Treats modelled fractional contacts as served impressions; mis-values the offer |
| How does the headline audience number decompose? | ADD-002 | Cannot compare two offers quoting the same audience with 10× different play counts |
| When do the numbers settle? | ADD-003 | Closes the campaign against provisional data |
| Which venues and networks am I buying? | ADD-004 | Cannot judge context fit; cannot exclude unsuitable venues |
| How precisely will locations be disclosed? | ADD-005 | Accepts an offer that cannot satisfy the brief's geo targeting |
| Will my video creative be rejected on some screens? | ADD-006 | Discovers mid-flight that a quarter of the buy needs static artwork |
| Do I need two aspect ratios? | ADD-007 | Under-produces creative; sync groups go unfilled |
| How long until my creative is approved? | ADD-008 | Books a start date that is not achievable |
| Can I rotate creative URLs? | ADD-009, ADD-010 | Creative rejected as fraudulent mid-campaign |
| What must my principal have declared? | ADD-011 | Blocked at delivery after the plan is signed off |
| How much of a loop can I actually hold? | ADD-012 | Promises an SOV that is structurally impossible |
| Can I even transact here, and what's the lead time? | ADD-013, ADD-014 | Plan is unexecutable; discovers the IO requirement at booking |
| Does the offer meet my planning targets? | ADD-015 | Cannot evaluate fit at all; falls back to price alone |

### Worked example

A brief and an offer, composed from the R1 additions. Illustrative shapes, not schemas.

**Brief** — planning objectives plus constraints:

```json
{
  "objective": { "market": "DE", "flight": { "start": "2026-10-05", "end": "2026-10-18" } },
  "planning_targets": [
    { "metric": "share_of_voice", "basis": "loop_time", "scope": "network",
      "value": 0.30, "type": "minimum" },
    { "metric": "grp", "value": 120, "type": "minimum", "target_group": "commuters_18_49" }
  ],
  "constraints": {
    "venue_types": { "include": ["transit", "mall"] },
    "min_location_disclosure_tier": "semi_transparent",
    "available_creative_forms": ["video"],
    "creative_ready_date": "2026-10-01"
  }
}
```

**Offer** — and note that a well-formed offer here is partly a *refusal*, with reasons:

```json
{
  "seller": "stroeer",
  "pricing_basis": "audience_impressions",
  "audience_impressions": { "value": 4820000, "kind": "forecast",
    "provenance": { "basis": "modelled", "methodology": "<currency>", "geography": "DE" } },
  "delivery_chain": { "screens": 412,
    "forecast": { "screen_plays": 1240000, "audience_impressions": 4820000 } },
  "seller_networks": [
    { "id": "sv", "name": "Public Video Station", "venue_types": [<transit>], "screens": 294 },
    { "id": "mv", "name": "Public Video Mall",    "venue_types": [<mall>],    "screens": 118 }
  ],
  "location_disclosure": { "tier": "semi_transparent",
    "attributes_provided": ["city", "region", "country", "network", "venue_type"] },
  "creative_constraints": [
    { "scope": { "seller_network": "mv" },
      "sync_groups": [{ "win_semantics": "all_or_nothing",
        "members": [{ "role": "primary", "w": 1080, "h": 1920 },
                    { "role": "companion", "w": 1920, "h": 1080 }] }] }
  ],
  "planning_forecast": [
    { "metric": "share_of_voice", "basis": "loop_time", "scope": "network",
      "value": 0.25, "guaranteed": true,
      "capped_by": { "ref": "ADD-012", "reason": "advertiser_separation" } }
  ],
  "creative_approval": { "required": true, "human_review": true,
    "sla": { "max": "P2D" }, "earliest_start_from_submission": "P2D" },
  "access": { "models": ["fixed_price_deal"], "open_auction": false,
    "prerequisites": [{ "type": "insertion_order", "status_for_buyer": "missing",
                        "lead_time": "P10D" }] },
  "unmet_brief_targets": [
    { "target": "share_of_voice", "requested": 0.30, "offered": 0.25, "cause": "ADD-012" }
  ]
}
```

From this the agent can conclude, without a human and without bidding:

1. The SOV target cannot be met — 25% is the structural cap from advertiser separation.
   It can widen the network set or extend the flight, and it knows which lever to pull.
2. The Mall portion needs a second creative in 16:9. Its brief said video only in 9:16,
   so **creative production is a blocker**, not the media plan.
3. Approval takes two days and the creative is ready 4 October for a 5 October start —
   that is one day short. The flight must move or the creative must land earlier.
4. There is no IO with this seller and it takes ~10 days. **This is a human decision and
   it is on the critical path** — the agent should escalate now, not at booking.

Every one of those four conclusions is impossible today. Three of them would surface as
campaign failures rather than planning outputs. That is the case for the offer/IO
bindings, and it is why they are specified in every addition rather than in a few.

### What this implies for the protocols

| Requirement | Where |
| --- | --- |
| A brief object that carries planning objectives, not just budget and targeting | AdCP Media Buy → brief/RFP; AAMP Agentic Direct |
| An offer object that answers in the same terms, with guarantees and caps | AdCP Media Buy → offer; AAMP Agentic Direct |
| **An offer must be able to express what it cannot do, and why** | Both — `unmet_brief_targets` has no equivalent in either protocol today |
| Buyer-specific prerequisite status, resolved before briefing | AdCP Accounts; AAMP Registry |
| An order object fixing the terms that give an offer meaning | AAMP Agentic Direct |

The third row is the one most likely to be overlooked and matters most. An offer that
silently under-delivers against a brief is worse than a refusal, because an agent will
accept it. **A structured "cannot meet, because" is a first-class protocol requirement.**

---

## 5. First submissions

Four OEPs, bundling additions into coherent asks. Written but not yet filed — see
[`proposals/`](proposals/).

| OEP | Bundles | Target | Ask |
| --- | --- | --- | --- |
| **OEP-0001** OOH product & offer shape | ADD-001, ADD-002, ADD-004, ADD-006 | AdCP Media Buy + Creative | The minimum to describe DOOH inventory in a product/offer |
| **OEP-0002** Briefs and offers in planning terms | ADD-015, ADD-005, ADD-012 | AdCP Media Buy + AAMP Agentic Direct | Planning objectives in briefs; forecasts, caps and `unmet_brief_targets` in offers |
| **OEP-0003** Creative approval as a gated lifecycle | ADD-008, ADD-009, ADD-010 | AdCP Creative | Approval state machine, SLA, rejection reason codes, integrity policy, authorisation object |
| **OEP-0004** Orders and commercial prerequisites | ADD-014, ADD-013, ADD-011 | AAMP Agentic Direct | The order as a protocol object; prerequisites with buyer-specific status |

Sequencing rationale: OEP-0001 is the foundation and the least contentious. OEP-0003 is
self-contained and generalises cleanly to any human-reviewed channel, so it is a good
early credibility win. OEP-0002 and OEP-0004 are the valuable, structural ones and should
go in once the first two have established the working relationship.

## 6. Before anything is submitted

Blocking:

- [ ] **Verify every placement** against current AdCP and AAMP revisions. All 16
      additions are `target_revision_checked: 2026-08-27` against public summaries, not
      against the specs themselves.
- [ ] **Retrieve the two blocked specifications** ([`analysis/open-gaps.md`](analysis/open-gaps.md) §1).
      ADD-008 cannot be finished without the rejection reason-code taxonomy.
- [ ] **Get answers to the eight Ströer questions** (§3 of the same file). At least three
      change the shape of an addition rather than its detail.
- [ ] **Settle the AdCP extension strategy** (§1 above) with the maintainers.
- [ ] **Resolve the 24 h / 48 h approval SLA contradiction.**

Strongly recommended:

- [ ] **A second media owner's integration standards**, ideally in another market, to
      separate universal additions from Ströer-specific ones. Every addition's market
      applicability is currently unfilled.
- [ ] **Classic/static OOH**, absent from R1 entirely and the largest gap in coverage.
- [ ] **A reference seller agent** implementing wave 1 against the offer bindings. It is
      the most convincing argument to a working group that these shapes are
      implementable, and it would immediately test the offer/IO sketches in §4.

## 7. Risks

| Risk | Mitigation |
| --- | --- |
| Evidence is one media owner in one market — additions may encode Ströer practice as if it were OOH practice | Explicit market-applicability sections; second-source before promoting anything to `stable` |
| Upstream moves faster than we verify | Date-stamped pins; treat any pin older than ~2 upstream releases as unverified (`VERSIONING.md` §3) |
| 16 additions is more than any working group will absorb at once | Four bundled OEPs, sequenced; wave 1 first |
| Arguing OOH specialness invites a second-class channel profile | Frame the six general additions as core improvements, not OOH pleading (§1) |
| The offer/IO bindings are our own invention and unreviewed | Build the reference seller agent; treat the JSON in §4 as sketches until a schema exists |
| ADD-014 is really general agentic commerce, and may be out of scope for an OOH group | Submit it to AAMP Agentic Direct as a general gap that OOH exposes, not as an OOH addition |
