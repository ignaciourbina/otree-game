# API Reference

This section provides detailed documentation for all modules in the oTree AI Growth-Risk Experiments project.

## Module Index

| Module | Description | Documentation |
|--------|-------------|---------------|
| `formal_model.jones_models` | Jones (2023) model implementations | [API Reference →](./formal-model.md) |
| `otree.cournot_shared_risk` | Two-player strategic experiment | [API Reference →](./cournot-shared-risk.md) |
| `otree.ai_growth_risk` | Single-player growth-risk experiment | [API Reference →](./ai-growth-risk.md) |
| `simulations.runner` | Batch simulation runner | [API Reference →](./simulations.md) |

## Quick Reference

### Formal Model Classes

```python
from formal_model.jones_models import (
    SimpleAIGrowthRiskModel,   # Section 2: optimal runtime
    DynamicAIGrowthRiskModel,  # Section 3: adoption decision
    Utility,                    # CRRA utility functions
    calibrate_ubar_from_v,     # VSL calibration helper
)
```

### oTree App Components

```python
# Cournot Shared Risk
from otree.cournot_shared_risk import (
    FIXED,                     # Fixed primitives (c0, delta, gamma)
    TREATMENTS,                # Treatment arm definitions
    survival_probability,      # S(T1, T2) computation
    payoff,                    # Full payoff calculation
)
```

## Import Patterns

### Standalone Analysis

```python
# For computational experiments without oTree
from formal_model.jones_models import SimpleAIGrowthRiskModel

model = SimpleAIGrowthRiskModel(gamma=2.0, g=0.10, delta_=0.01)
print(model.summary())
```

### With NumPy for Parameter Sweeps

```python
import numpy as np
from formal_model.jones_models import SimpleAIGrowthRiskModel

model = SimpleAIGrowthRiskModel()
deltas = np.linspace(0.005, 0.05, 20).tolist()
results = model.comparative_statics_over_delta(deltas)
```

### Visualization

```python
import matplotlib.pyplot as plt
from formal_model.jones_models import SimpleAIGrowthRiskModel

model = SimpleAIGrowthRiskModel()
results = model.comparative_statics_over_delta([0.01, 0.02, 0.03])

plt.plot([r["delta"] for r in results], 
         [r["extinction_prob"] for r in results])
plt.show()
```

## Type Annotations

All modules use Python type hints for better IDE support:

```python
def calibrate_ubar_from_v(
    c0: float, 
    gamma: float, 
    target_v: float = 6.0
) -> float:
    ...
```

## Error Handling

Common exceptions and how to handle them:

| Exception | Cause | Solution |
|-----------|-------|----------|
| `ValueError` | Invalid parameter combination | Check parameter constraints |
| `ZeroDivisionError` | γ = 1 edge case | Use log utility branch |
| `ImportError` | Missing optional dependency | Install matplotlib/numpy |

## See Also

- [Theory Documentation](../theory/README.md) - Mathematical foundations
- [Architecture Overview](../architecture/README.md) - System design
- [Development Guide](../development/README.md) - Contributing code
