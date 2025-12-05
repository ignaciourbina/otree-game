# Simulations API Reference

Complete API documentation for `simulations.runner`.

## Overview

The simulations module provides a command-line interface for running batch experiments on the formal models. It generates CSV datasets and visualizations for statistical analysis.

```bash
# Run simulations with default parameters
python -m simulations.runner

# Custom output directory
python -m simulations.runner --output-dir ./results --tag experiment_v1
```

---

## Command-Line Interface

### Basic Usage

```bash
python -m simulations.runner [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--output-dir` | `PATH` | `out/simulations` | Directory for results |
| `--tag` | `STRING` | — | Custom label appended to run ID |
| `--skip-plots` | `FLAG` | `False` | Suppress PNG generation |

### Output Structure

```
out/simulations/
└── 2024-01-15_14-30-00_experiment_v1/
    ├── simple_delta_sweep.csv
    ├── simple_growth_sweep.csv
    ├── dynamic_growth_sweep.csv
    ├── extinction_vs_delta.png
    ├── extinction_vs_growth.png
    └── delta_star_vs_growth.png
```

---

## Configuration Classes

### `SimpleModelConfig`

Configuration for `SimpleAIGrowthRiskModel` experiments.

```python
@dataclass(frozen=True)
class SimpleModelConfig:
    c0: float = 1.0
    g: float = 0.10
    delta_: float = 0.01
    gamma: float = 2.0
    target_v: float = 6.0
    delta_grid: Sequence[float] = (0.001, 0.0025, 0.005, ...)
    growth_grid: Sequence[float] = (0.02, 0.04, 0.06, ...)
```

#### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `c0` | `float` | `1.0` | Initial consumption |
| `g` | `float` | `0.10` | Baseline growth rate |
| `delta_` | `float` | `0.01` | Baseline hazard rate |
| `gamma` | `float` | `2.0` | CRRA coefficient |
| `target_v` | `float` | `6.0` | VSL calibration target |
| `delta_grid` | `Sequence[float]` | 10 values | δ sweep range |
| `growth_grid` | `Sequence[float]` | 10 values | g sweep range |

---

### `DynamicModelConfig`

Configuration for `DynamicAIGrowthRiskModel` experiments.

```python
@dataclass(frozen=True)
class DynamicModelConfig:
    c0: float = 1.0
    N0: float = 1.0
    gamma: float = 2.0
    target_v: float = 6.0
    rho_minus_b: float = 0.01
    g0: float = 0.02
    m0: float = 0.01
    ai_growth_grid: Sequence[float] = (0.02, 0.04, ..., 0.30)
    ai_mortality_grid: Sequence[float] = (0.0, 0.0025, ..., 0.05)
```

#### Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `rho_minus_b` | `float` | `0.01` | Effective discount rate (ρ - b) |
| `g0` | `float` | `0.02` | Baseline growth (no AI) |
| `m0` | `float` | `0.01` | Baseline mortality |
| `ai_growth_grid` | `Sequence[float]` | 12 values | AI growth sweep range |
| `ai_mortality_grid` | `Sequence[float]` | 12 values | AI mortality sweep range |

---

## Helper Functions

### `_write_csv`

Write rows to a CSV file.

```python
def _write_csv(
    path: Path, 
    rows: Sequence[Mapping[str, object]]
) -> None
```

Features:
- Auto-detects column headers from row keys
- Creates parent directories as needed
- UTF-8 encoding

---

### `_augment_rows`

Attach metadata to each row in a dataset.

```python
def _augment_rows(
    rows: Iterable[Mapping[str, object]], 
    metadata: Mapping[str, object]
) -> List[Dict[str, object]]
```

#### Example

```python
rows = [{"delta": 0.01, "T_star": 45.2}]
metadata = {"experiment": "delta_sweep", "gamma": 2.0}
augmented = _augment_rows(rows, metadata)
# [{"experiment": "delta_sweep", "gamma": 2.0, "delta": 0.01, "T_star": 45.2}]
```

---

### `_plot_line_chart`

Generate a simple line chart from data.

```python
def _plot_line_chart(
    rows: Sequence[Mapping[str, object]],
    *,
    x_key: str,
    y_key: str,
    title: str,
    x_label: str,
    y_label: str,
    output_path: Path,
) -> Path
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `rows` | `Sequence[Mapping]` | Data rows |
| `x_key` | `str` | Key for x-axis values |
| `y_key` | `str` | Key for y-axis values |
| `title` | `str` | Chart title |
| `x_label` | `str` | X-axis label |
| `y_label` | `str` | Y-axis label |
| `output_path` | `Path` | Output PNG path |

#### Returns

`Path` — Path to generated PNG file

---

## Programmatic Usage

### Custom Parameter Sweeps

```python
from simulations.runner import SimpleModelConfig, DynamicModelConfig
from formal_model.jones_models import SimpleAIGrowthRiskModel

# Define custom grid
config = SimpleModelConfig(
    gamma=3.0,  # Higher risk aversion
    delta_grid=(0.005, 0.010, 0.015, 0.020),
)

# Run sweep manually
model = SimpleAIGrowthRiskModel(
    gamma=config.gamma,
    g=config.g,
    delta_=config.delta_,
)
results = model.comparative_statics_over_delta(list(config.delta_grid))

# Process results
for r in results:
    print(f"δ={r['delta']:.3f} → T*={r['T_star']:.2f}")
```

### Generating Custom Plots

```python
from pathlib import Path
from simulations.runner import _plot_line_chart

data = [
    {"x": 0.01, "y": 45.2},
    {"x": 0.02, "y": 32.1},
    {"x": 0.03, "y": 24.5},
]

_plot_line_chart(
    data,
    x_key="x",
    y_key="y",
    title="Optimal Runtime vs. Hazard",
    x_label="δ",
    y_label="T*",
    output_path=Path("./my_plot.png"),
)
```

---

## Output File Formats

### CSV Structure

All CSV files include:
- Metadata columns (experiment name, timestamp, config values)
- Sweep variable column
- Computed statistics columns

#### Example: `simple_delta_sweep.csv`

```csv
experiment,timestamp,gamma,c0,delta,c_star,T_star,extinction_prob
delta_sweep,2024-01-15T14:30:00,2.0,1.0,0.005,3.2145,11.68,0.0567
delta_sweep,2024-01-15T14:30:00,2.0,1.0,0.010,2.4312,8.89,0.0851
...
```

### PNG Plots

- Resolution: 100 DPI
- Format: PNG with transparent background
- Style: Line chart with circular markers

---

## Integration with Notebooks

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load simulation results
df = pd.read_csv("out/simulations/latest/simple_delta_sweep.csv")

# Custom visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df["delta"], df["extinction_prob"], "o-", linewidth=2)
ax.set_xlabel("Hazard Rate δ", fontsize=12)
ax.set_ylabel("Extinction Probability", fontsize=12)
ax.set_title("Jones (2023) Model: Risk vs. Hazard", fontsize=14)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("custom_plot.png", dpi=150)
```

---

## See Also

- [Formal Model API](./formal-model.md) — Underlying model classes
- [First Experiment Guide](../experiments/first-experiment.md) — Running experiments
- [Architecture Overview](../architecture/README.md) — System design
