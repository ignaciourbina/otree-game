"""Experiment runner for comparative statics on the formal model module.

The script orchestrates a set of parametric experiments on the
:mod:`formal_model.jones_models` classes.  The resulting datasets are
persisted as CSV files that are ready for further statistical analysis
(e.g., plotting or regression work in a notebook environment).

Usage
-----
Run the experiments with the default parameter grids::

    python -m simulations.runner

The command produces a timestamped directory inside ``out/simulations``
containing one CSV file per experiment plus companion PNG plots.  Use
``--output-dir`` to change where results are written, ``--tag`` to append
a custom label to the run identifier, and ``--skip-plots`` to suppress
figure generation.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

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


_PYPLOT = None


def _lazy_import_pyplot():
    """Import matplotlib lazily to avoid forcing the dependency when unused."""

    global _PYPLOT
    if _PYPLOT is None:
        try:
            import matplotlib

            matplotlib.use("Agg", force=True)
            import matplotlib.pyplot as plt
        except ImportError as exc:  # pragma: no cover - dependency sanity
            raise RuntimeError(
                "Matplotlib is required to generate plots. Install it or pass --skip-plots."
            ) from exc
        _PYPLOT = plt
    return _PYPLOT


def _plot_line_chart(
    rows: Sequence[Mapping[str, object]],
    *,
    x_key: str,
    y_key: str,
    title: str,
    x_label: str,
    y_label: str,
    output_path: Path,
) -> Path:
    """Render a simple line chart for the provided dataset."""

    if not rows:
        raise ValueError("Cannot plot an empty dataset.")

    plt = _lazy_import_pyplot()
    xs = [float(row[x_key]) for row in rows]
    ys = [float(row[y_key]) for row in rows]

    fig, ax = plt.subplots()
    ax.plot(xs, ys, marker="o")
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
    return output_path


@dataclass
class ExperimentArtifact:
    """Container for experiment outputs."""

    csv_path: Path
    plot_path: Optional[Path] = None


# ---------------------------------------------------------------------------
# Experiment implementations
# ---------------------------------------------------------------------------


def _run_simple_model_delta_sweep(
    output_dir: Path, run_id: str, config: SimpleModelConfig, make_plots: bool
) -> ExperimentArtifact:
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
    plot_path = None
    if make_plots:
        plot_path = _plot_line_chart(
            rows,
            x_key="delta",
            y_key="extinction_prob",
            title="Simple model: extinction probability vs flow risk",
            x_label="flow existential risk δ",
            y_label="overall extinction probability 1 - e^{-δ T*}",
            output_path=output_dir / "simple_model_delta_sweep.png",
        )
    return ExperimentArtifact(csv_path=output_path, plot_path=plot_path)


def _run_simple_model_growth_sweep(
    output_dir: Path, run_id: str, config: SimpleModelConfig, make_plots: bool
) -> ExperimentArtifact:
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
    plot_path = None
    if make_plots:
        plot_path = _plot_line_chart(
            rows,
            x_key="g",
            y_key="extinction_prob",
            title="Simple model: extinction probability vs AI-driven growth",
            x_label="AI-boosted growth rate g",
            y_label="overall extinction probability 1 - e^{-δ T*}",
            output_path=output_dir / "simple_model_growth_sweep.png",
        )
    return ExperimentArtifact(csv_path=output_path, plot_path=plot_path)


def _run_dynamic_model_mortality_sweep(
    output_dir: Path, run_id: str, config: DynamicModelConfig, make_plots: bool
) -> ExperimentArtifact:
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
    plot_path = None
    if make_plots:
        g_for_label = float(rows[0]["g_ai_for_sweep"])
        title = f"Dynamic model: δ* vs mortality (g_ai={g_for_label:.3f})"
        plot_path = _plot_line_chart(
            rows,
            x_key="m_ai",
            y_key="delta_star",
            title=title,
            x_label="AI mortality shift m_ai",
            y_label="max acceptable one-time risk δ*",
            output_path=output_dir / "dynamic_model_mortality_sweep.png",
        )
    return ExperimentArtifact(csv_path=output_path, plot_path=plot_path)


def _run_dynamic_model_growth_sweep(
    output_dir: Path, run_id: str, config: DynamicModelConfig, make_plots: bool
) -> ExperimentArtifact:
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
    plot_path = None
    if make_plots:
        m_for_label = float(rows[0]["m_ai_for_sweep"])
        title = f"Dynamic model: δ* vs growth (m_ai={m_for_label:.4f})"
        plot_path = _plot_line_chart(
            rows,
            x_key="g_ai",
            y_key="delta_star",
            title=title,
            x_label="AI growth g_ai",
            y_label="max acceptable one-time risk δ*",
            output_path=output_dir / "dynamic_model_growth_sweep.png",
        )
    return ExperimentArtifact(csv_path=output_path, plot_path=plot_path)


def _run_dynamic_model_singularity_limit(
    output_dir: Path, run_id: str, config: DynamicModelConfig, make_plots: bool
) -> ExperimentArtifact:
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
    plot_path = None
    if make_plots:
        plot_path = _plot_line_chart(
            rows,
            x_key="m_ai",
            y_key="delta_star",
            title="Dynamic model: singularity limit δ* vs mortality",
            x_label="AI mortality shift m_ai",
            y_label="max acceptable one-time risk δ*",
            output_path=output_dir / "dynamic_model_singularity_limit.png",
        )
    return ExperimentArtifact(csv_path=output_path, plot_path=plot_path)


# ---------------------------------------------------------------------------
# Public orchestration API
# ---------------------------------------------------------------------------


def run_all_experiments(
    output_dir: Path, run_id: str | None = None, make_plots: bool = True
) -> List[ExperimentArtifact]:
    """Execute all configured experiments and return generated artifacts."""

    run_identifier = run_id or datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_dir = output_dir / run_identifier
    experiment_dir.mkdir(parents=True, exist_ok=True)

    simple_config = SimpleModelConfig()
    dynamic_config = DynamicModelConfig()

    generated_files = [
        _run_simple_model_delta_sweep(
            experiment_dir, run_identifier, simple_config, make_plots
        ),
        _run_simple_model_growth_sweep(
            experiment_dir, run_identifier, simple_config, make_plots
        ),
        _run_dynamic_model_mortality_sweep(
            experiment_dir, run_identifier, dynamic_config, make_plots
        ),
        _run_dynamic_model_growth_sweep(
            experiment_dir, run_identifier, dynamic_config, make_plots
        ),
        _run_dynamic_model_singularity_limit(
            experiment_dir, run_identifier, dynamic_config, make_plots
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
        default=Path(__file__).resolve().parent.parent / "out" / "simulations",
        help="Directory where experiment outputs will be stored (default: out/simulations).",
    )
    parser.add_argument(
        "--skip-plots",
        action="store_true",
        help="Skip Matplotlib plot generation and only emit CSV datasets.",
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

    generated_files = run_all_experiments(
        args.output_dir, run_id=run_id, make_plots=not args.skip_plots
    )

    print("Generated datasets:")
    for artifact in generated_files:
        try:
            csv_rel = artifact.csv_path.relative_to(args.output_dir)
        except ValueError:
            csv_rel = artifact.csv_path
        print(f" - {csv_rel}")
        if artifact.plot_path:
            try:
                plot_rel = artifact.plot_path.relative_to(args.output_dir)
            except ValueError:
                plot_rel = artifact.plot_path
            print(f"   plot -> {plot_rel}")


if __name__ == "__main__":
    main()
