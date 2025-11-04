"""Formalization of Jones (2023) AI growth and risk models.

This module provides two object-oriented implementations of the models
presented in Jones (2023):

* :class:`SimpleAIGrowthRiskModel` replicates the "run AI for ``T`` years"
  model from Section 2.
* :class:`DynamicAIGrowthRiskModel` implements the dynamic adoption model from
  Section 3, including the singularity limit.

The classes are designed for experimentation and comparative statics. See
``formal_model/USAGE.md`` for usage examples.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def calibrate_ubar_from_v(c0: float, gamma: float, target_v: float = 6.0) -> float:
    """Calibrate :math:`\bar{u}` from a target value of :math:`v(c_0)`.

    Jones (2023) matches ``v(c0) ≈ 6`` to US value-of-statistical-life (VSL)
    estimates. This helper replicates that calibration for either CRRA
    (``gamma != 1``) or log utility (``gamma == 1``).

    Parameters
    ----------
    c0:
        Baseline consumption level.
    gamma:
        Relative risk aversion coefficient.
    target_v:
        Desired value of :math:`v(c_0)`.

    Returns
    -------
    float
        The calibrated :math:`\bar{u}`.
    """

    if gamma == 1.0:
        return target_v - math.log(c0)

    return (target_v - 1.0 / (1.0 - gamma)) / (c0 ** (gamma - 1.0))


# ---------------------------------------------------------------------------
# Base utility class
# ---------------------------------------------------------------------------


@dataclass
class Utility:
    """CRRA (or log) utility with a level shift ``ubar``."""

    gamma: float
    ubar: float

    def u(self, c: float) -> float:
        """Utility function ``u(c)``."""

        if self.gamma == 1.0:
            return self.ubar + math.log(c)
        return self.ubar + (c ** (1.0 - self.gamma)) / (1.0 - self.gamma)

    def u_prime(self, c: float) -> float:
        """Marginal utility ``u'(c)``."""

        if self.gamma == 1.0:
            return 1.0 / c
        return c ** (-self.gamma)

    def v(self, c: float) -> float:
        """Convenience function :math:`v(c) = u(c)/(u'(c) c)`."""

        if self.gamma == 1.0:
            return self.u(c)
        return self.ubar * (c ** (self.gamma - 1.0)) + 1.0 / (1.0 - self.gamma)


# ---------------------------------------------------------------------------
# Section 2: Simple model
# ---------------------------------------------------------------------------


class SimpleAIGrowthRiskModel:
    """Section 2 "run AI for ``T`` years" model from Jones (2023)."""

    def __init__(
        self,
        c0: float = 1.0,
        g: float = 0.10,
        delta_: float = 0.01,
        gamma: float = 2.0,
        ubar: Optional[float] = None,
        target_v: float = 6.0,
    ) -> None:
        self.c0 = c0
        self.g = g
        self.delta_ = delta_
        self.gamma = gamma
        if ubar is None:
            ubar = calibrate_ubar_from_v(c0, gamma, target_v)
        self.util = Utility(gamma, ubar)

    # -- Core formulas ----------------------------------------------------

    def c_star(self) -> float:
        """Optimal consumption threshold :math:`c^*` (eq. 3)."""

        g_over_delta = self.g / self.delta_
        if self.gamma == 1.0:
            return math.exp(g_over_delta - self.util.ubar)
        inner = (1.0 / self.util.ubar) * (
            g_over_delta + 1.0 / (self.gamma - 1.0)
        )
        return inner ** (1.0 / (self.gamma - 1.0))

    def T_star(self) -> float:
        """Optimal runtime ``T*`` for AI."""

        cstar = self.c_star()
        return (1.0 / self.g) * math.log(cstar / self.c0)

    def total_extinction_prob(self) -> float:
        """Total extinction probability ``1 - exp(-δ T*)``."""

        T = self.T_star()
        return 1.0 - math.exp(-self.delta_ * T)

    def summary(self) -> Dict[str, float]:
        """Return a summary dictionary of the key statistics."""

        return {
            "c_star": self.c_star(),
            "T_star": self.T_star(),
            "extinction_prob": self.total_extinction_prob(),
            "ubar": self.util.ubar,
            "gamma": self.gamma,
            "g": self.g,
            "delta": self.delta_,
        }

    # -- Comparative statics --------------------------------------------

    def comparative_statics_over_delta(
        self, deltas: List[float]
    ) -> List[Dict[str, float]]:
        """Sweep over ``δ`` while keeping other parameters fixed."""

        out = []
        for d in deltas:
            self.delta_ = d
            res = self.summary()
            res["delta"] = d
            out.append(res)
        return out

    def comparative_statics_over_g(self, gs: List[float]) -> List[Dict[str, float]]:
        """Sweep over growth rates ``g``."""

        out = []
        for g in gs:
            self.g = g
            res = self.summary()
            res["g"] = g
            out.append(res)
        return out


