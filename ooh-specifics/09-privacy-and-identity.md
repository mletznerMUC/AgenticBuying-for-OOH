# 09 — Privacy and identity

> Status: **stub** — outline only.

**Question this document answers:** what does an agentic protocol look like in a
channel with no user identity at all?

## What this document will cover

- [ ] OOH as a one-to-many broadcast medium: no user, no device, no cookie, no
      consent surface at the point of exposure
- [ ] Audience as an aggregate model, never an individual record
- [ ] Why most addressability, identity-resolution and consent machinery is
      inapplicable — and should be explicitly marked as such rather than left
      ambiguous
- [ ] Where personal data does enter the picture and needs care: mobility datasets
      used for measurement, mobile-ID exposure segments used for retargeting or
      attribution, camera-based audience sensing
- [ ] Sensor and camera use on screens: what is measured, what is retained, and what
      must be disclosed
- [ ] Regulatory frame in Europe (GDPR) and its implications for OOH measurement
      inputs, including public-space data collection
- [ ] Bystander privacy: people exposed to a screen have not opted in to anything

## Why the digital-first assumption breaks

Two ways. First, protocol fields that assume a user identifier or a consent string
have no meaning here, and leaving them optional invites incorrect population.
Second, the genuinely sensitive parts of OOH privacy — measurement inputs and
sensor data — sit in places a digital-first protocol does not look.

## Requirements

`R-PRIV-1` … *to be written.*

## Open questions

- Should OOH products declare "non-addressable" explicitly as a capability, so
  agents stop attempting identity-based operations against them?
- How should sensor-based audience measurement be disclosed to a buying agent?
- What disclosure do mobility-data-derived audience figures require?

## Related

- [`../mapping/aamp/agentic-audiences.md`](../mapping/aamp/agentic-audiences.md)
- [`../mapping/adcp/trusted-match.md`](../mapping/adcp/trusted-match.md)
