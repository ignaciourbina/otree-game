#!/usr/bin/env python3
"""Auto-generate a LaTeX write-up of the Cournot shared-risk derivations."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


def latex(expr: sp.Expr) -> str:
    """Return a nicely simplified LaTeX string for the given SymPy expression."""
    return sp.latex(sp.simplify(expr))


def main() -> None:
    # Symbols using the notation from the note.
    delta = sp.Symbol(r"\delta", positive=True)
    omega = sp.Symbol(r"\omega_i", positive=True)
    g = sp.Symbol(r"g_i", positive=True)
    c0 = sp.Symbol(r"c_{0,i}", positive=True)
    ubar = sp.Symbol(r"\bar{u}_i", positive=True)
    gamma = sp.Symbol(r"\gamma_i")
    T = sp.Symbol(r"T_i", positive=True)
    c_sym = sp.Symbol(r"c_i", positive=True)
    Q = sp.Symbol("Q", positive=True)
    H_Q = sp.Function("H")(Q)
    Hprime = sp.diff(H_Q, Q)

    # Consumption path and welfare derivative.
    c_expr = c0 * sp.exp(g * T)
    u_template = ubar + c_sym ** (1 - gamma) / (1 - gamma)
    value_term = sp.simplify(u_template / (sp.diff(u_template, c_sym) * c_sym))
    u_at_T = u_template.subs(c_sym, c_expr)
    du_dc_at_T = sp.diff(u_template, c_sym).subs(c_sym, c_expr)
    W_expr = sp.exp(-delta * H_Q) * u_at_T
    dW_expr = sp.exp(-delta * H_Q) * (
        -delta * Hprime * omega * u_at_T + du_dc_at_T * c_expr * g
    )
    hazard_term = sp.simplify(g / (delta * omega * Hprime))

    # Best responses.
    h_eff = sp.Symbol(r"h_{\text{eff}}", positive=True)
    c_pow = sp.Symbol(r"c_{\mathrm{pow}}", positive=True)
    crra_equation = sp.Eq(ubar * c_pow - 1 / (gamma - 1), g / h_eff)
    crra_solution = sp.solve(crra_equation, c_pow)[0] ** (1 / (gamma - 1))
    crra_c_star = sp.simplify(crra_solution.subs(h_eff, delta * omega * Hprime))

    c_star_symbol = sp.Symbol(r"c_i^\star", positive=True)
    log_solution = sp.solve(
        sp.Eq(ubar + sp.log(c_star_symbol), g / (delta * omega * Hprime)),
        c_star_symbol,
    )[0]

    T_star = sp.Symbol(r"T_i^\star", positive=True)
    runtime_solution = sp.solve(
        sp.Eq(c_star_symbol, c0 * sp.exp(g * T_star)), T_star
    )[0]

    # Cournot quadratic hazard example.
    kappa = sp.Symbol(r"\kappa", positive=True)
    Q_sym = sp.Symbol("Q", positive=True)
    H_special = Q_sym + kappa * Q_sym ** 2 / 2
    Hprime_special = sp.diff(H_special, Q_sym)
    T_shared = sp.Symbol("T", positive=True)
    g_common = sp.Symbol("g", positive=True)
    symmetric_rhs = sp.simplify(g_common / (delta * (1 + 2 * kappa * T_shared)))

    # Build LaTeX document.
    doc_lines: list[str] = [
        r"\documentclass{article}",
        r"\usepackage{amsmath}",
        r"\usepackage{amssymb}",
        r"\begin{document}",
        r"\section*{Automated Cournot Shared-Risk Derivations}",
        r"\subsection*{Model Primitives}",
        r"We mirror the primitives in the main note, now rendered symbolically:",
        r"\begin{itemize}",
        r"\item \textbf{Players}: two agents $i \in \{1,2\}$ simultaneously choose runtimes $T_i \ge 0$ for their AI systems.",
        r"\item \textbf{Technology}: deterministic consumption scales with runtime via",
        r"\begin{equation}",
        r"c_i(T_i) = " + latex(c_expr),
        r"\end{equation}",
        r"unlocking exponential growth at rate $g_i$ from baseline $c_{0,i}$.",
        r"\item \textbf{Preferences}: CRRA utility with bounded shift provides a tractable value-of-life concept:",
        r"\begin{equation}",
        r"u_i(c) = " + latex(u_template),
        r"\end{equation}",
        r"\item \textbf{Risk Aggregation}: runtimes feed a convex global hazard $H(Q)$ with weights $\omega_i$,",
        r"\begin{equation}",
        r"S(T_1,T_2) = e^{-\delta H(Q)}, \quad Q = \omega_1 T_1 + \omega_2 T_2.",
        r"\end{equation}",
        r"\end{itemize}",
        r"\subsection*{Optimization Problem}",
        r"Each agent solves a single-variable calculus problem treating $T_j$ as fixed:",
        r"\begin{equation}",
        r"\max_{T_i \ge 0} \; W_i(T_i,T_j) = " + latex(W_expr),
        r"\end{equation}",
        r"subject to the implicit dependence of $Q$ on both runtimes. SymPy keeps the best-response perspective by leaving $T_j$ symbolic.",
        r"\subsection*{Analytical Strategy}",
        r"The symbolic pipeline mirrors the hand derivation, but each step is now automated:",
        r"\begin{enumerate}",
        r"\item \textbf{Embed technology in preferences}: Substitute $c_i(T_i)$ into $u_i(c)$ so that welfare carries runtime explicitly.",
        r"\item \textbf{Differentiate welfare}: Form $W_i(T_i,T_j)=S(T_i,T_j)u_i(c_i(T_i))$ and take $\partial W_i/\partial T_i$.",
        r"\item \textbf{Normalize the FOC}: Divide by $S u'_i(c_i)c_i$ to isolate the value-of-life ratio $v_i(c_i)=u_i/(u'_i c_i)$.",
        r"\item \textbf{Solve for best responses}: Invert the value-of-life condition under CRRA and logarithmic utility assumptions.",
        r"\item \textbf{Map back to runtimes}: Convert $c_i^\star$ into $T_i^\star$ through the exponential technology and inspect symmetric Cournot equilibria.",
        r"\end{enumerate}",
        r"\subsection*{Expected Welfare Derivative}",
        r"Executing Steps 1--2 yields a FOC whose two terms cleanly separate the marginal survival cost and consumption benefit:",
        r"\begin{equation}",
        r"\frac{\partial W_i}{\partial T_i} = " + latex(dW_expr),
        r"\end{equation}",
        r"To make the comparison explicit, recall that SymPy computes",
        r"\begin{equation}",
        r"u'_i(c_i)c_i = " + latex(sp.simplify(du_dc_at_T * c_expr)),
        r"\end{equation}",
        r"The first component $\propto -\delta \omega_i H'(Q)$ discounts utility by the incremental hazard, while the second captures direct consumption gains $\propto g_i u'_i(c_i)c_i$.",
        r"\subsection*{Value-of-Life Condition}",
        r"Step 3 divides the FOC by the positive term $S u'_i(c_i)c_i$, transforming it into the Cournot-style value-of-life balance:",
        r"\begin{equation}",
        r"v_i(c_i) = " + latex(value_term) + " = " + latex(hazard_term),
        r"\end{equation}",
        r"The left-hand side $v_i(c_i)$ encodes preferences only, while the right-hand side shows how growth benefits are scaled down by endogenous hazard $\delta \omega_i H'(Q)$.",
        r"\subsection*{Closed-Form Best Responses}",
        r"Steps 4--5 invert the condition for the two canonical preference cases.",
        r"\paragraph{CRRA ($\gamma_i \neq 1$).}",
        r"Solving $v_i(c_i^\star)=g_i/(\delta \omega_i H'(Q))$ produces",
        r"\begin{equation}",
        r"c_i^\star(T_j) = " + latex(crra_c_star),
        r"\end{equation}",
        r"which reduces to the single-agent solution when $H'(Q)$ is constant.",
        r"\paragraph{Log utility ($\gamma_i = 1$).}",
        r"With $\gamma_i=1$, SymPy recovers the exponential best response",
        r"\begin{equation}",
        r"c_i^\star(T_j) = " + latex(log_solution),
        r"\end{equation}",
        r"\subsection*{Back-Substituting for Runtime}",
        r"Substituting $c_i^\star$ into $c_{0,i}e^{g_i T_i}$ reintroduces runtimes, turning consumption best responses into reaction functions:",
        r"\begin{equation}",
        r"T_i^\star(T_j) = " + latex(runtime_solution),
        r"\end{equation}",
        r"\subsection*{Symmetric Cournot Hazard Example}",
        r"To illustrate Step 5, we specialize to $H(Q)=Q+\frac{\kappa}{2}Q^2$, yielding",
        r"\begin{equation}",
        r"H(Q) = " + latex(H_special) + r", \quad H'(Q) = " + latex(Hprime_special),
        r"\end{equation}",
        r"Evaluating at the symmetric profile $Q=2T$ recovers the textbook Cournot attenuation of marginal benefits:",
        r"\begin{equation}",
        r"v\!\left(c_0 e^{g T}\right) = " + latex(symmetric_rhs),
        r"\end{equation}",
        r"\end{document}",
    ]

    out_path = Path(__file__).with_name("shared_risk_derivations.tex")
    out_path.write_text("\n".join(doc_lines) + "\n")
    print(f"LaTeX derivation written to {out_path}")


if __name__ == "__main__":
    main()
