# AAMP proposals

Proposals targeting **AAMP** (`IABTechLab/*`), verified against **OpenDirect v2.1**
(Agentic Direct) and **OpenRTB 2.6** (ARTF).

Naming: `OEP-AAMP-NNNN-slug.md`. Numbers are per protocol and permanent.

Upstream contribution route: the AAMP hub states that contributions go to the relevant
**child repository**, while **architectural proposals may be initiated in the hub**.
Both items below span repositories, so both belong in the hub.

## Index

| OEP | Title | Bundles | Status |
| --- | --- | --- | --- |
| — | *none written yet* | | |

## Planned

All three AAMP-owned additions verified as already existing upstream, so there is
nothing to propose for them. What AAMP needs instead are two **consistency findings**
that emerged from verification and stand on their own:

| # | Title | Source | Why |
| --- | --- | --- | --- |
| 0001 | Agentic Direct has no DOOH placement object | [`../../verification/aamp.md`](../../verification/aamp.md) §6 | ARTF is on OpenRTB 2.6 and has a `Dooh` object; Agentic Direct's object set has none, forcing a screen to be modelled as a site or ad unit. The two halves of AAMP disagree about whether DOOH exists. |
| 0002 | The referenced DP-AA DOOH Extension is not implemented | [`../../verification/aamp.md`](../../verification/aamp.md) §5 | `opendirect.json` declares `"DP-AA DOOH Extension"` in `referencedSpecifications`, but no schema, field or enum implements any of it. |

**Blocked:** OEP-AAMP-0002 must not be written until the DP-AA DOOH Extension has been
read. Proposing against a specification we have not seen risks duplicating it.

## Guidance, not proposals

| Addition | Output |
| --- | --- |
| ADD-001 | Migration note: `imp.ext.totalaud` → OpenRTB 2.6 `Imp.Qty` (`multiplier`, `sourcetype`, `vendor`) |
| ADD-004 | Migration note: synthetic `site.domain` encoding → `Dooh` object with `venuetype` / `venuetypetax` |
| ADD-014 | Conformance mapping onto `OpenDirect.Order` / `Line` / `ChangeRequest`; the surviving requirement moved to ADD-013 (AdCP) |

These three are the most immediately useful output of the whole verification pass for a
DOOH seller on OpenRTB 2.5 — they describe how to stop needing proprietary extensions.
