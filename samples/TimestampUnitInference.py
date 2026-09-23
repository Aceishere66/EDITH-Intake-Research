from __future__ import annotations

from typing import Sequence


def infer_timestamp_unit(
    column_name: str,
    raw_values: Sequence[float],
    explicit_unit: str | None = None,
) -> tuple[int, str]:
    """Return multiplier-to-nanoseconds and unit name.

    Ambiguous inputs fail closed instead of guessing.
    """

    if explicit_unit:
        unit = explicit_unit.strip().lower()
        explicit = {
            "ns": (1, "ns"),
            "us": (1_000, "us"),
            "ms": (1_000_000, "ms"),
            "s": (1_000_000_000, "s"),
        }
        if unit not in explicit:
            raise ValueError(
                "Unsupported explicit time unit; expected s, ms, us or ns."
            )
        return explicit[unit]

    name = column_name.strip().lower()

    suffixes = (
        (("_ns", ".ns"), (1, "ns")),
        (("_us", ".us"), (1_000, "us")),
        (("_ms", ".ms"), (1_000_000, "ms")),
        (("_s", ".s"), (1_000_000_000, "s")),
    )

    for endings, result in suffixes:
        if name.endswith(endings):
            return result

    if not raw_values:
        raise ValueError("Cannot infer a timestamp unit from an empty stream.")

    first = raw_values[0]

    # Common Unix-epoch magnitude bands.
    if first >= 1e17:
        return 1, "ns"
    if 1e14 <= first < 1e17:
        return 1_000, "us"
    if 1e11 <= first < 1e14:
        return 1_000_000, "ms"
    if 1e9 <= first < 3e9:
        return 1_000_000_000, "s"

    # This range can represent incompatible interpretations.
    if 3e9 <= first < 1e11:
        raise ValueError(
            "Ambiguous timestamp magnitude. Supply an explicit time unit."
        )

    if len(raw_values) < 2:
        raise ValueError(
            "Cannot infer a relative timestamp unit from one sample."
        )

    deltas = sorted(
        raw_values[i] - raw_values[i - 1]
        for i in range(1, min(len(raw_values), 500))
        if raw_values[i] - raw_values[i - 1] > 0
    )

    if not deltas:
        raise ValueError("Timestamp progression is non-positive.")

    median_dt = deltas[len(deltas) // 2]

    if median_dt < 0.5:
        return 1_000_000_000, "s"
    if median_dt < 500.0:
        return 1_000_000, "ms"
    if median_dt < 500_000.0:
        return 1_000, "us"
    return 1, "ns"


# Curated from EDITH Intake's PhysicalDataImporter.
# The production importer also performs CSV/JSONL parsing, SI conversion,
# SHA-256 provenance validation and timing-quality auditing.
