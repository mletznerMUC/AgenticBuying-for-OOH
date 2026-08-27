# 05 — Creative and formats

> Status: **stub** — outline only.

**Question this document answers:** what does an OOH creative specification have to
carry, and what must happen to a creative before it can run?

## What this document will cover

- [ ] Digital format specs: pixel dimensions, aspect ratio, orientation, colour
      profile, file type, file size, bitrate, frame rate, duration
- [ ] Duration as a hard constraint set by the slot, not a preference
- [ ] Silence: most DOOH has no audio, and creative must work without it
- [ ] No click, no landing page — call-to-action is offline or via QR/short URL
- [ ] Safe areas, minimum legible type size, viewing distance
- [ ] Multi-frame and synchronised creative across adjacent screens
- [ ] Roadblocks and takeovers as creative constructs, not just buys
- [ ] Dynamic creative: templates plus data feeds and trigger conditions
- [ ] Classic/static: print specs, bleed, material, production and delivery deadlines
- [ ] Copy clearance and approval: media owner, landlord, municipal authority, and
      the fact that approval can be revoked mid-campaign
- [ ] Creative versioning and rotation within a booking

## Why the digital-first assumption breaks

A creative model built around tags, VAST and clickthroughs has nowhere to put "1080
× 1920 portrait, exactly 10 seconds, silent, no click, cleared by the landlord for
this specific site". Nor can it express one creative spanning three physical frames.

## Requirements

`R-CRE-1` … *to be written.*

## Open questions

- Do we define an OOH format taxonomy, or describe formats purely by their
  properties and let agents match on properties?
- How is a clearance workflow modelled in a protocol designed for automated
  execution — as a state machine on the creative, or as a separate approval task?
- How are multi-frame creatives bound to specific physical frames?

## Related

- [`../mapping/adcp/creative.md`](../mapping/adcp/creative.md)
- [`../mapping/adcp/accounts-and-governance.md`](../mapping/adcp/accounts-and-governance.md)
