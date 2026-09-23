# Current Stage and Evidence Boundary

EDITH Intake is an active research/prototyping project with a substantial software baseline, but its core wearable product hypothesis is not yet validated end-to-end.

## Implemented software evidence

At source commit `ed4a563621b8d56f8604bcf5dc76197cae707e03`, the private project records implemented work across:

- perception / open-set identity
- DINOv2 local inference
- semantic verification experiments
- Depth Anything V2 Small local inference
- quantity/geometry ablation infrastructure
- temporal signal processing
- a 4-state event-detection state machine
- IMU capture/import tooling
- timing-quality auditing
- provenance/integrity checks
- CLI/replay/test infrastructure

## Physical evidence boundary

The P0.6.1 software/capture foundation is complete, but the source record explicitly marks:

```text
PHYSICAL_CAPTURE_REQUIRES_USER_ACTION
REAL_IMU_EVIDENCE_GATE = WAITING_FOR_PHYSICAL_CAPTURE
```

Therefore this showcase does **not** claim:

- validated real-world eating-event recall
- validated drinking-event recall
- validated worn-device IMU performance
- validated physical portion/consumption error
- validated daily calorie error
- all-day measured battery life
- final wearable ergonomics

## Simulation/reference boundary

The project also contains simulation and reference-harness work.

Those results are useful for software verification but are not silently promoted into physical-product claims.

Examples:

- simulated energy models remain explicitly labeled `SIMULATED_POWER_BUDGET`
- reference depth/quantity fixtures remain distinct from scale-ground-truthed physical food samples
- physical sample count remains explicit when zero

## Current engineering value

Even before full wearable validation, the project demonstrates:

- computer-vision experimentation
- open-set classification/rejection
- local AI inference
- sensor-data schemas
- signal preprocessing
- temporal state machines
- multimodal architecture
- provenance/integrity controls
- evidence-aware experimentation
