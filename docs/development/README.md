# Development Guide

This section covers development setup, contribution guidelines, and testing procedures for the oTree AI Growth-Risk Experiments project.

## Quick Links

| Guide | Description |
|-------|-------------|
| [Development Setup](./setup.md) | Configure your development environment |
| [Contributing](./contributing.md) | Contribution workflow and guidelines |
| [Testing](./testing.md) | Run and write tests |

## Development Workflow

```
1. Fork & Clone
   └── git clone https://github.com/YOUR_USERNAME/otree-game.git

2. Create Branch
   └── git checkout -b feature/your-feature

3. Make Changes
   └── Edit code, write tests

4. Test
   └── python testing/run_ai_growth_risk_bots.py

5. Commit
   └── git commit -m "feat: add new feature"

6. Push & PR
   └── git push origin feature/your-feature
   └── Open Pull Request
```

## Project Structure

```
otree-game/
├── docs/                 # 📚 Documentation (you are here)
├── formal_model/         # 🧮 Economic theory implementation
│   ├── jones_models.py   #    Core model classes
│   └── cournot-risk-extension/
├── otree/                # 🎮 oTree experiment apps
│   ├── settings.py       #    Session configuration
│   ├── ai_growth_risk/   #    Single-player app
│   ├── cournot_shared_risk/  # Two-player app
│   ├── public_goods/     #    Classic game
│   └── survey/           #    Questionnaire
├── simulations/          # 📊 Batch experiment runner
├── testing/              # 🧪 Test infrastructure
└── requirements.txt      # Python dependencies
```

## Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Language | Python | 3.8+ |
| Framework | oTree | 5.x |
| Math | NumPy | 1.20+ |
| Visualization | Matplotlib | 3.0+ |
| Symbolics | SymPy | 1.9+ |
| Data | Pandas | 1.0+ |

## Key Concepts

### Formal Models

The `formal_model` package contains pure Python implementations of Jones (2023):

- **No oTree dependencies**: Can be used standalone
- **Dataclass-based**: Clean, immutable parameter objects
- **Type-annotated**: Full IDE support
- **Testable**: Unit testable without web server

### oTree Apps

Each app in `otree/` follows oTree conventions:

- `__init__.py`: Models, game logic, constants
- `pages.py`: Page classes and form handling (if separate)
- `templates/`: HTML templates with Django templating
- `tests.py`: App-specific tests

### Treatment Design

Experiments use a treatment arm pattern:

```python
@dataclass(frozen=True)
class TreatmentArm:
    label: str
    kappa: float
    omega: Tuple[float, float]
    g: Tuple[float, float]
```

This enables:
- Type-safe treatment definitions
- Easy serialization for analysis
- Clear documentation of experimental conditions

## Common Tasks

### Add a New Treatment

1. Edit `otree/cournot_shared_risk/__init__.py`
2. Add entry to `TREATMENTS` tuple
3. Test with demo session

### Modify Model Parameters

1. Edit `formal_model/jones_models.py`
2. Update affected oTree apps
3. Run simulations to verify

### Add New Analysis

1. Create script in `simulations/`
2. Use existing model classes
3. Output to `out/` directory

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/ignaciourbina/otree-game/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ignaciourbina/otree-game/discussions)
- **oTree Docs**: [oTree Documentation](https://otree.readthedocs.io/)

## Next Steps

- **[Development Setup →](./setup.md)** — Get your environment ready
- **[Contributing →](./contributing.md)** — Submit your first PR
- **[Testing →](./testing.md)** — Verify your changes
