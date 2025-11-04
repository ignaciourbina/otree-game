"""Experiment runner for comparative statics on the formal model module.

The script orchestrates a set of parametric experiments on the
:mod:`formal_model.jones_models` classes.  The resulting datasets are
persisted as CSV files that are ready for further statistical analysis
(e.g., plotting or regression work in a notebook environment).

Usage
-----
Run the experiments with the default parameter grids::

    python -m simulations.runner

The command produces a timestamped directory inside ``simulations/data``
containing one CSV file per experiment.  Use ``--output-dir`` to change
where results are written and ``--tag`` to append a custom label to the
run identifier.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

from formal_model.jones_models import (
    DynamicAIGrowthRiskModel,
    SimpleAIGrowthRiskModel,
)


# ---------------------------------------------------------------------------
# Configuration dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SimpleModelConfig:
    """Configuration for experiments on :class:`SimpleAIGrowthRiskModel`."""

    c0: float = 1.0
    g: float = 0.10
    delta_: float = 0.01
    gamma: float = 2.0
    target_v: float = 6.0
    delta_grid: Sequence[float] = (
        0.001,
        0.0025,
        0.005,
        0.0075,
        0.01,
        0.015,
        0.02,
        0.03,
        0.04,
        0.05,
    )
    growth_grid: Sequence[float] = (
        0.02,
        0.04,
        0.06,
        0.08,
        0.10,
        0.12,
        0.14,
        0.16,
        0.18,
        0.20,
    )


@dataclass(frozen=True)
class DynamicModelConfig:
    """Configuration for :class:`DynamicAIGrowthRiskModel` experiments."""

    c0: float = 1.0
    N0: float = 1.0
    gamma: float = 2.0
    target_v: float = 6.0
    rho_minus_b: float = 0.01
    g0: float = 0.02
    m0: float = 0.01
    ai_growth_grid: Sequence[float] = (
        0.02,
        0.04,
        0.06,
        0.08,
        0.10,
        0.12,
        0.14,
        0.16,
        0.18,
        0.20,
        0.25,
        0.30,
    )
    ai_mortality_grid: Sequence[float] = (
        0.0,
        0.0025,
        0.005,
        0.0075,
        0.01,
        0.015,
        0.02,
        0.03,
        0.04,
        0.05,
    )


# ---------------------------------------------------------------------------
# CSV helpers
# ---------------------------------------------------------------------------


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    """Write ``rows`` to ``path`` using :mod:`csv`.

    The helper collects the union of keys across all rows in insertion
    order so that metadata columns appear before experiment-specific
    statistics.
    """

    if not rows:
        raise ValueError("Cannot write an empty dataset to CSV.")

    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _augment_rows(
    rows: Iterable[Mapping[str, object]], metadata: Mapping[str, object]
) -> List[Dict[str, object]]:
    """Attach ``metadata`` to each dictionary in ``rows``."""

    augmented: List[Dict[str, object]] = []
    for row in rows:
        combined: Dict[str, object] = dict(metadata)
        combined.update(row)
        augmented.append(combined)
    return augmented


# ---------------------------------------------------------------------------
# Experiment implementations
# ---------------------------------------------------------------------------


def _run_simple_model_delta_sweep(
    output_dir: Path, run_id: str, config: SimpleModelConfig
) -> Path:
    model = SimpleAIGrowthRiskModel(
        c0=config.c0,
        g=config.g,
        delta_=config.delta_,
        gamma=config.gamma,
        target_v=config.target_v,
    )
    metadata = {
        "run_id": run_id,
        "experiment": "simple_model_delta_sweep",
        "model": "SimpleAIGrowthRiskModel",
        "baseline_c0": config.c0,
        "baseline_g": config.g,
        "baseline_delta": config.delta_,
        "baseline_gamma": config.gamma,
        "target_v": config.target_v,
    }
    rows = _augment_rows(model.comparative_statics_over_delta(config.delta_grid), metadata)
    output_path = output_dir / "simple_model_delta_sweep.csv"
    _write_csv(output_path, rows)
    return output_path


def _run_simple_model_growth_sweep(
    output_dir: Path, run_id: str, config: SimpleModelConfig
) -> Path:
    model = SimpleAIGrowthRiskModel(
        c0=config.c0,
        g=config.g,
        delta_=config.delta_,
        gamma=config.gamma,
        target_v=config.target_v,
    )
    metadata = {
        "run_id": run_id,
        "experiment": "simple_model_growth_sweep",
        "model": "SimpleAIGrowthRiskModel",
        "baseline_c0": config.c0,
        "baseline_g": config.g,
        "baseline_delta": config.delta_,
        "baseline_gamma": config.gamma,
        "target_v": config.target_v,
    }
    rows = _augment_rows(model.comparative_statics_over_g(config.growth_grid), metadata)
    output_path = output_dir / "simple_model_growth_sweep.csv"
    _write_csv(output_path, rows)
    return output_path


def _run_dynamic_model_mortality_sweep(
    output_dir: Path, run_id: str, config: DynamicModelConfig
) -> Path:
    model = DynamicAIGrowthRiskModel(
        c0=config.c0,
        N0=config.N0,
        gamma=config.gamma,
        target_v=config.target_v,
        rho_minus_b=config.rho_minus_b,
        g0=config.g0,
        m0=config.m0,
    )
    metadata = {
        "run_id": run_id,
        "experiment": "dynamic_model_mortality_sweep",
        "model": "DynamicAIGrowthRiskModel",
        "baseline_c0": config.c0,
        "baseline_N0": config.N0,
        "baseline_gamma": config.gamma,
        "baseline_rho_minus_b": config.rho_minus_b,
        "baseline_g0": config.g0,
        "baseline_m0": config.m0,
        "target_v": config.target_v,
    }
    rows = _augment_rows(
        model.sweep_mortality(g_ai=config.ai_growth_grid[-1], m_vals=config.ai_mortality_grid),
        {**metadata, "g_ai_for_sweep": config.ai_growth_grid[-1]},
    )
    output_path = output_dir / "dynamic_model_mortality_sweep.csv"
    _write_csv(output_path, rows)
    return output_path


def _run_dynamic_model_growth_sweep(
    output_dir: Path, run_id: str, config: DynamicModelConfig
) -> Path:
    model = DynamicAIGrowthRiskModel(
        c0=config.c0,
        N0=config.N0,
        gamma=config.gamma,
        target_v=config.target_v,
        rho_minus_b=config.rho_minus_b,
        g0=config.g0,
        m0=config.m0,
    )
    metadata = {
        "run_id": run_id,
        "experiment": "dynamic_model_growth_sweep",
        "model": "DynamicAIGrowthRiskModel",
        "baseline_c0": config.c0,
        "baseline_N0": config.N0,
        "baseline_gamma": config.gamma,
        "baseline_rho_minus_b": config.rho_minus_b,
        "baseline_g0": config.g0,
        "baseline_m0": config.m0,
        "target_v": config.target_v,
    }
    rows = _augment_rows(
        model.sweep_growth(g_vals=config.ai_growth_grid, m_ai=config.ai_mortality_grid[3]),
        {**metadata, "m_ai_for_sweep": config.ai_mortality_grid[3]},
    )
    output_path = output_dir / "dynamic_model_growth_sweep.csv"
    _write_csv(output_path, rows)
    return output_path


def _run_dynamic_model_singularity_limit(
    output_dir: Path, run_id: str, config: DynamicModelConfig
) -> Path:
    model = DynamicAIGrowthRiskModel(
        c0=config.c0,
        N0=config.N0,
        gamma=config.gamma,
        target_v=config.target_v,
        rho_minus_b=config.rho_minus_b,
        g0=config.g0,
        m0=config.m0,
    )
    metadata = {
        "run_id": run_id,
        "experiment": "dynamic_model_singularity_limit",
        "model": "DynamicAIGrowthRiskModel",
        "baseline_c0": config.c0,
        "baseline_N0": config.N0,
        "baseline_gamma": config.gamma,
        "baseline_rho_minus_b": config.rho_minus_b,
        "baseline_g0": config.g0,
        "baseline_m0": config.m0,
        "target_v": config.target_v,
    }
    rows = []
    for m_ai in config.ai_mortality_grid:
        rows.append({"m_ai": m_ai, "delta_star": model.delta_star_singularity(m_ai)})
    rows = _augment_rows(rows, metadata)
    output_path = output_dir / "dynamic_model_singularity_limit.csv"
    _write_csv(output_path, rows)
    return output_path


# ---------------------------------------------------------------------------
# Public orchestration API
# ---------------------------------------------------------------------------


def run_all_experiments(output_dir: Path, run_id: str | None = None) -> List[Path]:
    """Execute all configured experiments and return generated file paths."""

    run_identifier = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_dir = output_dir / run_identifier
    experiment_dir.mkdir(parents=True, exist_ok=True)

    simple_config = SimpleModelConfig()
    dynamic_config = DynamicModelConfig()

    generated_files = [
        _run_simple_model_delta_sweep(experiment_dir, run_identifier, simple_config),
        _run_simple_model_growth_sweep(experiment_dir, run_identifier, simple_config),
        _run_dynamic_model_mortality_sweep(experiment_dir, run_identifier, dynamic_config),
        _run_dynamic_model_growth_sweep(experiment_dir, run_identifier, dynamic_config),
        _run_dynamic_model_singularity_limit(
            experiment_dir, run_identifier, dynamic_config
        ),
    ]

    return generated_files


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "data",
        help="Directory where experiment outputs will be stored.",
    )
    parser.add_argument(
        "--tag",
        type=str,
        default=None,
        help="Optional label to append to the run identifier.",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_id = f"{timestamp}_{args.tag}" if args.tag else timestamp

    generated_files = run_all_experiments(args.output_dir, run_id=run_id)

    print("Generated the following datasets:")
    for path in generated_files:
        print(f" - {path.relative_to(path.parent.parent)}")


if __name__ == "__main__":
    main()
