from __future__ import annotations

import math
from typing import Sequence

from edith_intake.domain import ImuSample, SensorSample, TimingQualityReport


class TimingQualityAuditor:
    """Rigorous timing quality auditor for inertial sensor streams.
    Never silently resamples or interpolates away timing defects.
    """

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
        """Audit timestamps across a sequence of samples."""
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

        sample_count = len(samples)
        if sample_count == 1:
            return TimingQualityReport(
                sample_count=1,
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
                unacceptable_reasons=("insufficient_samples_for_duration",),
            )

        timestamps_ns = [s.timestamp_ns for s in samples]
        t_start = timestamps_ns[0]
        t_end = timestamps_ns[-1]
        duration_s = max(0.0, (t_end - t_start) / 1_000_000_000.0)

        intervals_ms: list[float] = []
        non_monotonic_count = 0
        nominal_interval_ms = (1.0 / nominal_sample_rate_hz) * 1000.0 if nominal_sample_rate_hz > 0 else 20.0
        gap_limit_ms = nominal_interval_ms * self.gap_threshold_factor

        gap_count = 0
        dropped_sample_estimate = 0

        for i in range(1, sample_count):
            dt_ns = timestamps_ns[i] - timestamps_ns[i - 1]
            dt_ms = dt_ns / 1_000_000.0

            if dt_ns <= 0:
                non_monotonic_count += 1

            intervals_ms.append(dt_ms)

            if dt_ms > gap_limit_ms:
                gap_count += 1
                missing = max(0, int(round(dt_ms / nominal_interval_ms)) - 1)
                dropped_sample_estimate += missing

        measured_rate_hz = ((sample_count - 1) / duration_s) if duration_s > 0 else 0.0

        sorted_intervals = sorted(intervals_ms)
        n_intervals = len(sorted_intervals)

        if n_intervals % 2 == 1:
            median_interval_ms = sorted_intervals[n_intervals // 2]
        else:
            median_interval_ms = (sorted_intervals[n_intervals // 2 - 1] + sorted_intervals[n_intervals // 2]) / 2.0

        p95_idx = int(math.ceil(0.95 * n_intervals)) - 1
        p95_idx = max(0, min(p95_idx, n_intervals - 1))
        p95_interval_ms = sorted_intervals[p95_idx]

        max_interval_ms = sorted_intervals[-1]

        mean_interval_ms = sum(intervals_ms) / float(n_intervals)
        variance = sum((x - mean_interval_ms) ** 2 for x in intervals_ms) / float(n_intervals)
        jitter_std_ms = math.sqrt(variance)

        unacceptable_reasons: list[str] = []

        if non_monotonic_count > 0:
            unacceptable_reasons.append(f"non_monotonic_timestamps_detected_{non_monotonic_count}")

        if gap_count > self.max_allowed_gaps:
            unacceptable_reasons.append(f"gap_count_exceeded_{gap_count}_vs_max_{self.max_allowed_gaps}")

        if nominal_sample_rate_hz > 0:
            rate_dev = abs(measured_rate_hz - nominal_sample_rate_hz) / nominal_sample_rate_hz * 100.0
            if rate_dev > self.max_rate_deviation_percent:
                unacceptable_reasons.append(
                    f"sample_rate_deviation_{rate_dev:.1f}%_exceeds_max_{self.max_rate_deviation_percent}%"
                )

        is_acceptable = len(unacceptable_reasons) == 0

        return TimingQualityReport(
            sample_count=sample_count,
            duration_s=duration_s,
            nominal_sample_rate_hz=nominal_sample_rate_hz,
            measured_mean_sample_rate_hz=measured_rate_hz,
            median_interval_ms=median_interval_ms,
            p95_interval_ms=p95_interval_ms,
            max_interval_ms=max_interval_ms,
            jitter_std_ms=jitter_std_ms,
            gap_count=gap_count,
            dropped_sample_estimate=dropped_sample_estimate,
            non_monotonic_timestamp_count=non_monotonic_count,
            is_acceptable=is_acceptable,
            unacceptable_reasons=tuple(unacceptable_reasons),
        )

# Exact source excerpt from the private EDITH Intake repository.
