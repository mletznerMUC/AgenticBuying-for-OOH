# Analysis of existing implementation guidelines

Analysis of real, in-production proprietary OOH integration standards, used as the
input to the additions in [`../additions/`](../additions/).

The premise: a media owner that already runs programmatic DOOH at scale has been
forced to invent, in private, every extension the standard was missing. Those
private extensions are the most reliable available evidence of what an agentic
protocol has to carry. Rather than deriving OOH requirements from first principles,
we read them off a working implementation.

| Document | Scope |
| --- | --- |
| [stroeer-ppv-baseline.md](stroeer-ppv-baseline.md) | Complete inventory of the proprietary additions in the Ströer Public Video DSP integration, with source references |
| [open-gaps.md](open-gaps.md) | What could not be verified, and internal inconsistencies found in the source documents |

## Sources analysed

| Source | Version / date | Notes |
| --- | --- | --- |
| Ströer PPV Implementation Guide | v6, 11 pp. | Core document: OpenRTB adjustments, macros, networks, code examples, best practice, IO appendix |
| Ströer PPV Implementation Guide — Static Creatives | 6 pp., states "August 2022" for affected networks | Two implementation options for static image creatives |
| Public Video Creative Approval | 1 p. (also Appendix B of the v6 guide) | Creative review, caching model, DCO-ID process |
| DSP Integration Ströer SSP | 2 pp. | Onboarding and certification test plan |
| `https://creative.api.adscale.de/v1/docs` | — | **Not retrieved** — blocked by this environment's network egress policy |
| `https://specs.myadscale.de/dsp-adapter/external/1.0.html` | — | **Not retrieved** — blocked by this environment's network egress policy |

See [open-gaps.md](open-gaps.md) for what specifically needs to be filled in from
the two unreachable sources.

## The central finding

Every one of Ströer's OOH-specific concepts is encoded **inside the programmatic
transport**: as an OpenRTB extension object, a VAST substitution macro, a synthetic
domain string, a token inside a file name, or a mime-type list that implies a legal
restriction. None of it exists at the level of a *product* or an *offer*.

That is a rational response to OpenRTB being the only channel available. It is also
exactly what breaks agentic buying:

- A buyer agent that has not yet bid cannot discover any of it. The venue type, the
  audience multiplier, the static-only restriction, the approval SLA and the
  sync-group obligation are only observable by inspecting live bid requests.
- Concepts leak into fields that mean something else. A screen's location becomes a
  fake domain name (`duesseldorfhbf-duesseldorf-sv.de`). A physical screen becomes a
  `site` with a `page`. A DCO authorisation becomes a substring of a file name. A
  channel with no users carries a hashed `user.id`.
- None of it is reusable for insertion-order or direct buying, which is where the
  majority of OOH money still sits — even though the underlying facts (audience
  basis, venue type, format restrictions, approval lead time) are identical.

The work in [`../additions/`](../additions/) therefore does two things at once:
**lift each concept out of the transport into a transport-neutral definition**, then
**bind it back down** to both a programmatic and an insertion-order representation.
