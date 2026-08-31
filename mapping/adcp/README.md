# AdCP mapping

Per-domain mapping of OOH requirements onto the **Ad Context Protocol**.

Upstream: [`adcontextprotocol/adcp`](https://github.com/adcontextprotocol/adcp) —
normative text under `docs/`, schemas under `static/schemas/source/`.

| Document | AdCP domain | OOH weight |
| --- | --- | --- |
| [media-buy.md](media-buy.md) | Media Buy | **High** — inventory, targeting, pricing, booking, delivery |
| [creative.md](creative.md) | Creative | **High** — formats, silence, multi-frame, clearance, print |
| [signals.md](signals.md) | Signals | Medium — audience currencies, venue context, triggers |
| [accounts-and-governance.md](accounts-and-governance.md) | Accounts, Governance | Medium — content restrictions, competitive separation |
| [trusted-match.md](trusted-match.md) | Trusted Match | Low — OOH is non-addressable |

## Cross-cutting question — **resolved**

> **Answered by verification (2026-08-27).** AdCP has a first-class extension
> mechanism: `extensions/extension-meta.json` defines namespaced extensions at
> `/schemas/extensions/{namespace}.json`, carrying data at **`ext.{namespace}`**,
> declaring **`valid_from`** / `valid_until` AdCP versions and a `docs_url`, and
> **auto-discovered** into versioned schema builds. `core/product.json` has an `ext`
> field.
>
> **Decision: a registered `ooh` namespace for genuinely OOH-only concepts, core
> changes for the six additions that are not really OOH-specific** (see
> [`../../PLAN.md`](../../PLAN.md) §1). The mechanism even versions itself in a way that
> lines up with [`../../VERSIONING.md`](../../VERSIONING.md) §3.
>
> Verification also showed the premise was too pessimistic: AdCP already has `dooh` and
> `ooh` channels, `property-type: dooh`, `dooh_metrics`, an experimental `ooh_metrics`,
> and `sov_percentage`. OOH is not absent from the core — it is partially there already.
>
> The original framing is kept below for the record.

Does OOH belong in AdCP as:

- **(a) channel-specific extensions** to the existing objects — an `ooh` block on
  products, targeting, creative and delivery; or
- **(b) a distinct OOH profile** of the protocol, with its own objects that reuse the
  shared envelope; or
- **(c) generalisation of the core** — making the core less impression-first so OOH
  falls out naturally, which also benefits audio, cinema and print?

(c) is the most valuable if the maintainers will entertain it, (a) is the most likely
to be accepted quickly, (b) risks a second-class channel. This decision shapes every
document in this directory and should be settled early, with the maintainers.