# ---------------------------------------------------------------------------
# Section 3: Dynamic model
# ---------------------------------------------------------------------------


class DynamicAIGrowthRiskModel:
    """Section 3 dynamic adoption model from Jones (2023)."""

    def __init__(
        self,
        c0: float = 1.0,
        N0: float = 1.0,
        gamma: float = 2.0,
        ubar: Optional[float] = None,
        target_v: float = 6.0,
        rho_minus_b: float = 0.01,
        g0: float = 0.02,
        m0: float = 0.01,
    ) -> None:
        self.c0 = c0
        self.N0 = N0
        self.gamma = gamma
        if ubar is None:
            ubar = calibrate_ubar_from_v(c0, gamma, target_v)
        self.util = Utility(gamma, ubar)
        self.rho_minus_b = rho_minus_b
        self.g0 = g0
        self.m0 = m0

    def welfare(self, g: float, m: float) -> float:
        """Social welfare ``U(g, m)`` (eq. 4)."""

        top_part = self.N0 * self.util.ubar / (self.rho_minus_b + m)
        bottom_part = (
            self.N0
            * (self.c0 ** (1.0 - self.gamma))
            / (1.0 - self.gamma)
            * 1.0
            / (self.rho_minus_b + m + (self.gamma - 1.0) * g)
        )
        return top_part + bottom_part

    def delta_star(self, g_ai: float, m_ai: float) -> float:
        """Maximum tolerable one-time risk ``δ*``."""

        U0 = self.welfare(self.g0, self.m0)
        U_ai = self.welfare(g_ai, m_ai)
        return 1.0 - U0 / U_ai

    def delta_star_singularity(self, m_ai: float) -> float:
        """Singularity limit with infinite growth (eq. 7)."""

        U0 = self.welfare(self.g0, self.m0)
        U_sing = self.N0 * self.util.ubar / (self.rho_minus_b + m_ai)
        return 1.0 - U0 / U_sing

    def sweep_mortality(self, g_ai: float, m_vals: List[float]) -> List[Dict[str, float]]:
        """Sweep ``δ*`` across mortality adjustments."""

        out = []
        for m_ai in m_vals:
            dstar = self.delta_star(g_ai, m_ai)
            out.append({"m_ai": m_ai, "g_ai": g_ai, "delta_star": dstar})
        return out

    def sweep_growth(self, g_vals: List[float], m_ai: float) -> List[Dict[str, float]]:
        """Sweep ``δ*`` across AI-driven growth rates."""

        out = []
        for g_ai in g_vals:
            dstar = self.delta_star(g_ai, m_ai)
            out.append({"g_ai": g_ai, "m_ai": m_ai, "delta_star": dstar})
        return out


__all__ = [
    "calibrate_ubar_from_v",
    "Utility",
    "SimpleAIGrowthRiskModel",
    "DynamicAIGrowthRiskModel",
]
