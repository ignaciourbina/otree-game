# Architecture Overview

This document describes the high-level architecture of the oTree AI Growth-Risk Experiments project.

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         oTree AI Growth-Risk                            │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────┐  │
│  │  Formal Models  │◄───│   Simulations   │    │   oTree Platform    │  │
│  │  (Python)       │    │   Runner        │    │   (Web Framework)   │  │
│  └────────┬────────┘    └─────────────────┘    └──────────┬──────────┘  │
│           │                                               │             │
│           │              ┌────────────────┐               │             │
│           └─────────────►│  Experiment    │◄──────────────┘             │
│                          │  Applications  │                             │
│                          └────────────────┘                             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Formal Models Layer (`formal_model/`)

The theoretical foundation implementing Jones (2023) AI growth-risk models.

```
formal_model/
├── jones_models.py          # Core model implementations
├── USAGE.md                  # Usage documentation
└── cournot-risk-extension/   # Multi-player extension
    ├── Shared-Risk-Model.md  # Theory documentation
    ├── validate_shared_risk.py
    └── generate_shared_risk_tex.py
```

**Key Classes:**

| Class | Description | Reference |
|-------|-------------|-----------|
| `SimpleAIGrowthRiskModel` | Section 2 "run AI for T years" model | Jones (2023) §2 |
| `DynamicAIGrowthRiskModel` | Section 3 dynamic adoption model | Jones (2023) §3 |
| `Utility` | CRRA utility with level shift | Supporting class |

**Dependencies:** NumPy (required), Matplotlib (optional for plots)

### 2. oTree Experiment Layer (`otree/`)

Interactive web-based experiments built on the oTree framework.

```
otree/
├── settings.py               # Session configurations
├── ai_growth_risk/           # Single-player growth-risk experiment
│   ├── __init__.py           # Models and game logic
│   ├── pages.py              # Page sequence
│   └── templates/            # HTML templates
├── cournot_shared_risk/      # Two-player strategic experiment
│   ├── __init__.py           # Models and Cournot logic
│   └── templates/            # HTML templates
├── public_goods/             # Classic public goods game
└── survey/                   # Post-experiment questionnaire
```

**Application Flow:**

```
Introduction ──► Decision ──► WaitPage ──► Results
     │               │            │           │
     ▼               ▼            ▼           ▼
 Consent &     Player submits  Sync groups  Display
 instructions  runtime choice  & compute    payoffs
                               payoffs
```

### 3. Simulations Layer (`simulations/`)

Batch experiments and comparative statics analysis.

```
simulations/
├── __init__.py
└── runner.py     # CLI runner for parameter sweeps
```

**Outputs:** CSV datasets and PNG visualizations in `out/simulations/`

### 4. Testing Infrastructure (`testing/`)

Automated stress testing using oTree's bot framework.

```
testing/
├── run_ai_growth_risk_bots.py   # Bot runner harness
├── scenarios_snapshot.json       # Reference scenarios
├── settings_bots.py              # Test configuration
└── workflows/                    # CI/CD recipes
    ├── github-actions.yml
    └── run_local.sh
```

## Data Flow

### Experiment Session Flow

```
┌──────────────┐     ┌─────────────┐     ┌────────────────┐
│ Researcher   │────►│  oTree      │────►│  Participant   │
│ Admin Panel  │     │  Server     │     │  Browser       │
└──────────────┘     └──────┬──────┘     └────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Database    │
                     │  (SQLite)    │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  CSV Export  │
                     └──────────────┘
```

### Model Computation Flow

```
Treatment Parameters ──► Formal Model Formulas ──► Expected Utility
         │                        │                       │
         ▼                        ▼                       ▼
    (g, δ, γ, ω, κ)    ───►  c*(T), S(T)  ───►   W = S·u(c)
                                                      │
                                                      ▼
                                               Token Payoff
```

## Key Design Decisions

### 1. Separation of Theory and Implementation

The formal model layer (`formal_model/`) is intentionally decoupled from oTree:
- Enables standalone computational experiments
- Facilitates unit testing of economic formulas
- Allows reuse in notebooks, simulations, or other platforms

### 2. Treatment Parameterization

Experiments use pre-defined treatment arms rather than exposing raw model parameters:
- Simplifies participant decision interface
- Ensures incentive compatibility
- Facilitates between-subjects design

### 3. Unique Pair Matching (Cournot Game)

The `cournot_shared_risk` app implements round-robin scheduling:
- Each pair meets at most once across all rounds
- Eliminates reputation/learning confounds
- Requires even participant count and `rounds ≤ N-1`

### 4. Token-Based Incentives

Expected utility is mapped to tokens via affine transformation:
```python
tokens = token_floor + token_scale × (expected_utility - min_utility)
```
This ensures:
- Non-negative payments
- Incentive compatibility with underlying welfare model
- Scalable lab payouts

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Backend | Python 3.8+ | Core language |
| Framework | oTree 5.x | Experiment platform |
| Web Server | Flask/ASGI | HTTP handling |
| Database | SQLite | Session data storage |
| Math | NumPy, SciPy | Numerical computation |
| Symbolics | SymPy | Equation validation |
| Visualization | Matplotlib | Plot generation |
| Testing | oTree Bots | Automated testing |

## File Organization

```
otree-game/
├── README.md                 # Project overview
├── MODEL_PRIMITIVES.md       # Core model equations
├── requirements.txt          # Python dependencies
├── docs/                     # 📚 Documentation (this folder)
├── formal_model/             # 🧮 Theoretical models
├── otree/                    # 🎮 oTree experiments
├── simulations/              # 📊 Batch simulations
├── testing/                  # 🧪 Test infrastructure
├── _static/                  # Static assets (global)
└── out/                      # Generated outputs (gitignored)
```

## Next Steps

- **[Getting Started →](../getting-started/README.md)** - Set up your environment
- **[API Reference →](../api/README.md)** - Detailed module documentation
- **[Experiment Guides →](../experiments/README.md)** - Run experiments
