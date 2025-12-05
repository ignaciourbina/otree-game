# Formal Model API Reference

Complete API documentation for `formal_model.jones_models`.

## Overview

This module implements the theoretical models from Jones (2023) "The A.I. Dilemma: Growth versus Existential Risk."

```python
from formal_model.jones_models import (
    SimpleAIGrowthRiskModel,
    DynamicAIGrowthRiskModel,
    Utility,
    calibrate_ubar_from_v,
)
```

---

## `calibrate_ubar_from_v`

Calibrate the utility shift parameter ū from a target value of v(c₀).

```python
def calibrate_ubar_from_v(
    c0: float, 
    gamma: float, 
    target_v: float = 6.0
) -> float
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `c0` | `float` | — | Baseline consumption level |
| `gamma` | `float` | — | Relative risk aversion coefficient |
| `target_v` | `float` | `6.0` | Desired value of v(c₀), typically VSL-based |

### Returns

`float` — The calibrated ū value

### Example

```python
ubar = calibrate_ubar_from_v(c0=1.0, gamma=2.0, target_v=6.0)
print(f"Calibrated ū = {ubar:.4f}")
# Output: Calibrated ū = 7.0000
```

### Mathematical Background

Jones (2023) calibrates v(c₀) ≈ 6 to match US value-of-statistical-life estimates. Given:

$$v(c) = \frac{u(c)}{u'(c) \cdot c}$$

For CRRA utility with γ ≠ 1:

$$\bar{u} = \frac{v(c_0) - \frac{1}{1-\gamma}}{c_0^{\gamma-1}}$$

For log utility (γ = 1):

$$\bar{u} = v(c_0) - \ln(c_0)$$

---

## `Utility`

CRRA utility function with level shift.

```python
@dataclass
class Utility:
    gamma: float
    ubar: float
```

### Methods

#### `u(c: float) -> float`

Compute utility u(c).

$$u(c) = \begin{cases}
\bar{u} + \frac{c^{1-\gamma}}{1-\gamma} & \gamma \neq 1 \\
\bar{u} + \ln(c) & \gamma = 1
\end{cases}$$

#### `u_prime(c: float) -> float`

Compute marginal utility u'(c).

$$u'(c) = c^{-\gamma}$$

#### `v(c: float) -> float`

Compute the ratio v(c) = u(c) / (u'(c) · c).

### Example

```python
util = Utility(gamma=2.0, ubar=7.0)

c = 1.0
print(f"u({c}) = {util.u(c):.4f}")      # u(1.0) = 6.0000
print(f"u'({c}) = {util.u_prime(c):.4f}")  # u'(1.0) = 1.0000
print(f"v({c}) = {util.v(c):.4f}")      # v(1.0) = 6.0000
```

---

## `SimpleAIGrowthRiskModel`

Section 2 "run AI for T years" model from Jones (2023).

```python
class SimpleAIGrowthRiskModel:
    def __init__(
        self,
        c0: float = 1.0,
        g: float = 0.10,
        delta_: float = 0.01,
        gamma: float = 2.0,
        ubar: Optional[float] = None,
        target_v: float = 6.0,
    ) -> None
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `c0` | `float` | `1.0` | Initial consumption level |
| `g` | `float` | `0.10` | AI-induced growth rate (10% annually) |
| `delta_` | `float` | `0.01` | Flow rate of existential hazard (1% per year) |
| `gamma` | `float` | `2.0` | CRRA coefficient (relative risk aversion) |
| `ubar` | `Optional[float]` | `None` | Utility shift; auto-calibrated if None |
| `target_v` | `float` | `6.0` | Target v(c₀) for VSL calibration |

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `c0` | `float` | Initial consumption |
| `g` | `float` | Growth rate |
| `delta_` | `float` | Hazard rate |
| `gamma` | `float` | Risk aversion |
| `util` | `Utility` | Utility function instance |

### Methods

#### `c_star() -> float`

Compute optimal consumption threshold c*.

$$c^* = \left[ \frac{1}{\bar{u}} \left( \frac{g}{\delta} + \frac{1}{\gamma - 1} \right) \right]^{1/(\gamma-1)}$$

#### `T_star() -> float`

Compute optimal runtime T*.

$$T^* = \frac{1}{g} \ln\left(\frac{c^*}{c_0}\right)$$

#### `total_extinction_prob() -> float`

Compute total extinction probability.

$$P_{\text{ext}} = 1 - e^{-\delta T^*}$$

#### `summary() -> Dict[str, float]`

Return dictionary of all key statistics.

```python
{
    "c_star": float,
    "T_star": float,
    "extinction_prob": float,
    "ubar": float,
    "gamma": float,
    "g": float,
    "delta": float,
}
```

#### `comparative_statics_over_delta(deltas: List[float]) -> List[Dict[str, float]]`

