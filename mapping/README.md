# Mapping to the existing protocols

**Where each OOH requirement belongs in AdCP and AAMP.**

This directory answers the second half of the brief: not *what* OOH needs, but
*where in the existing protocols* to put it — and whether that is a new field, a new
enum value, a new object, a new task, or a change to existing semantics.

- [`adcp/`](adcp/) — Ad Context Protocol, by protocol domain
- [`aamp/`](aamp/) — Agentic Advertising Management Protocols, by component

## Protocol landscape (checked August 2026 — re-verify before citing)

**AdCP — Ad Context Protocol.** Open protocol for AI agents to discover inventory,
buy media, build creatives and activate audiences, built on MCP. Published October
2025; founding participants include Yahoo, Optable, PubMatic, Scope3, Swivel and
Triton Digital. Specification and reference implementation:
[`adcontextprotocol/adcp`](https://github.com/adcontextprotocol/adcp). Normative
sources are the documents under `docs/` and the schemas under
`static/schemas/source/`.

Domains observed at the revision checked:

| Domain | Purpose |
| --- | --- |
| Media Buy | Inventory discovery and campaign management |
| Creative | Ad asset management across channels |
| Signals | Audience activation and targeting |
| Accounts | Commercial identity and billing |
| Governance | Brand suitability and content standards |
| Trusted Match | Serve-time package activation |

**AAMP — Agentic Advertising Management Protocols.** IAB Tech Lab's umbrella
framework for agentic advertising, named February 2026 and published March 2026;
latest public release at the time of checking was 2.3 (July 2026). Organised across
three pillars — Agentic Foundations, Agentic Protocols, and Trust and Transparency —
and distributed over several repositories under
[`IABTechLab/AAMP`](https://github.com/IABTechLab/AAMP), each versioned
independently: Agentic Direct, Buyer Agent, Seller Agent, Registry Agent, ARTF
(Agentic Real-Time Framework) and Agentic Audiences.

> Task names, field names, module names and versions cited anywhere in this
> repository are from public sources as of August 2026 and **must be re-verified**
> against the current revision before any proposal is submitted.

## How to read a mapping document

Each document covers one target surface and states, per OOH requirement:

| Column | Meaning |
| --- | --- |
| Requirement | The `R-*` ID from [`../ooh-specifics/`](../ooh-specifics/) |
| Target | The specific object, field, enum or task in that surface |
| Change type | `extend-enum`, `add-field`, `new-object`, `new-task`, `clarify-semantics`, `out-of-scope` |
| Rationale | Why here and not elsewhere |
| Confidence | How sure we are that this surface exists and looks as described |

## Working order

1. Verify each surface against the current spec revision and correct this directory.
2. Fill in the mapping tables, starting with AdCP Media Buy — it carries the most
   OOH-specific weight.
3. Promote the highest-value mappings into OEPs in [`../proposals/`](../proposals/).
