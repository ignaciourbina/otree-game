# Experiment Guides

This section provides step-by-step guides for running laboratory experiments using the oTree AI Growth-Risk platform.

## Available Guides

| Guide | Description |
|-------|-------------|
| [First Experiment](./first-experiment.md) | Run your first lab session |
| [Session Configuration](./session-config.md) | Customize experiment parameters |
| [Simulations](../api/simulations.md) | Batch simulation runner API |

## Experiment Overview

### Available Apps

| App | Players | Description |
|-----|---------|-------------|
| `cournot_shared_risk` | 2 per group | Strategic AI deployment with shared global risk |
| `ai_growth_risk` | 2 per group | Single-player growth-risk tradeoff |
| `public_goods` | N | Classic public goods contribution game |
| `survey` | 1 | Post-experiment questionnaire |

### Typical Session Flow

```
1. Pre-Session Setup
   └── Configure treatments, participant count, randomization

2. Session Launch
   └── Generate participant links, brief participants

3. Experiment Rounds
   └── Introduction → Decision → Results (repeat per round)

4. Post-Experiment
   └── Survey → Debrief → Payment

5. Data Collection
   └── Export CSV → Analysis
```

## Quick Start: Cournot Shared Risk

```bash
# Start the server
cd otree
otree devserver

# Open http://localhost:8000/demo
# Select "Cournot Shared-Risk (6 rounds)"
# Create session and share participant links
```

## Experiment Design Considerations

### Between-Subjects Design

Treatment assignment is randomized at the group level:
- Each group receives one treatment arm per round
- Round-robin matching ensures unique pairs
- `random_seed` in config enables reproducibility

### Within-Subjects Design

Multiple rounds allow within-subject analysis:
- Each participant experiences multiple treatment conditions
- Learning effects can be measured
- Requires careful counterbalancing

### Sample Size Requirements

| Design | Minimum N | Recommended N |
|--------|-----------|---------------|
| Cournot (6 rounds) | 6 | 20+ |
| Single-player | 30 | 100+ |
| Public goods (N=4) | 16 | 40+ |

## Pre-Registration

For publication-quality experiments, consider:
- Pre-registering hypotheses on OSF or AsPredicted
- Documenting exact treatment parameters
- Specifying primary and secondary outcomes
- Planning power analysis

## Next Steps

- **[First Experiment →](./first-experiment.md)** — Detailed walkthrough
- **[Session Configuration →](./session-config.md)** — Customize treatments
