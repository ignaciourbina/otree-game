# 🤝 Cournot-Style Shared Risk Extension of the Jones (2023) Simple Model

This note augments the Section 2 “run AI for `T` years” model from Jones (2023) so that two strategic agents choose separate runtimes while sharing a *global* existential hazard, à la Cournot quantity competition. The primitives mirror the single-agent presentation in `MODEL_PRIMITIVES.md`, with all departures called out explicitly.

---

## 1. Agents, Preferences, and Controls

- Players \(i \in \{1,2\}\) (e.g., coalitions, blocs, firms) act simultaneously and non-cooperatively.
- Each player chooses a runtime \(T_i \ge 0\) for its AI system; choice sets are continuous.
- Utility over deterministic consumption \(c_i\) follows CRRA with bounded shift \(\bar u_i\):
  \[
  u_i(c) =
  \begin{cases}
  \bar u_i + \dfrac{c^{1-\gamma_i}}{1-\gamma_i}, & \gamma_i \neq 1, \\
  \bar u_i + \ln c, & \gamma_i = 1,
  \end{cases}
  \qquad
  v_i(c) \equiv \frac{u_i(c)}{u_i'(c)c}.
  \]
  As in Jones (2023), \(\bar u_i\) can be pinned down by a group-specific \(v_i(c_{0,i})\) (e.g., (=6) to match a VSL target).
- Each player takes the other player’s runtime as given, ignoring any cooperative risk internalization—this is the Cournot analogy.

---

## 2. Technological Payoffs

- Baseline consumption for player \(i\) is \(c_{0,i}\); AI raises it deterministically according to
  \[
  c_i(T_i) = c_{0,i} e^{g_i T_i},
  \]
  with \(g_i > 0\) capturing how strongly AI augments that player’s growth prospects.
- Unlike the single-agent benchmark, players do **not** share consumption, only survival odds.

---

## 3. Global Risk Aggregation

- Let aggregate “risk quantity” be the weighted sum \(Q = \omega_1 T_1 + \omega_2 T_2\), where \(\omega_i > 0\) scales how aggressively player \(i\) converts runtime into global hazard (e.g., due to scale or alignment choices).
- The shared cumulative hazard is
  \[
  \Delta(T_1,T_2) = \delta \, H(Q),
  \]
  where
  - \(\delta > 0\) is a baseline hazard intensity,
  - \(H\) is twice-differentiable, strictly increasing, and convex: \(H'(Q) > 0\), \(H''(Q) \ge 0\).
  - Convexity is what generates Cournot-style strategic interaction: the marginal hazard \(\partial \Delta / \partial T_i\) depends on *total* runtime through \(H'(Q)\).
- Survival probability common to both players:
  \[
  S(T_1,T_2) = \exp\!\left[-\,\delta H(Q)\right].
  \]
  Special case intuition:
  - If \(H(Q)=Q\), we revert to the single-agent hazard structure and strategic interaction disappears.
  - Choosing \(H(Q)= Q + \tfrac{\kappa}{2} Q^2\) (affine plus quadratic term) delivers linear-plus-convex marginal hazard \(H'(Q)=1+\kappa Q\), closely mirroring Cournot inverse demand.

---

## 4. Expected Welfare per Player

Expected payoff for player \(i\) given \((T_i,T_j)\) is
\[
W_i(T_i,T_j) \;=\; S(T_i,T_j)\,u_i\!\left(c_{0,i} e^{g_i T_i}\right)
\;=\; \exp[-\delta H(Q)]\,u_i(c_i).
\]

Taking the derivative with respect to \(T_i\) yields the first-order condition (FOC)
\[
\frac{\partial W_i}{\partial T_i} = \exp[-\delta H(Q)] \Big[-\delta H'(Q)\omega_i \, u_i(c_i) + u_i'(c_i) \, c_i \, g_i \Big]=0.
\]
Whenever interior solutions exist (\(T_i>0\)), we obtain the Cournot-adjusted value-of-life condition:
\[
v_i\!\left(c_i^\star\right) = \frac{g_i}{\delta \,\omega_i H'(Q)}. \tag{1}
\]
Equation (1) generalizes the single-agent benchmark \(v(c^\star)=g/\delta\): each player’s marginal hazard is now *endogenous*, scaled by both their own weight \(\omega_i\) and the aggregate slope \(H'(Q)\).

---

## 5. Closed-Form Best Responses

Solving (1) for \(c_i^\star\) proceeds exactly as in the single-agent model, replacing \(\delta\) with the *effective* hazard multiplier \(\delta \omega_i H'(Q)\).

### 5.1 CRRA, \(\gamma_i \neq 1\)
\[
c_i^\star(T_j) = \left[\frac{1}{\bar u_i}\left(\frac{g_i}{\delta \omega_i H'(Q)} + \frac{1}{\gamma_i-1}\right)\right]^{\!1/(\gamma_i-1)}.
\]

### 5.2 Log Utility, \(\gamma_i = 1\)
\[
c_i^\star(T_j) = \exp\!\left(\frac{g_i}{\delta \omega_i H'(Q)} - \bar u_i\right).
\]

Converting optimal consumption into optimal runtime reproduces the Jones (2023) mapping but now as a *best-response* function:
\[
T_i^\star(T_j) = \frac{1}{g_i} \ln\!\left(\frac{c_i^\star(T_j)}{c_{0,i}}\right). \tag{2}
\]
Because \(H'(Q)\) contains \(T_i^\star\) via \(Q = \omega_1 T_1^\star + \omega_2 T_2\), (2) defines player \(i\)’s best-response implicitly just like the reaction schedule in Cournot games.

---

## 6. Solving for Nash Equilibrium

Let \(R_i(T_j)\) denote the solution to (2). A Nash equilibrium \((T_1^{\text{N}}, T_2^{\text{N}})\) satisfies
\[
T_1^{\text{N}} = R_1(T_2^{\text{N}}), \qquad T_2^{\text{N}} = R_2(T_1^{\text{N}}).
\]
Closed-form solutions arise for symmetric players and simple \(H\). Example with symmetry (\(\gamma_i=\gamma\), \(g_i=g\), \(c_{0,i}=c_0\), \(\bar u_i=\bar u\), \(\omega_i=1\)) and \(H(Q)=Q+\tfrac{\kappa}{2}Q^2\):

1. Aggregate runtime at a symmetric profile is \(Q = 2T\).
2. Marginal hazard is \(H'(Q)=1+\kappa Q = 1+2\kappa T\).
3. Plugging into (1) gives the scalar equilibrium condition
   \[
   v\!\left(c_0 e^{g T}\right) = \frac{g}{\delta (1 + 2\kappa T)}. \tag{3}
   \]
4. Equation (3) collapses to the Jones (2023) FOC when \(\kappa=0\); for \(\kappa>0\), the right-hand side shrinks with total runtime, capturing the strategic substitutability of risk production. Higher \(\kappa\) therefore reduces equilibrium \(T\).

For \(\gamma \neq 1\), substituting the CRRA expression for \(v(c)\) into (3) yields an explicit scalar equation in \(T\) that can be solved via fixed-point iteration or Newton’s method. Once \(T\) is known, each player’s optimal runtime is \(T_i^{\text{N}} = T\), and total extinction probability matches the single-agent model.

## 7. Comparative Statics

| Shock | Effect on \(R_i(T_j)\) | Intuition |
| --- | --- | --- |
| ↑\(\gamma_i\) or ↑\(\bar u_i\) | Shifts \(R_i(T_j)\) downward | Higher curvature or value-of-life makes each player more cautious; they more efficiently internalize larger marginal risk. |
| ↑\(T_j\) | Lowers \(R_i(T_j)\) | Captures the Cournot-style “quantity competition”: one agent’s aggressive AI rollout tightens the other’s optimal runtime. |
| ↑\(\kappa\) | Shifts \(R_i(T_j)\) downward | Steeper hazard curvature raises the effective hazard \(\delta \omega_i H'(Q)\), so each agent shortens runtime even holding \(T_j\) fixed. |

---

## 8. Implementation Notes

- The theoretical ingredient that feeds into code is simple: replace every appearance of \(\delta\) in the single-agent formulas with the *state-dependent* effective hazard \(\delta_{\text{eff},i} = \delta \omega_i H'(Q)\) when computing best responses.
- Numerical routines can iterate best responses until convergence, evaluate symmetric equilibria, or embed this Cournot layer inside larger political-economy games.
- Because \(H'(Q)\) depends on the sum of runtimes, equilibria inherit all the standard Cournot properties (existence from monotonic best responses, potential multiplicity if \(H''\) is large, etc.).

---

**Summary:** By letting each actor pick its own runtime while sharing a convex hazard aggregator, we obtain a Cournot-style extension of the Jones (2023) static model. The optimality condition \(v_i(c_i^\star) = g_i / [\delta\,\omega_i H'(Q)]\) delivers player-specific \(T_i^\star\) that decline when others run AI longer or when the global hazard curve steepens, providing a tractable microfoundation for multi-actor AI deployment scenarios.
