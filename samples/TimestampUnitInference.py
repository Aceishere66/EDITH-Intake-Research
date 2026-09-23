# Exact excerpt from EDITH Intake's private PhysicalDataImporter.
# The surrounding importer handles CSV/JSONL parsing, SI conversion,
# SHA-256 provenance and timing-quality validation.

from __future__ import annotations

from typing import Sequence

def infer_timestamp_unit(
    col_name: str,
    raw_values: Sequence[float],
    explicit_unit: str | None = None,
) -> tuple[int, str]:
    """Deterministically determine multiplier to convert timestamps to integer nanoseconds.

    Returns (multiplier_to_ns, detected_unit_name).
    Fails closed by raising ValueError if unit inference is ambiguous or unsupported.
    """
    if explicit_unit is not None and explicit_unit.strip() != "":
        u = explicit_unit.strip().lower()
        if u in ("ns", "nanos", "nanoseconds"):
            return 1, "ns"
        if u in ("us", "micros", "microseconds", "µs"):
            return 1_000, "us"
        if u in ("ms", "millis", "milliseconds"):
            return 1_000_000, "ms"
        if u in ("s", "sec", "secs", "seconds"):
            return 1_000_000_000, "s"
        raise ValueError(
            f"Unsupported explicit time_unit: '{explicit_unit}'. Must be one of ('s', 'ms', 'us', 'ns')"
        )

    col_lower = col_name.strip().lower()

    # Deterministic column suffix matching
    if col_lower.endswith(("_ns", ".ns")) or col_lower in ("timestamp_ns", "time_ns", "epoch_ns", "t_ns", "ns"):
        return 1, "ns"
    if col_lower.endswith(("_us", ".us", "_micros")) or col_lower in (
        "timestamp_us",
        "time_us",
        "epoch_us",
        "t_us",
        "us",
        "micros",
    ):
        return 1_000, "us"
    if col_lower.endswith(("_ms", ".ms", "_millis")) or col_lower in (
        "timestamp_ms",
        "time_ms",
        "epoch_ms",
        "t_ms",
        "ms",
        "millis",
    ):
        return 1_000_000, "ms"
    if col_lower.endswith(("_s", ".s", "_sec", "_secs", "_seconds")) or col_lower in (
        "timestamp_s",
        "time_s",
        "epoch_s",
        "t_s",
        "s",
        "sec",
    ):
        return 1_000_000_000, "s"

    # Generic column (e.g. timestamp, time, t, epoch, date)
    if not raw_values:
        raise ValueError(f"Cannot infer timestamp unit for empty values under column '{col_name}'")

    t0 = raw_values[0]

    # Unix epoch ranges
    if t0 >= 1e17:  # e.g. ~1.725e18 ns
        return 1, "ns"
    if 1e14 <= t0 < 1e17:  # e.g. ~1.725e15 us
        return 1_000, "us"
    if 1e11 <= t0 < 1e14:  # e.g. ~1.725e12 ms
        return 1_000_000, "ms"
    if 1e9 <= t0 < 3e9:  # e.g. ~1.725e9 s
        return 1_000_000_000, "s"

    if 3e9 <= t0 < 1e11:
        raise ValueError(
            f"Ambiguous timestamp magnitude ({t0}) under column '{col_name}'. "
            f"Cannot distinguish epoch vs relative units. Please specify explicit --time-unit (s, ms, us, ns)."
        )

    # Relative timestamps (t0 < 1e9)
    if len(raw_values) < 2:
        raise ValueError(
            f"Cannot infer timestamp unit for single relative timestamp ({t0}) under column '{col_name}'. "
            f"Please specify explicit --time-unit (s, ms, us, ns)."
        )

    # Compute median of positive consecutive deltas
    sample_limit = min(len(raw_values), 500)
    deltas = [
        raw_values[i] - raw_values[i - 1]
        for i in range(1, sample_limit)
        if raw_values[i] - raw_values[i - 1] > 0
    ]

    if not deltas:
        raise ValueError(
            f"Non-positive timestamp progression under column '{col_name}'. "
            f"Please specify explicit --time-unit (s, ms, us, ns)."
        )

    deltas.sort()
    n = len(deltas)
    med_dt = deltas[n // 2] if n % 2 == 1 else (deltas[n // 2 - 1] + deltas[n // 2]) / 2.0

    if med_dt < 0.5:
        # Typical IMU in seconds -> dt in [0.001, 0.1] s
        return 1_000_000_000, "s"
    if 0.5 <= med_dt < 500.0:
        # Typical IMU in ms -> dt in [1, 100] ms
        return 1_000_000, "ms"
    if 500.0 <= med_dt < 500_000.0:
        # Typical IMU in us -> dt in [1000, 100000] us
        return 1_000, "us"
    if med_dt >= 500_000.0:
        # Typical IMU in ns -> dt in [1000000, 100000000] ns
        return 1, "ns"

    raise ValueError(
        f"Unable to determine timestamp unit for column '{col_name}' (median dt={med_dt}). "
        f"Please specify explicit --time-unit (s, ms, us, ns)."
    )
