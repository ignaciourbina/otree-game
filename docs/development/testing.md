# Testing Guide

This guide covers how to run existing tests and write new tests for the oTree AI Growth-Risk Experiments project.

## Test Organization

```
testing/
├── run_ai_growth_risk_bots.py   # oTree bot runner
├── scenarios_snapshot.json       # Test fixture data
├── settings_bots.py              # Test session config
└── workflows/
    ├── github-actions.yml        # CI configuration
    └── run_local.sh              # Local test script
```

## Running Tests

### Quick Test

```bash
# From project root
python testing/run_ai_growth_risk_bots.py --iterations 2
```

### Full Test Suite

```bash
# Run all bot iterations
python testing/run_ai_growth_risk_bots.py \
    --iterations 10 \
    --participants 6 \
    --export-dir testing/output
```

### Specific Components

```bash
# Test formal model only
python -c "from formal_model.jones_models import SimpleAIGrowthRiskModel; m = SimpleAIGrowthRiskModel(); print(m.summary())"

# Test oTree server startup
cd otree && otree devserver --check
```

## Bot Test Runner

### Usage

```bash
python testing/run_ai_growth_risk_bots.py [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--settings-module` | `str` | `testing.settings_bots` | oTree settings module |
| `--session-config` | `str` | `ai_growth_risk_bot` | Session config name |
| `--participants` | `int` | `2` | Participants per session |
| `--iterations` | `int` | `5` | Number of test runs |
| `--random-seed-base` | `int` | None | Base seed for reproducibility |
| `--export-dir` | `Path` | None | CSV output directory |
| `--verbosity` | `str` | `info` | Log level |

### Example Output

```
INFO - Running iteration 1/5...
INFO - Session created with config: ai_growth_risk_bot
INFO - Running bots...
INFO - Session completed successfully
INFO - Running iteration 2/5...
...
INFO - All 5 iterations completed successfully
```

## Writing Tests

### Unit Tests for Formal Model

```python
# testing/test_jones_models.py
import pytest
from formal_model.jones_models import (
    SimpleAIGrowthRiskModel,
    calibrate_ubar_from_v,
    Utility,
)

class TestCalibration:
    def test_calibrate_ubar_log_utility(self):
        """Test ubar calibration for gamma=1 (log utility)."""
        ubar = calibrate_ubar_from_v(c0=1.0, gamma=1.0, target_v=6.0)
        assert ubar == 6.0  # log(1) = 0
    
    def test_calibrate_ubar_crra(self):
        """Test ubar calibration for gamma=2."""
        ubar = calibrate_ubar_from_v(c0=1.0, gamma=2.0, target_v=6.0)
        assert abs(ubar - 7.0) < 0.001

class TestSimpleModel:
    def test_optimal_runtime_positive(self):
        """Optimal runtime should be positive."""
        model = SimpleAIGrowthRiskModel(g=0.10, delta_=0.01)
        assert model.T_star() > 0
    
    def test_extinction_prob_bounded(self):
        """Extinction probability should be in [0, 1]."""
        model = SimpleAIGrowthRiskModel()
        prob = model.total_extinction_prob()
        assert 0 <= prob <= 1
    
    def test_higher_delta_lower_runtime(self):
        """Higher hazard should reduce optimal runtime."""
        model_low = SimpleAIGrowthRiskModel(delta_=0.01)
        model_high = SimpleAIGrowthRiskModel(delta_=0.05)
        assert model_high.T_star() < model_low.T_star()

class TestComparativeStatics:
    def test_delta_sweep_monotonic(self):
        """Extinction probability should increase with delta."""
        model = SimpleAIGrowthRiskModel()
        results = model.comparative_statics_over_delta([0.01, 0.02, 0.03])
        probs = [r["extinction_prob"] for r in results]
        assert probs == sorted(probs)  # Should be monotonically increasing
```

### Run Unit Tests

```bash
python -m pytest testing/test_jones_models.py -v
```

### oTree App Tests

oTree uses bots for automated testing. Bot classes go in each app's `tests.py`:

