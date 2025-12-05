# Cournot Shared Risk API Reference

Complete API documentation for `otree.cournot_shared_risk`.

## Overview

This oTree application implements a two-player strategic game based on the Cournot-style extension of Jones (2023). Players choose AI runtime durations while sharing global existential risk.

```python
from otree.cournot_shared_risk import (
    FIXED,
    TREATMENTS,
    TreatmentArm,
    survival_probability,
    consumption,
    crra_utility,
    payoff,
)
```

---

## Data Classes

### `FixedPrimitives`

Constant parameters shared across all treatments.

```python
@dataclass(frozen=True)
class FixedPrimitives:
    c0: float = 1.0           # Baseline consumption
    delta: float = 0.01       # Baseline hazard intensity
    gamma: float = 2.0        # CRRA coefficient
    token_floor: float = 10.0 # Minimum token payout
    token_scale: float = 150.0 # Token conversion factor
```

#### Usage

```python
from otree.cournot_shared_risk import FIXED

print(f"Baseline consumption: {FIXED.c0}")
print(f"Hazard intensity: {FIXED.delta}")
print(f"Risk aversion: {FIXED.gamma}")
```

---

### `TreatmentArm`

Defines a randomized treatment condition.

```python
@dataclass(frozen=True)
class TreatmentArm:
    label: str                        # Human-readable name
    kappa: float                      # Hazard curvature parameter
    omega: Tuple[float, float]        # Player hazard weights (ω₁, ω₂)
    g: Tuple[float, float]            # Player growth rates (g₁, g₂)
    description: str = ""             # Optional description
```

#### Methods

##### `as_dict() -> dict`

Convert to dictionary for JSON serialization.

#### Example

```python
arm = TreatmentArm(
    label="High curvature",
    kappa=0.6,
    omega=(1.0, 1.0),
    g=(0.10, 0.10),
    description="Sharper global risk response"
)

print(arm.label)        # "High curvature"
print(arm.kappa)        # 0.6
print(arm.omega)        # (1.0, 1.0)
```

---

## Default Treatments

```python
TREATMENTS: Sequence[TreatmentArm] = (
    TreatmentArm(
        label="Low curvature",
        kappa=0.1,
        omega=(1.0, 1.0),
        g=(0.10, 0.10),
        description="Benchmark hazard curvature with symmetric weights",
    ),
    TreatmentArm(
        label="High curvature",
        kappa=0.6,
        omega=(1.0, 1.0),
        g=(0.10, 0.10),
        description="Sharper global risk response to aggregate runtime",
    ),
    TreatmentArm(
        label="Asymmetric influence",
        kappa=0.3,
        omega=(1.0, 1.5),
        g=(0.10, 0.11),
        description="Player 2 translates runtime into hazard more strongly",
    ),
)
```

### Treatment Parameters Explained

| Parameter | Symbol | Role |
|-----------|--------|------|
| `kappa` | κ | Hazard curvature: higher κ = steeper marginal hazard |
| `omega` | (ω₁, ω₂) | Player weights in aggregate risk |
| `g` | (g₁, g₂) | Per-player growth rates from runtime |

---

## Core Functions

### `hazard_components`

Compute aggregate risk quantity Q and marginal hazard H'(Q).

```python
def hazard_components(
    T1: float, 
    T2: float, 
    arm: TreatmentArm
) -> Tuple[float, float]
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `T1` | `float` | Player 1's runtime choice |
| `T2` | `float` | Player 2's runtime choice |
| `arm` | `TreatmentArm` | Current treatment arm |

#### Returns

`Tuple[float, float]` — (Q, H'(Q))

Where:
- $Q = \omega_1 T_1 + \omega_2 T_2$
- $H'(Q) = 1 + \kappa Q$

#### Example

```python
from otree.cournot_shared_risk import hazard_components, TREATMENTS

arm = TREATMENTS[0]  # Low curvature
Q, Hprime = hazard_components(T1=5.0, T2=3.0, arm=arm)
print(f"Aggregate Q = {Q:.2f}")
print(f"Marginal hazard H'(Q) = {Hprime:.4f}")
```

---

### `survival_probability`

Compute joint survival probability S(T₁, T₂).

```python
def survival_probability(
    T1: float, 
    T2: float, 
    arm: TreatmentArm
) -> float
```

$$S(T_1, T_2) = \exp\left[-\delta \cdot H(Q)\right]$$

Where:
$$H(Q) = Q + \frac{\kappa}{2} Q^2$$

#### Example

```python
from otree.cournot_shared_risk import survival_probability, TREATMENTS

arm = TREATMENTS[1]  # High curvature
S = survival_probability(T1=5.0, T2=5.0, arm=arm)
print(f"Survival probability: {S:.2%}")
```

---

### `consumption`

Compute consumption level from runtime and growth.

```python
def consumption(runtime: float, growth_rate: float) -> float
```

$$c_i(T_i) = c_0 \cdot e^{g_i T_i}$$

#### Example

```python
from otree.cournot_shared_risk import consumption

