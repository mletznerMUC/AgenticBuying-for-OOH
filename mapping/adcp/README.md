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

## Cross-cutting question

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