```python
# otree/cournot_shared_risk/tests.py
from otree.api import Bot, Submission
import random

class PlayerBot(Bot):
    def play_round(self):
        # Introduction page
        yield Submission(
            pages.Introduction,
            check_html=False,
        )
        
        # Decision page
        yield Submission(
            pages.Decision,
            dict(runtime_choice=random.uniform(1, 10)),
            check_html=False,
        )
        
        # Results page (no submission needed)
        pass
```

### Test Fixtures

```python
# testing/fixtures.py
import pytest
from formal_model.jones_models import SimpleAIGrowthRiskModel

@pytest.fixture
def default_model():
    """Provide a model with default parameters."""
    return SimpleAIGrowthRiskModel()

@pytest.fixture
def high_risk_model():
    """Provide a high-risk scenario."""
    return SimpleAIGrowthRiskModel(delta_=0.05)

# Usage in tests
def test_something(default_model):
    assert default_model.T_star() > 0
```

## Continuous Integration

### GitHub Actions

```yaml
# testing/workflows/github-actions.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run unit tests
        run: python -m pytest testing/ -v
      
      - name: Run bot tests
        run: python testing/run_ai_growth_risk_bots.py --iterations 3
```

### Local CI Simulation

```bash
# testing/workflows/run_local.sh
#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running unit tests..."
python -m pytest testing/ -v

echo "Running bot tests..."
python testing/run_ai_growth_risk_bots.py --iterations 3

echo "All tests passed!"
```

## Test Coverage

### Generate Coverage Report

```bash
pip install pytest-cov
python -m pytest testing/ --cov=formal_model --cov-report=html
open htmlcov/index.html  # View report
```

### Coverage Goals

| Module | Target |
|--------|--------|
| `formal_model.jones_models` | 90% |
| `otree.cournot_shared_risk` | 80% |
| `simulations.runner` | 70% |

## Debugging Tests

### Verbose Output

```bash
python -m pytest testing/ -v --tb=long
```

### Drop into Debugger

```bash
python -m pytest testing/ --pdb
```

### Print Statements

```python
def test_something():
    model = SimpleAIGrowthRiskModel()
    result = model.T_star()
    print(f"DEBUG: T* = {result}")  # Will show with -s flag
    assert result > 0
```

```bash
python -m pytest testing/ -v -s  # Show print output
```

## Test Data

### Snapshot Testing

The `scenarios_snapshot.json` file contains reference data:

```json
{
    "treatments": [
        {
            "label": "Low curvature",
            "kappa": 0.1,
            "expected_equilibrium_T": 8.5
        }
    ],
    "benchmarks": {
        "simple_model_baseline": {
            "T_star": 45.2,
            "extinction_prob": 0.36
        }
    }
}
```

### Updating Snapshots

```bash
# Generate new snapshot
python -c "
import json
from formal_model.jones_models import SimpleAIGrowthRiskModel

model = SimpleAIGrowthRiskModel()
snapshot = {'T_star': model.T_star(), 'extinction_prob': model.total_extinction_prob()}
print(json.dumps(snapshot, indent=2))
" > testing/snapshots/baseline.json
```

## Performance Testing

### Timing Tests

```python
import time

def test_comparative_statics_performance():
    """Comparative statics should complete in reasonable time."""
    model = SimpleAIGrowthRiskModel()
    deltas = [i * 0.001 for i in range(1, 100)]
    
    start = time.time()
    results = model.comparative_statics_over_delta(deltas)
    elapsed = time.time() - start
    
    assert elapsed < 1.0  # Should complete in under 1 second
    assert len(results) == 99
```

## Best Practices

### Do

- ✅ Test edge cases (γ=1, δ=0, etc.)
- ✅ Use descriptive test names
- ✅ Test both success and failure cases
- ✅ Keep tests independent
- ✅ Use fixtures for shared setup

### Don't

- ❌ Test implementation details
- ❌ Have tests depend on each other
- ❌ Use random values without seeding
- ❌ Skip tests without good reason

## See Also

- [Development Setup →](./setup.md) — Configure environment
- [Contributing →](./contributing.md) — Submit tests with PRs
- [CI/CD Workflows →](../../testing/workflows/) — Automation recipes
