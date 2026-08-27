# 01 — Inventory and supply model

> Status: **stub** — outline only.

**Question this document answers:** how do you describe OOH supply to an agent, when
supply is a finite set of physical objects rather than an addressable stream?

## What this document will cover

- [ ] The supply hierarchy: media owner → network → structure → face → panel/screen
- [ ] Screen properties: resolution, orientation, physical size, indoor/outdoor,
      illumination hours, operating hours, audio capability (usually none)
- [ ] The loop: loop length, slot length, slots per loop, plays per hour, and how
      loop composition constrains what can be sold
- [ ] Static panels: no loop, no schedule — one creative for one booking period
- [ ] Venue classification and why a shared taxonomy (e.g. the OpenOOH venue
      taxonomy) is a prerequisite for cross-seller comparison
- [ ] Geography as an intrinsic property of inventory, not a targeting overlay
- [ ] Identity and stability of inventory: panel/screen IDs, network IDs, and what
      happens when a screen is replaced, moved or re-classified
- [ ] Granularity of disclosure: screen-level, network-level or aggregate, and what
      a seller is willing to expose to a buying agent

## Why the digital-first assumption breaks

An impression-stream model has no place to express "this is 42 specific screens, at
these coordinates, in these venues, each with a 60-second loop of six 10-second
slots, lit from 06:00 to 24:00". Without that, an agent cannot reason about reach,
capacity, competitive separation or physical context.

## Requirements

`R-INV-1` … *to be written.*

## Open questions

- What is the minimum viable inventory description — the smallest set of fields that
  still lets an agent plan competently?
- Do we standardise a venue taxonomy or reference an existing one normatively?
- How are panel/screen identifiers made globally unambiguous across sellers?

## Related

- [`../mapping/adcp/media-buy.md`](../mapping/adcp/media-buy.md)
- [`../mapping/aamp/agent-sdks-and-registry.md`](../mapping/aamp/agent-sdks-and-registry.md)
