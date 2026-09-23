from __future__ import annotations

import math
from typing import Sequence

from edith_intake.domain import ImuSample, SensorSample, TimingQualityReport


class TimingQualityAuditor:
    """Audit sensor-stream timing without silently hiding defects."""

    def __init__(
        self,
        gap_threshold_factor: float = 2.5,
        max_rate_deviation_percent: float = 25.0,
        max_allowed_gaps: int = 0,
    ) -> None:
        self.gap_threshold_factor = gap_threshold_factor
        self.max_rate_deviation_percent = max_rate_deviation_percent
        self.max_allowed_gaps = max_allowed_gaps

    def audit(
        self,
        samples: Sequence[ImuSample | SensorSample],
        nominal_sample_rate_hz: float = 50.0,
    ) -> TimingQualityReport:
        if not samples:
            return TimingQualityReport(
                sample_count=0,
                duration_s=0.0,
                nominal_sample_rate_hz=nominal_sample_rate_hz,
                measured_mean_sample_rate_hz=0.0,
                median_interval_ms=0.0,
                p95_interval_ms=0.0,
                max_interval_ms=0.0,
                jitter_std_ms=0.0,
                gap_count=0,
                dropped_sample_estimate=0,
                non_monotonic_timestamp_count=0,
                is_acceptable=False,
                unacceptable_reasons=("empty_stream",),
            )

        timestamps_ns = [sample.timestamp_ns for sample in samples]
        duration_s = max(
            0.0,
            (timestamps_ns[-1] - timestamps_ns[0]) / 1_000_000_000.0,
        )

        nominal_interval_ms = (
            1000.0 / nominal_sample_rate_hz
            if nominal_sample_rate_hz > 0
            else 20.0
        )
        gap_limit_ms = nominal_interval_ms * self.gap_threshold_factor

        intervals_ms: list[float] = []
        non_monotonic_count = 0
        gap_count = 0
        dropped_sample_estimate = 0

        for previous, current in zip(timestamps_ns, timestamps_ns[1:]):
            dt_ns = current - previous
            dt_ms = dt_ns / 1_000_000.0

            if dt_ns <= 0:
                non_monotonic_count += 1

            intervals_ms.append(dt_ms)

            if dt_ms > gap_limit_ms:
                gap_count += 1
                dropped_sample_estimate += max(
                    0,
                    int(round(dt_ms / nominal_interval_ms)) - 1,
                )

        measured_rate_hz = (
            (len(samples) - 1) / duration_s
            if duration_s > 0
            else 0.0
        )

        sorted_intervals = sorted(intervals_ms)
        mean_interval_ms = sum(intervals_ms) / len(intervals_ms)
        jitter_std_ms = math.sqrt(
            sum((x - mean_interval_ms) ** 2 for x in intervals_ms)
            / len(intervals_ms)
        )

        reasons: list[str] = []

        if non_monotonic_count:
            reasons.append(
                f"non_monotonic_timestamps_detected_{non_monotonic_count}"
            )

        if gap_count > self.max_allowed_gaps:
            reasons.append(
                f"gap_count_exceeded_{gap_count}_vs_max_{self.max_allowed_gaps}"
            )

        if nominal_sample_rate_hz > 0:
            rate_deviation = (
                abs(measured_rate_hz - nominal_sample_rate_hz)
                / nominal_sample_rate_hz
                * 100.0
            )
            if rate_deviation > self.max_rate_deviation_percent:
                reasons.append(
                    f"sample_rate_deviation_{rate_deviation:.1f}%"
                    f"_exceeds_max_{self.max_rate_deviation_percent}%"
                )

        p95_index = max(
            0,
            min(
                int(math.ceil(0.95 * len(sorted_intervals))) - 1,
                len(sorted_intervals) - 1,
            ),
        )

        return TimingQualityReport(
            sample_count=len(samples),
            duration_s=duration_s,
            nominal_sample_rate_hz=nominal_sample_rate_hz,
            measured_mean_sample_rate_hz=measured_rate_hz,
            median_interval_ms=sorted_intervals[len(sorted_intervals) // 2],
            p95_interval_ms=sorted_intervals[p95_index],
            max_interval_ms=sorted_intervals[-1],
            jitter_std_ms=jitter_std_ms,
            gap_count=gap_count,
            dropped_sample_estimate=dropped_sample_estimate,
            non_monotonic_timestamp_count=non_monotonic_count,
            is_acceptable=not reasons,
            unacceptable_reasons=tuple(reasons),
        )


# Curated from the private EDITH Intake implementation.
# Domain types are intentionally not mirrored into this portfolio repository.
