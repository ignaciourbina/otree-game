# oTree Experiments

This directory contains the oTree experiment applications for the AI Growth-Risk project.

## Running the Server

```bash
cd otree
otree devserver
# Open http://localhost:8000
```

## Available Apps

| App | Description | Group Size |
|-----|-------------|------------|
| `cournot_shared_risk` | Two-player strategic AI deployment game based on Cournot extension of Jones (2023) | 2 |
| `ai_growth_risk` | Single-player AI growth-risk tradeoff experiment | 1-2 |
| `ai_growth_risk_bot` | Bot testing harness for ai_growth_risk | 2 |
| `public_goods` | Classic public goods contribution game | N |
| `survey` | Post-experiment questionnaire | 1 |

## Key Files

- `settings.py` — Session configurations and app registration
- `_static/` — Shared static assets (CSS, JS, images)
- Each app folder contains:
  - `__init__.py` — Models, constants, and game logic
  - `pages.py` — Page classes (if separated from models)
  - `templates/` — HTML templates
  - `tests.py` — App-specific tests

## Session Configuration

Edit `settings.py` to add or modify session configurations:

```python
SESSION_CONFIGS = [
    dict(
        name='cournot_shared_risk_lab',
        display_name='Cournot Shared-Risk (6 rounds)',
        num_demo_participants=6,
        app_sequence=['cournot_shared_risk'],
    ),
]
```

## Documentation

See [`docs/experiments/`](../docs/experiments/README.md) for detailed guides on running experiments.
