# EDITH Intake — Multimodal Sensing Research

Curated research edition of **EDITH Intake**, an EDITH Dev Studio project exploring passive nutrition capture through event-triggered wearable sensing and multimodal inference.

> Current status: architecture, software/AI research and prototype planning. The central sensing and accuracy hypotheses are **not presented as already validated product results**.

## Research question

Can a small wearable reduce the manual burden of nutrition tracking by combining complementary signals rather than relying on a single photograph?

The current hypothesis combines:

- low-power IMU event detection
- event-triggered RGB capture
- ToF/depth measurements
- temporal tracking
- product/barcode metadata
- confidence-aware decision logic
- paired-phone inference

## Why multimodal sensing

Each signal has different strengths:

| Signal | Useful for | Limitation |
|---|---|---|
| IMU | low-power event candidate detection | cannot identify food |
| RGB | identity, segmentation, containers | weak absolute scale |
| ToF | metric distance / geometry constraints | weak identity |
| temporal tracking | served → remaining change | occlusion / scene changes |
| barcode/OCR | packaged product identity | not general meals |

The research goal is to determine whether fusion provides enough measured benefit to justify its power, size and complexity.

## Architecture

```text
Wearable
  ├── IMU
  ├── RGB
  ├── ToF/depth
  └── firmware / event gating
           │
           ▼
      Paired phone
           │
  ┌────────┼─────────┐
  ▼        ▼         ▼
event   perception  geometry
  └────────┼─────────┘
           ▼
      sensor fusion
           │
           ▼
 confidence-aware result
           │
           ▼
        EDITH Fit
```

## Engineering principles

- event-triggered sensing instead of continuous video by default
- preserve uncertainty
- no fake precision
- measure where possible, infer where necessary
- evaluate added sensors against simpler baselines
- keep hardware providers modular
- prefer local/on-phone processing
- separate ground-truth equipment from product inputs

## Current stage

Defined:

- product/system architecture
- sensing roles
- software/hardware boundaries
- fusion strategy
- candidate models/datasets
- testing methodology
- staged prototype plan

Still ahead:

- P0 implementation
- controlled dataset collection
- measured event-detection performance
- measured portion/consumption performance
- power/battery validation
- wearable ergonomics validation

## Documentation

- [System architecture](docs/ARCHITECTURE.md)
- [Sensor-fusion strategy](docs/SENSOR_FUSION.md)
- [Current stage and evidence boundary](docs/CURRENT_STAGE.md)
- [Public research scope](docs/PUBLIC_SCOPE.md)

## Related

- Engineering portfolio: https://github.com/Aceishere66/engineering-portfolio
- EDITH Dev Studio engineering page: https://edithdevstudio.com/engineering