Sweep over δ values while keeping other parameters fixed.

#### `comparative_statics_over_g(gs: List[float]) -> List[Dict[str, float]]`

Sweep over growth rate g values.

### Example

```python
from formal_model.jones_models import SimpleAIGrowthRiskModel

# Create model with default parameters
model = SimpleAIGrowthRiskModel(gamma=2.0, g=0.10, delta_=0.01)

# Compute optimal values
print(f"Optimal runtime T* = {model.T_star():.2f} years")
print(f"Optimal consumption c* = {model.c_star():.4f}")
print(f"Extinction probability = {model.total_extinction_prob():.2%}")

# Get full summary
summary = model.summary()
for key, value in summary.items():
    print(f"{key}: {value}")
```

### Comparative Statics Example

```python
import matplotlib.pyplot as plt
from formal_model.jones_models import SimpleAIGrowthRiskModel

model = SimpleAIGrowthRiskModel(gamma=2.0)
deltas = [0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
results = model.comparative_statics_over_delta(deltas)

plt.figure(figsize=(10, 6))
plt.plot([r["delta"] for r in results], 
         [r["extinction_prob"] for r in results], 
         marker='o')
plt.xlabel("Flow existential risk (δ)")
plt.ylabel("Total extinction probability")
plt.title("Extinction Risk vs. Hazard Rate")
plt.grid(True, alpha=0.3)
plt.show()
```

---

## `DynamicAIGrowthRiskModel`

Section 3 dynamic adoption model from Jones (2023).

```python
class DynamicAIGrowthRiskModel:
    def __init__(
        self,
        c0: float = 1.0,
        N0: float = 1.0,
        gamma: float = 2.0,
        ubar: Optional[float] = None,
        target_v: float = 6.0,
        rho_minus_b: float = 0.01,
        g0: float = 0.02,
        m0: float = 0.01,
    ) -> None
```

### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `c0` | `float` | `1.0` | Initial consumption |
| `N0` | `float` | `1.0` | Initial population |
| `gamma` | `float` | `2.0` | CRRA coefficient |
| `ubar` | `Optional[float]` | `None` | Utility shift (auto-calibrated) |
| `target_v` | `float` | `6.0` | VSL calibration target |
| `rho_minus_b` | `float` | `0.01` | Discount rate minus fertility (ρ - b) |
| `g0` | `float` | `0.02` | Baseline growth rate (no AI) |
| `m0` | `float` | `0.01` | Baseline mortality rate |

### Key Methods

#### `U(g: float, m: float) -> float`

Compute expected welfare U(g, m) for given growth and mortality.

$$U(g, m) = N_0 \left[ \frac{\bar{u}}{\rho - b + m} + \frac{c_0^{1-\gamma}}{1-\gamma} \cdot \frac{1}{\rho - b + m + (\gamma-1)g} \right]$$

#### `delta_star(g_ai: float, m_ai: float) -> float`

Compute critical risk tolerance δ* for AI adoption.

$$\delta^* = 1 - \frac{U(g_0, m_0)}{U(g_{AI}, m_{AI})}$$

#### `delta_star_singularity(m_ai: float) -> float`

Compute δ* in the singularity limit (g_ai → ∞).

#### `sweep_growth(g_vals: List[float], m_ai: float) -> List[Dict[str, float]]`

Sweep over AI growth rates for fixed mortality reduction.

### Example

```python
from formal_model.jones_models import DynamicAIGrowthRiskModel

# Create model
dyn = DynamicAIGrowthRiskModel(gamma=2.0)

# Compute critical risk for specific AI scenario
g_ai = 0.08  # 8% growth from AI
m_ai = 0.005  # AI reduces mortality by half

delta_critical = dyn.delta_star(g_ai=g_ai, m_ai=m_ai)
print(f"Maximum acceptable one-time risk: δ* = {delta_critical:.2%}")
```

---

## Constants and Defaults

### Default Parameters (Jones 2023 Baseline)

| Parameter | Symbol | Default | Interpretation |
|-----------|--------|---------|----------------|
| Initial consumption | c₀ | 1.0 | Normalized baseline |
| Growth rate | g | 0.10 | 10% annual growth |
| Hazard rate | δ | 0.01 | 1% extinction risk per year |
| Risk aversion | γ | 2.0 | Moderate risk aversion |
| VSL target | v(c₀) | 6.0 | US VSL calibration |

### Parameter Constraints

- `gamma > 0` (risk aversion must be positive)
- `g > 0` (growth must be positive for meaningful AI)
- `delta_ > 0` (hazard rate must be positive)
- `c0 > 0` (consumption must be positive)

---

## See Also

- [Theory Documentation](../theory/README.md) — Mathematical derivations
- [Simulations API](./simulations.md) — Batch experiment runner
- [Cournot Shared Risk API](./cournot-shared-risk.md) — Multi-player extension
