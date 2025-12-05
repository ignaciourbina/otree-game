# oTree AI Growth-Risk Experiments

This repository implements laboratory experiments based on [Jones (2023) "The A.I. Dilemma: Growth versus Existential Risk"](https://web.stanford.edu/~chadj/AIdilemma.pdf). It contains:

- **Formal economic models** implementing Jones (2023) in Python
- **oTree experiments** for lab-based behavioral research
- **Simulations** for computational parameter exploration
- **Testing infrastructure** for automated validation

## Quick Start

```bash
# Clone and setup
git clone https://github.com/ignaciourbina/otree-game.git
cd otree-game
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the oTree server
cd otree
otree devserver

# Open http://localhost:8000 in your browser
```

## Project Structure

```
otree-game/
├── formal_model/         # Jones (2023) model implementations
│   ├── jones_models.py   # Core SimpleAI and DynamicAI models
│   └── cournot-risk-extension/  # Two-player strategic extension
├── otree/                # oTree experiment applications
│   ├── cournot_shared_risk/  # Two-player Cournot game
│   ├── ai_growth_risk/       # Single-player growth-risk tradeoff
│   ├── public_goods/         # Classic public goods game
│   └── survey/               # Post-experiment questionnaire
├── simulations/          # Batch simulation runner
├── testing/              # Automated bot testing
└── docs/                 # Full documentation
```

## Available Experiments

| App | Description | Players |
|-----|-------------|---------|
| `cournot_shared_risk` | Strategic AI deployment with shared global risk | 2 per group |
| `ai_growth_risk` | Single-player growth-risk tradeoff | 1-2 per group |
| `public_goods` | Classic public goods contribution | N per group |
| `survey` | Post-experiment questionnaire | 1 |

## Documentation

See the [`docs/`](./docs/README.md) folder for comprehensive documentation:

- [Getting Started](./docs/getting-started/README.md) — Installation and quickstart
- [Architecture](./docs/architecture/README.md) — System design and data flow
- [API Reference](./docs/api/README.md) — Module documentation
- [Experiments](./docs/experiments/README.md) — Running lab sessions
- [Development](./docs/development/README.md) — Contributing and testing

## Key References

- Jones, C. I. (2023). *The A.I. Dilemma: Growth versus Existential Risk*. NBER Working Paper.
- [MODEL_PRIMITIVES.md](./MODEL_PRIMITIVES.md) — Core equations and notation
- [Shared-Risk-Model.md](./formal_model/cournot-risk-extension/Shared-Risk-Model.md) — Two-player extension

## License

Research use. See repository for details.