c = consumption(runtime=10.0, growth_rate=0.10)
print(f"Consumption after 10 years: {c:.2f}")
# Output: Consumption after 10 years: 2.72
```

---

### `crra_utility`

Compute CRRA utility of consumption.

```python
def crra_utility(consumption_level: float) -> float
```

$$u(c) = \begin{cases}
\frac{c^{1-\gamma}}{1-\gamma} & \gamma \neq 1 \\
\ln(c) & \gamma = 1
\end{cases}$$

> **Note:** This simplified version omits the level shift ū for in-game calculations. The full formula with ū is in `formal_model.jones_models.Utility`.

---

### `payoff`

Compute complete payoff structure for a player.

```python
def payoff(
    runtime: float, 
    partner_runtime: float, 
    player_idx: int, 
    arm: TreatmentArm
) -> dict
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `runtime` | `float` | This player's runtime choice |
| `partner_runtime` | `float` | Partner's runtime choice |
| `player_idx` | `int` | Player index (0 or 1) |
| `arm` | `TreatmentArm` | Treatment arm |

#### Returns

```python
{
    "survival": float,          # S(T₁, T₂)
    "consumption": float,       # cᵢ(Tᵢ)
    "expected_utility": float,  # S × u(c)
}
```

#### Example

```python
from otree.cournot_shared_risk import payoff, TREATMENTS

result = payoff(
    runtime=5.0,
    partner_runtime=3.0,
    player_idx=0,
    arm=TREATMENTS[0]
)

print(f"Survival: {result['survival']:.2%}")
print(f"Consumption: {result['consumption']:.4f}")
print(f"Expected utility: {result['expected_utility']:.4f}")
```

---

### `tokenise`

Convert expected utility to token payout.

```python
def tokenise(expected_utility: float, min_utility: float) -> float
```

$$\text{tokens} = \text{token\_floor} + \text{token\_scale} \times \max(U - U_{\min}, 0)$$

This ensures:
- Non-negative payouts
- Incentive compatibility with the underlying utility model
- Scalable lab payments

---

## Matching Functions

### `build_round_robin_schedule`

Generate unique pair schedule for all rounds.

```python
def build_round_robin_schedule(
    players: Sequence[Player], 
    rng: random.Random
) -> List[List[Tuple[int, int]]]
```

Returns a list of rounds, where each round contains tuples of (player1_id, player2_id).

**Constraints:**
- Requires even number of players
- Maximum rounds = N - 1 for N players
- Each pair meets exactly once

---

### `draw_scenario_for_groups`

Randomly assign treatment arms to groups.

```python
def draw_scenario_for_groups(
    num_groups: int, 
    rng: random.Random
) -> Tuple[TreatmentArm, ...]
```

---

## oTree Components

### Constants

```python
class Constants(BaseConstants):
    name_in_url = "cournot_shared_risk"
    players_per_group = 2
    num_rounds = 6  # DEFAULT_NUM_ROUNDS
```

### Player Fields

| Field | Type | Description |
|-------|------|-------------|
| `runtime_choice` | `FloatField` | Player's runtime decision |
| `survival` | `FloatField` | Computed survival probability |
| `consumption` | `FloatField` | Final consumption level |
| `expected_utility` | `FloatField` | Expected utility value |
| `payoff` | `CurrencyField` | Token payout |

### Group Fields

| Field | Type | Description |
|-------|------|-------------|
| `treatment_label` | `StringField` | Name of assigned treatment |
| `kappa` | `FloatField` | Hazard curvature parameter |
| `omega1`, `omega2` | `FloatField` | Player hazard weights |
| `g1`, `g2` | `FloatField` | Player growth rates |

---

## Session Configuration

```python
# In settings.py
SESSION_CONFIGS = [
    dict(
        name='cournot_shared_risk_lab',
        display_name='Cournot Shared-Risk (6 rounds)',
        num_demo_participants=6,
        app_sequence=['cournot_shared_risk'],
        random_seed=42,  # For reproducibility
    ),
]
```

### Configuration Options

| Key | Type | Description |
|-----|------|-------------|
| `num_demo_participants` | `int` | Must be even |
| `random_seed` | `int` | Seed for randomization |
| `app_sequence` | `list` | Include `'survey'` for post-experiment |

---

## See Also

- [Cournot Shared Risk Docs](../../otree/cournot_shared_risk/docs/README.md) — App documentation
- [Shared Risk Model](../../formal_model/cournot-risk-extension/Shared-Risk-Model.md) — Theory
- [Experiment Guide](../experiments/cournot-experiment.md) — Running sessions
