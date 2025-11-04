# Formal Model Usage

This directory contains a drop-in Python module that implements the two
formal models presented in Jones (2023) for studying AI-driven growth and
existential risk. The code is self-contained, depends only on NumPy and
Matplotlib for the plotting examples, and can be imported into scripts,
notebooks, or interactive Python sessions.

## Installation

From the project root, install the optional dependencies used in the example
plots:

```bash
pip install -r requirements.txt
```

(NumPy is required for parameter sweeps; Matplotlib is only needed if you plan
on reproducing the demonstration plots.)

## Quick start

```python
from formal_model.jones_models import (
    SimpleAIGrowthRiskModel,
    DynamicAIGrowthRiskModel,
)

# Section 2 model: optimal runtime and extinction probability
simple = SimpleAIGrowthRiskModel(gamma=2.0, g=0.10, delta_=0.01)
print(simple.summary())

# Section 3 model: acceptable one-time risk given growth and mortality shifts
dyn = DynamicAIGrowthRiskModel(gamma=2.0)
print(dyn.delta_star(g_ai=0.08, m_ai=0.01))
```

## Reproducing the comparative statics from the paper

```python
import matplotlib.pyplot as plt
import numpy as np
from formal_model.jones_models import SimpleAIGrowthRiskModel

model = SimpleAIGrowthRiskModel(gamma=2.0, g=0.10, delta_=0.01)
deltas = np.linspace(0.005, 0.03, 40)
results = model.comparative_statics_over_delta(deltas.tolist())

plt.plot([r["delta"] for r in results],
         [r["extinction_prob"] for r in results])
plt.xlabel("flow existential risk δ")
plt.ylabel("overall extinction probability 1 - e^{-δ T*}")
plt.show()
```

```python
import matplotlib.pyplot as plt
import numpy as np
from formal_model.jones_models import DynamicAIGrowthRiskModel

dyn = DynamicAIGrowthRiskModel(gamma=2.0)
g_vals = np.linspace(0.03, 0.15, 50)  # AI gives 3% to 15% growth
res = dyn.sweep_growth(g_vals.tolist(), m_ai=0.01)

plt.plot([r["g_ai"] for r in res],
         [r["delta_star"] for r in res])
plt.axhline(0, color="black")
plt.xlabel("AI growth g_ai")
plt.ylabel("max acceptable one-time existential risk δ*")
plt.show()
```

## Notes

* The helper :func:`calibrate_ubar_from_v` allows you to reproduce the VSL
  calibration step Jones uses.
* The classes mutate their internal parameters during comparative statics
  sweeps (matching the provided skeleton). If you need to preserve the
  original parameterization, instantiate a fresh model before each sweep or
  store the original values.
* The module exports an ``__all__`` list so that ``from formal_model.jones_models
  import *`` only brings the intended helpers into scope.
