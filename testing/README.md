# AI Growth Risk Experiment Stress Tests

This directory bundles lightweight tooling to exercise the `ai_growth_risk`
experiment with oTree's bot framework. Use these helpers before launching lab
sessions to verify that the randomised scenarios, runtime menu, and incentive
mapping behave as expected under automated play.

## Contents

- `run_ai_growth_risk_bots.py` – command line harness that spins up repeated
oTree sessions, runs the bundled bots, and optionally exports CSV logs for each
run.
- `scenarios_snapshot.json` – quick reference dump of the currently coded
runtime menus and benchmark statistics that the bots consume.
- `workflows/` – sample automation recipes (shell and GitHub Actions) that wire
this harness into CI or ad-hoc stress campaigns.

## Quick start

```bash
# Activate your virtual environment first.
python testing/run_ai_growth_risk_bots.py --iterations 5 --participants 24 --export-dir testing/output
```

The harness targets the lightweight `testing.settings_bots` configuration,
which mirrors the production app via the `ai_growth_risk_bot` alias while
keeping app names CLI-friendly. Override `--settings-module` if you need to
exercise an alternative settings file. The script rotates the scenario random
seed across iterations unless you pin `--random-seed-base`.

Review the generated CSVs (if exporting) and the JSON snapshot to confirm that
runtime averages, survival probabilities, and incentives align with the
intended treatment catalogue.
