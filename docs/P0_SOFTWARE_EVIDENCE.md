# P0 Software Evidence

## Source

```text
Private repository: Aceishere66/EDITH-Intake
Source commit: ed4a563621b8d56f8604bcf5dc76197cae707e03
```

This page lists selected implemented evidence without turning software/reference results into unmeasured wearable claims.

## Perception baseline

The private P0 baseline records:

- Meta DINOv2 ViT-S/14 executed locally
- 384-dimensional embeddings
- NVIDIA RTX 4060 Ti 16 GB execution
- 72 reference images
- 12 references per class across 6 classes
- class-level statistics and dispersion
- two-stage identity gating
- nearest-prototype, centroid, margin, dispersion and kNN signals
- held-out/OOD-oriented evaluation work

## Depth baseline

Depth Anything V2 Small was implemented with explicit local checkpoint/cache handling.

Recorded execution evidence:

| Execution | Measurement |
|---|---:|
| RTX 4060 Ti warm latency | 164.8 ms |
| RTX 4060 Ti minimum observed latency | 88.2 ms |
| CPU latency | 191.7 ms |

These measurements describe the depth-model execution path only.

## Temporal baseline

P0.6 implemented:

- canonical SI sensor units
- sliding-window extraction
- gravity separation
- jerk and rolling-energy transforms
- 18-element classical feature extraction
- 4-state hysteresis state machine
- hand-to-mouth gesture analysis
- hard-negative handling
- separate drinking gesture path
- jaw/swallow evidence contracts
- replay/evaluation infrastructure

## Simulated power model

The project contains an analytical power model for exploring event-triggered sensing.

One documented scenario estimated approximately **58.1 mAh/day** for 40 camera wakeups of 3 seconds each.

This result is explicitly tagged:

```text
SIMULATED_POWER_BUDGET
```

It is **not** a measured battery result.

## Physical IMU capture foundation

P0.6.1 implemented:

- physical capture domain records
- explicit mount/sensor metadata
- SHA-256 file integrity
- local mobile sensor capture
- CSV/JSONL importing
- SI conversion
- fail-closed timestamp inference
- sample-rate/jitter/gap auditing
- estimated dropped-sample reporting
- non-monotonic timestamp detection
- consent/provenance validation

At the source snapshot, live physical capture remained pending operator execution.

## Evidence rule

A result is only described at the strongest level actually supported by the source:

```text
software behavior
≠ simulation
≠ reference-fixture result
≠ controlled physical measurement
≠ wearable field validation
```
