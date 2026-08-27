# AAMP mapping

Per-component mapping of OOH requirements onto the **Agentic Advertising Management
Protocols**.

Upstream: [`IABTechLab/AAMP`](https://github.com/IABTechLab/AAMP) — a hub pointing at
independently versioned component repositories, organised across three pillars
(Agentic Foundations, Agentic Protocols, Trust and Transparency).

| Document | AAMP component | OOH weight |
| --- | --- | --- |
| [artf.md](artf.md) | Agentic Real-Time Framework | **High** — programmatic DOOH |
| [agentic-direct.md](agentic-direct.md) | Agentic Direct | **High** — classic OOH and reserved buys |
| [agentic-audiences.md](agentic-audiences.md) | Agentic Audiences | Medium — ID-free audience schema |
| [agent-sdks-and-registry.md](agent-sdks-and-registry.md) | Buyer / Seller / Registry Agent | Medium — capability advertisement and discovery |
| [trust-and-transparency.md](trust-and-transparency.md) | Trust and Transparency pillar | Medium — playout-log integrity |

## Cross-cutting question

AAMP is distributed across repositories with independent versioning, so an OOH
extension may need to land in several places at once and be coordinated across them.
Before proposing anything, establish:

- which repository owns the object we want to change;
- whether OOH is better served by changes in the components or by an OOH profile
  document that constrains several of them;
- how AAMP and AdCP relate in practice for a seller supporting both, so we do not
  standardise two incompatible OOH models.
