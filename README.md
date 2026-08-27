# Standard extensions for Agentic Advertising in OOH

An open working repository for **OOH- and DOOH-specific standards and standard
extensions** for the two emerging agentic advertising protocols:

- **[AdCP](https://github.com/adcontextprotocol/adcp)** — Ad Context Protocol
  (Ad Context Protocol project / AgenticAdvertising.org)
- **[AAMP](https://github.com/IABTechLab/AAMP)** — Agentic Advertising Management
  Protocols (IAB Tech Lab)

Both protocols were designed from a digital-first, impression-first, addressable
world view. Out of Home does not fit that world view cleanly. This repository
collects what is genuinely different about OOH, turns those differences into
concrete protocol requirements, and proposes **where in the existing protocols
each requirement belongs** — as a field, an enum value, a new object, or a new
task.

## Why this repository exists

An AI buying agent that can plan and execute across CTV, audio, display and
retail media will fail on OOH for reasons that are structural, not cosmetic:

| Digital assumption | OOH reality |
| --- | --- |
| The unit of trade is an impression | The unit of trade is a **play in a loop**, a **share of voice/time**, or a **panel for a calendar period** |
| One ad render = one person | One play = **n people**, modelled by a market audience currency (impression multiplier) |
| Inventory is an auctionable stream | Inventory is a **finite set of physical screens and frames** with a fixed loop capacity per daypart |
| Availability is a forecast | Availability is a **booking calendar** with reservations, blackouts and lead times |
| Targeting is user- or content-based | Targeting is **geospatial, venue-type and temporal** |
| Delivery is a served-impression log | Delivery is a **proof-of-play log** per screen, plus modelled audience on top |
| Identity is a device or user ID | There is **no user identity at all** — OOH is aggregate and privacy-by-design |
| Creative is a tag or a video file | Creative is resolution-, orientation- and duration-bound, usually **silent**, often **multi-frame**, and needs **landlord and municipal clearance** |
| Static inventory does not exist | **Classic (printed) OOH** still carries a large share of spend and has print, logistics and installation lead times |

Getting these into the protocols now — while both are young and actively taking
contributions — is cheaper than retrofitting them later.

## What this repository will produce

1. **OOH specifica** — a structured catalogue of what OOH needs from an agentic
   protocol, written so a protocol maintainer with no OOH background can read it.
   → [`ooh-specifics/`](ooh-specifics/)
2. **Placement proposals** — for each requirement, the concrete place in AdCP and
   AAMP where it should live, and whether it is an extension, a new enum value or
   a new object/task.
   → [`mapping/`](mapping/)
3. **Formal extension proposals (OEPs)** — self-contained, reviewable documents we
   can hand to the AdCP and AAMP working groups, with schema drafts.
   → [`proposals/`](proposals/) and [`schemas/`](schemas/)

## Repository layout

```
.
├── PLAN.md                The plan: which additions go where, in what order, and how
│                          insertion-order buying is served alongside programmatic
├── VERSIONING.md          How additions, releases and protocol pins are versioned
├── analysis/              Analysis of real media-owner integration standards
├── additions/             THE VERSIONED CORE — one file per extension unit
│   └── releases/          Frozen manifests pinning addition versions
├── docs/                  Background reading: glossary, OOH primer, measurement currencies
├── ooh-specifics/         WHAT is specific to OOH — the requirements catalogue
├── mapping/               WHERE it belongs in the existing protocols
│   ├── adcp/              Per AdCP domain: Media Buy, Creative, Signals, ...
│   └── aamp/              Per AAMP component: ARTF, Agentic Audiences, Agentic Direct, ...
├── proposals/             OOH Extension Proposals (OEPs) — the deliverables to the WGs
├── schemas/               JSON Schema drafts backing the proposals
└── scripts/               validate.py — registry, version and link consistency checks
```

Every directory has its own `README.md` explaining its scope and current status.

## Start here

| If you want to... | Read |
| --- | --- |
| Understand the plan and what we ask AdCP/AAMP for | [`PLAN.md`](PLAN.md) |
| See the versioned extension units | [`additions/REGISTRY.md`](additions/REGISTRY.md) |
| See where the evidence comes from | [`analysis/`](analysis/) |
| Understand how versions work | [`VERSIONING.md`](VERSIONING.md) |

## Additions — the versioned core

An **addition** is one normative extension unit: a single OOH concept, defined
independently of any transport, bound to both a **programmatic** and an
**insertion-order** representation, with a proposed placement in AdCP and AAMP.

Release **R1.0** contains 16 additions, derived from analysis of Ströer's production
DOOH integration standards. Index: [`additions/REGISTRY.md`](additions/REGISTRY.md).
Manifest: [`additions/releases/R1.0.md`](additions/releases/R1.0.md).

Every addition carries three layers, and the middle one is the reason the whole
exercise exists:

```
   SEMANTIC DEFINITION  ── transport-neutral. What the concept IS.
        │            │
        ▼            ▼
  PROGRAMMATIC     OFFER / IO BINDING
  BINDING          What a buyer agent reads when it sends a brief —
  (RTB today)      before any bid request exists.
```

Media owners have been forced to encode every OOH-specific concept **inside the
programmatic transport**: as an OpenRTB extension, a VAST macro, a synthetic domain
name, or a token inside a file name. A buyer agent that has not yet bid can discover
none of it — and none of it is reusable for insertion-order buying, which is where most
OOH money still sits. Each addition therefore lifts the concept out of the transport,
then binds it back down to both paths.

Everything is versioned per addition, with frozen release manifests, because these
standards will expand — see [`VERSIONING.md`](VERSIONING.md).

## The OOH specifica at a glance

The requirements catalogue is organised into ten areas. Each links to its stub:

| # | Area | Core question |
| --- | --- | --- |
| 01 | [Inventory & supply model](ooh-specifics/01-inventory-and-supply-model.md) | How do you describe a network of screens, frames and loops? |
| 02 | [Trading & pricing models](ooh-specifics/02-trading-and-pricing-models.md) | How do you price a play, a share of voice, or a panel-week? |
| 03 | [Audience & measurement](ooh-specifics/03-audience-and-measurement.md) | Whose impression number is it, and how is it derived? |
| 04 | [Targeting dimensions](ooh-specifics/04-targeting-dimensions.md) | Geospatial, venue and temporal targeting as first-class citizens |
| 05 | [Creative & formats](ooh-specifics/05-creative-and-formats.md) | Format specs, silence, multi-frame, dynamic triggers, print |
| 06 | [Delivery & proof of play](ooh-specifics/06-delivery-and-proof-of-play.md) | What does "delivered" mean without an ad server impression? |
| 07 | [Availability & booking lifecycle](ooh-specifics/07-availability-and-booking-lifecycle.md) | Reservations, calendars, lead times, cancellation terms |
| 08 | [Compliance & content restrictions](ooh-specifics/08-compliance-and-content-restrictions.md) | Landlord rules, municipal law, category separation |
| 09 | [Privacy & identity](ooh-specifics/09-privacy-and-identity.md) | A channel with no user identity — and what that simplifies |
| 10 | [Sustainability](ooh-specifics/10-sustainability.md) | Energy and emissions per play as a buying criterion |

## Where it plugs in — first read

A first, deliberately coarse view of the target surfaces. Detail and verification
against the current spec revisions is the next work package.

**AdCP**

| AdCP domain | Candidate OOH work |
| --- | --- |
| Media Buy | OOH product shape, geospatial/venue targeting, play- and SOV-based pricing, reservation semantics, proof-of-play delivery reporting |
| Creative | DOOH format definitions (resolution, orientation, duration, no audio), multi-frame/synchronised creative, print specs, clearance workflow |
| Signals | OOH audience currencies, venue context, moment triggers (weather, transit, events) |
| Accounts & Governance | Landlord and municipal content standards, competitive separation within a loop |
| Trusted Match | Largely N/A — OOH is non-addressable; screen/context matching at play time instead |

**AAMP**

| AAMP component | Candidate OOH work |
| --- | --- |
| ARTF | pDOOH in real-time bidding: multiplied impressions, screen context, loop constraints |
| Agentic Audiences | Aggregate, ID-free OOH audience schema and currency provenance |
| Agentic Direct | Classic OOH direct flow: RFP → proposal → reservation → installation proof |
| Buyer/Seller/Registry Agents | Media-owner and screen-network discovery and capability advertisement |
| Trust & Transparency | Playout-log integrity, verified vs modelled delivery, discrepancy handling |

For the coarse view above, see [`mapping/`](mapping/). For the actual placement
decisions — which protocol owns what, in what order, and with which additions bundled
into which submission — see [`PLAN.md`](PLAN.md).

## Status

**Early.** Release R1.0 of the additions is published, and all 16 additions are at
`0.1.0` / `draft` — the analysis is complete, but **nothing has been verified against a
current AdCP or AAMP revision and nothing should be implemented yet.** The
`ooh-specifics/` and `mapping/` documents remain outlines.

Nothing here has been submitted to, or endorsed by, the AdCP or AAMP projects.

Protocol facts in this repository were last checked against public sources in
**August 2026** (AdCP published Oct 2025; AAMP named Feb 2026, published Mar 2026,
latest public release AAMP 2.3, Jul 2026). Both move fast — re-verify before
citing any task, field or version.

## Roadmap

- [x] Analyse a real media owner's DSP integration standards → [`analysis/`](analysis/)
- [x] Turn the findings into versioned additions → [`additions/`](additions/) release R1.0
- [x] Set up versioning for additions, releases and protocol pins → [`VERSIONING.md`](VERSIONING.md)
- [x] Produce the placement plan, covering insertion-order as well as programmatic → [`PLAN.md`](PLAN.md)
- [ ] **Verify AdCP and AAMP surface names, tasks and schemas against the current revisions** — every R1 placement is unverified
- [ ] Retrieve the two blocked source specifications ([`analysis/open-gaps.md`](analysis/open-gaps.md) §1)
- [ ] Settle the AdCP extension strategy with the maintainers ([`PLAN.md`](PLAN.md) §1)
- [ ] Fill in the ten `ooh-specifics/` documents with concrete requirements
- [ ] Complete the `mapping/` documents, one target surface at a time
- [ ] Write the four planned OEPs ([`PLAN.md`](PLAN.md) §5)
- [ ] Draft JSON Schemas in `schemas/` for the accepted OEPs
- [ ] Add a second media owner's standards, to separate universal additions from Ströer-specific ones
- [ ] Cover classic/static OOH, absent from R1 entirely

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Market-specific input is explicitly
wanted — OOH trading conventions and audience currencies differ substantially
between markets, and a standard that only fits one of them is not a standard.

## Licence

Not yet decided — see the open question in [CONTRIBUTING.md](CONTRIBUTING.md).
Until a `LICENSE` file exists, treat the contents as "all rights reserved" and
ask before reusing.
