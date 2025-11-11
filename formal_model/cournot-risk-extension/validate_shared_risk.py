#!/usr/bin/env python3
"""Validate the Cournot-style shared risk derivations with SymPy.

Checks performed:
1. Player-level welfare derivatives reproduce the stated FOCs.
2. The FOC rearranges to the Cournot value-of-life condition (eq. 1).
3. Closed-form best-response expressions (CRRA and log utility) match Section 5.
4. Runtime mapping (eq. 2) follows from the consumption definition.
5. The symmetric Cournot condition (eq. 3) emerges under the quadratic hazard example.
"""

from __future__ import annotations

from pathlib import Path

import sympy as sp


def assert_zero(expr: sp.Expr, label: str, log) -> None:
    """Assert that a SymPy expression simplifies to zero."""
    simplified = sp.simplify(sp.factor(expr))
    if simplified != 0:
        raise AssertionError(f"{label} check failed: {simplified}")
    log(f"[ok] {label}")


def main() -> None:
    log_lines: list[str] = []

    def log(msg: str) -> None:
        print(msg)
        log_lines.append(msg)

    # --- Shared symbols and functions ---------------------------------------------------------
    T1, T2, w1, w2, g1, g2, delta = sp.symbols(
        "T1 T2 w1 w2 g1 g2 delta", positive=True
    )
    c01, c02, ubar1, ubar2 = sp.symbols("c01 c02 ubar1 ubar2", positive=True)
    gamma1, gamma2 = sp.symbols("gamma1 gamma2")
    c = sp.symbols("c", positive=True)

    Q_expr = w1 * T1 + w2 * T2
    Q_fn = sp.Function("Q")(T1, T2)
    H = sp.Function("H")
    H_expr = H(Q_fn)
    survival_template = sp.exp(-delta * H_expr)
    survival = sp.exp(-delta * H(Q_expr))
    subs_map = {
        Q_fn: Q_expr,
        sp.diff(Q_fn, T1): w1,
        sp.diff(Q_fn, T2): w2,
    }
    Hprime = sp.diff(H_expr, Q_fn).subs(Q_fn, Q_expr)

    def crra_template(ubar_sym: sp.Symbol, gamma_sym: sp.Symbol) -> tuple[sp.Expr, sp.Expr]:
        """Return CRRA utility and its derivative wrt consumption."""
        utility = ubar_sym + c ** (1 - gamma_sym) / (1 - gamma_sym)
        return utility, sp.diff(utility, c)

    def check_player(
        label: int,
        T: sp.Symbol,
        g: sp.Symbol,
        w: sp.Symbol,
        c0: sp.Symbol,
        ubar_sym: sp.Symbol,
        gamma_sym: sp.Symbol,
    ) -> None:
        """Validate the welfare derivative and eq. (1) for a given player."""
        u_template, du_dc_template = crra_template(ubar_sym, gamma_sym)
        c_expr = c0 * sp.exp(g * T)
        u_expr = u_template.subs(c, c_expr)
        du_dc_expr = du_dc_template.subs(c, c_expr)

        welfare = survival_template * u_expr
        dW = sp.diff(welfare, T).subs(subs_map)
        expected = survival * (-delta * Hprime * w * u_expr + du_dc_expr * c_expr * g)
        assert_zero(dW - expected, f"dW/dT_{label} reproduces the FOC structure", log)

        foc_core = -delta * Hprime * w * u_expr + du_dc_expr * c_expr * g
        normalized = sp.simplify(
            foc_core / (delta * Hprime * w * du_dc_expr * c_expr)
        )
        eq1_form = sp.simplify(-u_expr / (du_dc_expr * c_expr) + g / (delta * w * Hprime))
        assert_zero(
            normalized - eq1_form,
            f"Value-of-life form (eq. 1) holds for player {label}",
            log,
        )
        value_term = sp.simplify(u_expr / (du_dc_expr * c_expr))
        log(f"Player {label} value-of-life term u/(u'c): {value_term}")
        log(f"Player {label} hazard-scaled growth term: {sp.simplify(g / (delta * w * Hprime))}")

    check_player(1, T1, g1, w1, c01, ubar1, gamma1)
    check_player(2, T2, g2, w2, c02, ubar2, gamma2)

    # --- Section 5: closed-form best responses -------------------------------------------------
    ubar, gamma, g_sym, h_eff = sp.symbols("ubar gamma g h_eff")
    c_pow = sp.symbols("c_pow")
    crra_equation = sp.Eq(ubar * c_pow - 1 / (gamma - 1), g_sym / h_eff)
    crra_solution = sp.solve(crra_equation, c_pow)[0]
    crra_doc = (g_sym / h_eff + 1 / (gamma - 1)) / ubar
    assert_zero(
        crra_solution - crra_doc,
        "CRRA best-response inversion (eq. 5.1) base",
        log,
    )
    crra_c_star = sp.simplify(crra_solution ** (1 / (gamma - 1)))
    log(f"CRRA optimal consumption c*: {crra_c_star}")

    c_star = sp.symbols("c_star", positive=True)
    log_solution = sp.solve(sp.Eq(ubar + sp.log(c_star), g_sym / h_eff), c_star)[0]
    assert_zero(
        log_solution - sp.exp(g_sym / h_eff - ubar),
        "Log-utility best response (eq. 5.2)",
        log,
    )
    log(f"Log-utility optimal consumption c*: {sp.simplify(log_solution)}")

    # Runtime mapping (eq. 2)
    c_star_sym, c0_sym, g_runtime, T_sym = sp.symbols(
        "c_star_sym c0_sym g_runtime T_sym", positive=True
    )
    runtime_solution = sp.solve(
        sp.Eq(c_star_sym, c0_sym * sp.exp(g_runtime * T_sym)), T_sym
    )[0]
    assert_zero(
        runtime_solution - sp.log(c_star_sym / c0_sym) / g_runtime,
        "Consumption-to-runtime mapping (eq. 2)",
        log,
    )
    log(f"Runtime mapping T(c*): {sp.simplify(runtime_solution)}")

    # --- Section 6: symmetric Cournot condition (eq. 3) ----------------------------------------
    T_equil, kappa, g_common = sp.symbols("T_equil kappa g_common", positive=True)
    Q_sym = sp.symbols("Q_sym", positive=True)
    H_special = Q_sym + kappa * Q_sym ** 2 / 2
    Hprime_special = sp.diff(H_special, Q_sym)
    rhs = sp.simplify(g_common / (delta * Hprime_special.subs(Q_sym, 2 * T_equil)))
    assert_zero(
        rhs - g_common / (delta * (1 + 2 * kappa * T_equil)),
        "Symmetric hazard condition (eq. 3)",
        log,
    )
    log(f"Symmetric Cournot RHS expression: {rhs}")

    log("")
    log("All symbolic checks passed.")

    log_path = Path(__file__).with_name("validate_shared_risk.log.txt")
    footer = f"Log saved to {log_path}"
    log_path.write_text("\n".join([*log_lines, footer]) + "\n")
    print(footer)


if __name__ == "__main__":
    main()
