#!/usr/bin/env bash
set -euo pipefail

# Example shell wrapper that runs a moderate bot stress test locally.

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/../.. && pwd)"

python "${PROJECT_ROOT}/testing/run_ai_growth_risk_bots.py" \
  --iterations "${ITERATIONS:-10}" \
  --participants "${PARTICIPANTS:-20}" \
  --random-seed-base "${SEED_BASE:-1000}" \
  --export-dir "${PROJECT_ROOT}/testing/output"
