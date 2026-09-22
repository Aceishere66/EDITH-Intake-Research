# Sensor-Fusion Strategy

## Core idea

No single sensor solves passive dietary tracking.

The system therefore treats multiple signals as complementary evidence rather than averaging them blindly.

## Candidate flow

```text
IMU / context
      │
      ▼
candidate event
      │
      ▼
short RGB + ToF observation
      │
      ├── perception
      ├── depth / geometry
      └── temporal context
      │
      ▼
cross-signal consistency
      │
      ▼
confidence-aware hypothesis
```

## Temporal consumption reasoning

The quantity of interest is consumption, not simply the initial visible portion.

A future experimental pipeline can compare:

- served state
- intermediate observations
- final remaining state

with:

- segmentation
- temporal tracking
- RGB depth
- ToF constraints
- known-container geometry when justified

## Contradiction handling

Examples:

- IMU suggests intake but vision sees no food/drink
- vision sees a bottle but no consumption sequence occurs
- ToF and monocular depth disagree
- tracking loses the object
- history conflicts with current evidence

Possible responses include:

- collect one additional burst
- lower confidence
- request a focused correction
- classify as false trigger
- preserve only the supported parts of the result

## Experimental requirement

Each fusion addition should be compared on replayable sessions against simpler baselines, for example:

1. RGB only
2. RGB + monocular depth
3. RGB + ToF
4. RGB + ToF + temporal tracking
5. full fusion including IMU/context

A sensor or algorithm should remain only if measured benefit justifies its power, size, cost and complexity.
