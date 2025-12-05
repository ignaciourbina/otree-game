# Session Configuration Guide

This guide explains how to customize experiment sessions by modifying treatment parameters, session configs, and app settings.

## Configuration Hierarchy

```
settings.py
├── SESSION_CONFIGS         # Session-level settings
├── SESSION_CONFIG_DEFAULTS # Shared defaults
└── App-level constants     # In each app's __init__.py
    ├── FIXED               # Fixed primitives
    └── TREATMENTS          # Treatment arms
```

## Modifying settings.py

### Location

```
otree/settings.py
```

### Session Configs

```python
SESSION_CONFIGS = [
    dict(
        name='cournot_shared_risk_lab',
        display_name='Cournot Shared-Risk (6 rounds)',
        num_demo_participants=6,
        app_sequence=['cournot_shared_risk'],
        random_seed=42,
    ),
    # Add more configs here
]
```

### Config Options

| Key | Type | Description |
|-----|------|-------------|
| `name` | `str` | Internal identifier (no spaces) |
| `display_name` | `str` | Human-readable name |
| `num_demo_participants` | `int` | Demo session size |
| `app_sequence` | `list` | Order of apps |
| `random_seed` | `int` | Randomization seed |
| `participation_fee` | `float` | Fixed show-up payment |
| `real_world_currency_per_point` | `float` | Token → USD conversion |

### Example: Multiple Session Types

```python
SESSION_CONFIGS = [
    # Short lab session
    dict(
        name='cournot_short',
        display_name='Cournot (3 rounds, quick)',
        num_demo_participants=4,
        app_sequence=['cournot_shared_risk', 'survey'],
        random_seed=42,
    ),
    # Full experiment
    dict(
        name='cournot_full',
        display_name='Cournot (6 rounds, full)',
        num_demo_participants=12,
        app_sequence=['cournot_shared_risk', 'survey'],
        random_seed=123,
    ),
    # High-stakes variant
    dict(
        name='cournot_highstakes',
        display_name='Cournot (High Stakes)',
        num_demo_participants=8,
        app_sequence=['cournot_shared_risk'],
        real_world_currency_per_point=0.10,  # 10¢ per point
        participation_fee=5.00,
    ),
]
```

## Modifying Treatment Arms

### Location

```
otree/cournot_shared_risk/__init__.py
```

### Default Treatments

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

### Adding Custom Treatments

```python
TREATMENTS: Sequence[TreatmentArm] = (
    # ... existing treatments ...
    
    # New: Extreme curvature
    TreatmentArm(
        label="Extreme curvature",
        kappa=1.0,
        omega=(1.0, 1.0),
        g=(0.10, 0.10),
        description="Very steep marginal hazard for strategic study",
    ),
    
    # New: Asymmetric growth
    TreatmentArm(
        label="Asymmetric growth",
        kappa=0.3,
        omega=(1.0, 1.0),
        g=(0.08, 0.12),  # Player 2 has higher growth
        description="Testing growth rate heterogeneity",
    ),
    
    # New: One-sided risk
    TreatmentArm(
        label="Dictator risk",
        kappa=0.3,
        omega=(2.0, 0.0),  # Only Player 1 contributes to risk
        g=(0.10, 0.10),
        description="Player 1 determines all shared risk",
    ),
)
```

### Treatment Parameters Explained

| Parameter | Symbol | Range | Effect |
|-----------|--------|-------|--------|
| `kappa` | κ | 0.0 - 1.0+ | Higher = steeper hazard curve |
| `omega` | (ω₁, ω₂) | 0.0+ each | Weight of each player's runtime in aggregate risk |
| `g` | (g₁, g₂) | 0.01 - 0.20 | Growth rate per year of runtime |

## Modifying Fixed Primitives

### Location

```
otree/cournot_shared_risk/__init__.py
```

### Defaults

```python
@dataclass(frozen=True)
class FixedPrimitives:
    c0: float = 1.0           # Baseline consumption
    delta: float = 0.01       # Baseline hazard intensity
    gamma: float = 2.0        # CRRA coefficient
    token_floor: float = 10.0 # Minimum token payout
    token_scale: float = 150.0 # Token conversion factor
```

### Customizing

```python
# For higher-risk scenarios
FIXED = FixedPrimitives(
    delta=0.02,        # Double the hazard
    gamma=3.0,         # More risk-averse participants
    token_scale=200.0, # Larger payoff spread
)

# For lower-stakes testing
FIXED = FixedPrimitives(
    token_floor=5.0,
    token_scale=50.0,
)
```

## Adjusting Round Count

### Location

```
otree/cournot_shared_risk/__init__.py
```

### Setting

```python
DEFAULT_NUM_ROUNDS = 6  # Change this

class Constants(BaseConstants):
    name_in_url = "cournot_shared_risk"
    players_per_group = 2
    num_rounds = DEFAULT_NUM_ROUNDS
```

### Constraints

- Must have `num_rounds ≤ N - 1` for N participants
- Unique pair matching requires even participant count
- Consider fatigue effects for long sessions

## Payment Configuration

### Token to Currency Conversion

```python
SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.05,  # 5¢ per point
    participation_fee=5.00,              # $5 show-up
)
```

### App-Level Token Mapping

In `cournot_shared_risk/__init__.py`:

```python
def tokenise(expected_utility: float, min_utility: float) -> float:
    shifted = max(expected_utility - min_utility, 0)
    return FIXED.token_floor + FIXED.token_scale * shifted
```

Adjust `token_floor` and `token_scale` to calibrate payouts.

## Environment Variables

### For Production

```bash
export OTREE_ADMIN_PASSWORD="secure_password"
export OTREE_AUTH_LEVEL=DEMO  # or STUDY
```

### For Development

```bash
export DEBUG=1
export OTREE_ADMIN_PASSWORD="password"
```

## Validation Checklist

Before running experiments:

- [ ] Verify treatment parameter ranges are sensible
- [ ] Ensure num_rounds ≤ participants - 1
- [ ] Check token payouts produce reasonable payments
- [ ] Test with demo session
- [ ] Confirm random_seed is set (for reproducibility)
- [ ] Review app_sequence includes survey if needed

## Common Configurations

### Standard Lab Experiment

```python
dict(
    name='cournot_standard',
    display_name='Cournot Shared-Risk (Standard)',
    num_demo_participants=10,
    app_sequence=['cournot_shared_risk', 'survey'],
    random_seed=42,
    participation_fee=5.00,
    real_world_currency_per_point=0.05,
)
```

### Online Experiment (MTurk/Prolific)

```python
dict(
    name='cournot_online',
    display_name='Cournot (Online)',
    num_demo_participants=100,
    app_sequence=['cournot_shared_risk', 'survey'],
    random_seed=None,  # Different randomization per session
    participation_fee=2.00,
    real_world_currency_per_point=0.02,
)
```

### Pilot Testing

```python
dict(
    name='cournot_pilot',
    display_name='Cournot (Pilot - 2 rounds)',
    num_demo_participants=4,
    app_sequence=['cournot_shared_risk'],
    random_seed=1,
)
# Also set DEFAULT_NUM_ROUNDS = 2 in app
```

## See Also

- [First Experiment →](./first-experiment.md) — Run the session
- [API Reference →](../api/cournot-shared-risk.md) — Code details
- [Theory →](../theory/cournot-model.md) — Model background
