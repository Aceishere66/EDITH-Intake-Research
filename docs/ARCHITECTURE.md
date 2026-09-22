# System Architecture

## Compute split

Early prototypes deliberately keep the wearable simple and place heavier inference on a paired phone.

```text
┌──────────────────────────────┐
│ Wearable                     │
│ IMU / RGB / ToF              │
│ timestamps / buffering       │
│ event gating / transport     │
└──────────────┬───────────────┘
               │ BLE / Wi-Fi / USB during R&D
               ▼
┌──────────────────────────────┐
│ Paired phone                 │
│ event engine                 │
│ perception                   │
│ geometry / depth             │
│ sensor fusion                │
│ confidence / decision        │
│ persistence                  │
└──────────────┬───────────────┘
               ▼
           EDITH Fit
```

## Power-state concept

```text
IDLE
  │ low-power IMU
  ▼
CANDIDATE
  │
  ▼
VERIFY
  │ short RGB/ToF burst
  ├── false trigger → IDLE
  ▼
SESSION
  │ sparse temporal observations
  ▼
FINALIZE
  ▼
IDLE
```

Continuous high-rate video is not the default architecture.

## Stable interfaces

Hardware-specific implementations should sit behind narrow adapters such as:

- IMU adapter
- RGB camera adapter
- depth adapter
- battery adapter
- transport adapter
- calibration service

This allows sensor choices to change without redesigning the entire inference pipeline.

## Evidence model

Raw observations should retain:

- timestamps
- sensor/device identity
- calibration/version metadata
- measurement payload
- quality/status flags
- power state

AI/model output is treated as evidence contributing to a hypothesis rather than unquestioned truth.

## Phone responsibilities

The paired phone is expected to perform heavier work such as:

- segmentation/tracking
- recognition
- depth processing
- multimodal fusion
- confidence handling
- nutrition-data resolution
- user confirmation when needed
