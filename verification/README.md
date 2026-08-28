# Verification

What the R1.0 additions assumed about AdCP and AAMP, checked against the actual
specifications rather than public summaries.

| Document | Contents |
| --- | --- |
| [verdicts.md](verdicts.md) | **The result** — per-addition verdict and what each ask becomes |
| [adcp-3.2.md](adcp-3.2.md) | AdCP findings, with schema paths as evidence |
| [aamp.md](aamp.md) | AAMP findings — Agentic Direct / OpenDirect, ARTF / OpenRTB 2.6 |

## Method

Both specifications were cloned and read directly. Nothing here comes from a summary,
a marketing page or a search result.

| Source | Revision | Retrieved |
| --- | --- | --- |
| `adcontextprotocol/adcp` | **3.2.0-beta.8** (`package.json`) | 2026-08-27 |
| `IABTechLab/AAMP` (hub) | HEAD | 2026-08-27 |
| `IABTechLab/agentic-direct` | OpenDirect **v2.1** MCP server | 2026-08-27 |
| `IABTechLab/agentic-rtb-framework` (ARTF) | v1.0, OpenRTB **2.6** protobuf | 2026-08-27 |

Evidence is cited as a repository-relative path into the upstream source, so any claim
here can be re-checked directly.

## The headline

**R1.0 substantially overestimated the gap.** Both protocols already carry more OOH
support than the additions assumed — in several cases exactly the thing an addition
proposed to invent.

The single most important finding: **OpenRTB 2.6 already standardises the audience
multiplier.** `Imp.Qty` carries a fractional `multiplier`, a `sourcetype` drawn from
`DOOHMultiplierMeasurementSourceType`, and a measurement `vendor` domain. Ströer's
`imp.ext.totalaud` is not a gap in the standard — it is a **pre-2.6 workaround for a
gap that has since been closed**. ARTF is built on 2.6, so the fix for a large part of
Ströer's proprietary transport layer is *migrate*, not *extend*.

Counting the sixteen additions:

| Verdict | Count | Meaning |
| --- | :-: | --- |
| **Exists** | 4 | Upstream already covers it; our work is conformance and migration guidance |
| **Partial** | 8 | Substantial prior art; the ask shrinks to a specific field or enum value |
| **Gap** | 4 | Confirmed absent from both protocols |

Four confirmed gaps — ADD-005, ADD-009, ADD-012, ADD-013 — are now the most valuable
things in the repository, because they are the ones nobody has solved. See
[verdicts.md](verdicts.md).

## What this does not cover

- AdCP's `docs/` prose was only spot-checked; the schemas were treated as normative.
- AAMP's Buyer Agent, Seller Agent, Registry Agent and Agentic Audiences repositories
  were **not** examined in this pass. ADD-016's placement and the Agentic Audiences
  half of ADD-001 therefore remain unverified.
- The two Ströer specifications are still unretrievable (see
  [`../analysis/open-gaps.md`](../analysis/open-gaps.md) §1), though the AdCP finding
  on rejection reason codes makes the most urgent of those questions much less urgent.
