# Cournot Shared-Risk oTree App

This scaffold sketches how to port the Cournot-style shared-risk extension of Jones (2023) into a two-player laboratory game.

## Model Primitives

| Symbol | Interpretation | oTree implementation |
| --- | --- | --- |
| \(c_{0,i}\) | Baseline deterministic consumption | `FIXED.c0` (held at 1.0) inside `__init__.py` |
| \(g_i\) | Growth from runtime | per-round treatment arm (`TreatmentArm.g`) |
| \(\delta\) | Baseline hazard intensity | `FIXED.delta` |
| \(\omega_i\) | Contribution to shared hazard | treatment arm entry `TreatmentArm.omega` |
| \(\kappa\) | Convexity of hazard aggregator | treatment arm entry `TreatmentArm.kappa` |
| \(H(Q)\) | Hazard aggregator \(Q + \kappa Q^2/2\) | helper `hazard_components` / `survival_probability` |
| \(S(T_1,T_2)\) | Survival probability | `survival_probability` helper |
| \(u_i(c)\) | CRRA utility | `crra_utility` inside `__init__.py` |

## Treatment dimensions

- **Fixed primitives** live in the `FIXED` dataclass (baseline consumption, hazard intensity, CRRA curvature, and token mapping).
- **Randomised primitives** sit inside `TREATMENTS`. Each `TreatmentArm` defines \((\kappa, \omega_1, \omega_2, g_1, g_2)\). The Subsession draws an arm for every pair, every round.

## Round-level flow

1. `Subsession.creating_session` pre-computes a round-robin schedule at round 1, ensuring no pair repeats before all unique pairings are exhausted. Each round loads the scheduled pairs (with \(N\) participants you can run at most \(N-1\) rounds).
2. Treatments are drawn independently for each group and round via `draw_scenario_for_groups`, so pair-level manipulations remain fully random even though the pairing schedule is deterministic.
3. Players observe the arm’s parameters on the decision page and submit a runtime choice. Input can be continuous (default slider) or replaced with dropdowns if needed.
4. `set_group_payoffs` (called from the wait page) computes survival, consumption, and expected utility using the shared-risk formulas. Token rewards shift expected utility by the within-round minimum to guarantee non-negative points.
5. Results pages show individual outcomes plus partner choices, enabling immediate feedback for learning across rounds.

## Extending the scaffold

- Add comprehension quizzes or comprehension checks by inserting extra pages before `Decision`.
- To test additional primitives (e.g., asymmetric \(g_i\) *and* \(\omega_i\)), add more `TreatmentArm` entries or adjust `draw_scenario_for_groups` to sample with replacement.
- For between-session manipulations, adjust `SESSION_CONFIGS` to pass a custom `scenario_sequence` or override `TREATMENTS` at runtime.

### Session-config wiring

Add the app to `SESSION_CONFIGS`, e.g.:

```python
dict(
    name='cournot_shared_risk_lab',
    display_name='Cournot Shared-Risk (6 rounds)',
    num_demo_participants=10,
    app_sequence=['cournot_shared_risk', 'survey'],
    random_seed=42,
)
```

Ensure that `num_demo_participants` (and thus actual session attendance) is even; the unique-pair schedule requires it. If you need more than \(N-1\) rounds for \(N\) participants, duplicate the schedule manually or relax the no-repeat constraint.

This scaffold keeps the analytics close to the formal model while remaining concise enough for rapid iteration in the lab.
