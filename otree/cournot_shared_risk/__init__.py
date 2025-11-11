from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import List, Sequence, Tuple

from otree.api import *


doc = """Two-player Cournot shared-risk extension of Jones (2023)."""


@dataclass(frozen=True)
class FixedPrimitives:
    c0: float = 1.0
    delta: float = 0.01
    gamma: float = 2.0
    token_floor: float = 10.0
    token_scale: float = 150.0


@dataclass(frozen=True)
class TreatmentArm:
    label: str
    kappa: float
    omega: Tuple[float, float]
    g: Tuple[float, float]
    description: str = ""

    def as_dict(self) -> dict:
        return dict(
            label=self.label,
            kappa=self.kappa,
            omega=list(self.omega),
            g=list(self.g),
            description=self.description,
        )


FIXED = FixedPrimitives()

TREATMENTS: Sequence[TreatmentArm] = (
    TreatmentArm(
        label="Low curvature",
        kappa=0.1,
        omega=(1.0, 1.0),
        g=(0.10, 0.10),
        description="Benchmark hazard curvature with symmetric weights",
    ),
    TreatmentArm(
        label="High curvature",
        kappa=0.6,
        omega=(1.0, 1.0),
        g=(0.10, 0.10),
        description="Sharper global risk response to aggregate runtime",
    ),
    TreatmentArm(
        label="Asymmetric influence",
        kappa=0.3,
        omega=(1.0, 1.5),
        g=(0.10, 0.11),
        description="Player 2 translates runtime into hazard more strongly",
    ),
)

DEFAULT_NUM_ROUNDS = 6


def hazard_components(T1: float, T2: float, arm: TreatmentArm) -> Tuple[float, float]:
    omega1, omega2 = arm.omega
    Q = omega1 * T1 + omega2 * T2
    Hprime = 1 + arm.kappa * Q  # derivative of Q + 0.5*kappa*Q^2
    return Q, Hprime


def survival_probability(T1: float, T2: float, arm: TreatmentArm) -> float:
    Q, _ = hazard_components(T1, T2, arm)
    H = Q + 0.5 * arm.kappa * Q**2
    return math.exp(-FIXED.delta * H)


def consumption(runtime: float, growth_rate: float) -> float:
    return FIXED.c0 * math.exp(growth_rate * runtime)


def crra_utility(consumption_level: float) -> float:
    gamma = FIXED.gamma
    if gamma == 1:
        return math.log(consumption_level)
    return (consumption_level ** (1 - gamma)) / (1 - gamma)


def payoff(runtime: float, partner_runtime: float, player_idx: int, arm: TreatmentArm) -> dict:
    survival = survival_probability(runtime, partner_runtime, arm)
    consumption_i = consumption(runtime, arm.g[player_idx])
    utility = crra_utility(consumption_i)
    expected_utility = survival * utility
    return dict(
        survival=survival,
        consumption=consumption_i,
        expected_utility=expected_utility,
    )


def tokenise(expected_utility: float, min_utility: float) -> float:
    shifted = max(expected_utility - min_utility, 0)
    return FIXED.token_floor + FIXED.token_scale * shifted


def draw_scenario_for_groups(num_groups: int, rng: random.Random) -> Tuple[TreatmentArm, ...]:
    base_sequence = list(TREATMENTS)
    rng.shuffle(base_sequence)
    repetitions = math.ceil(num_groups / len(base_sequence))
    expanded = (base_sequence * repetitions)[:num_groups]
    return tuple(expanded)


def build_round_robin_schedule(players: Sequence[Player], rng: random.Random) -> List[List[Tuple[int, int]]]:
    ids = [p.participant.id_in_session for p in players]
    rng.shuffle(ids)
    n = len(ids)
    schedule: List[List[Tuple[int, int]]] = []
    for _ in range(n - 1):
        pairs = [(ids[i], ids[n - 1 - i]) for i in range(n // 2)]
        schedule.append(pairs)
        ids = [ids[0]] + [ids[-1]] + ids[1:-1]
    return schedule


def ensure_unique_pair_feasibility(num_players: int, requested_rounds: int):
    max_unique_rounds = num_players - 1
    if requested_rounds > max_unique_rounds:
        raise ValueError(
            f"num_rounds={requested_rounds} exceeds maximum unique-pair rounds ({max_unique_rounds}) "
            "for the participant count."
        )


def assign_treatment_to_group(group: Group, arm: TreatmentArm):
    group.treatment_label = arm.label
    group.kappa = arm.kappa
    group.omega1, group.omega2 = arm.omega
    group.g1, group.g2 = arm.g


def group_treatment_arm(group: Group) -> TreatmentArm:
    return TreatmentArm(
        label=group.treatment_label,
        kappa=group.kappa,
        omega=(group.omega1, group.omega2),
        g=(group.g1, group.g2),
    )


def set_group_payoffs(group: Group):
    players = group.get_players()
    runtimes = [p.runtime_choice for p in players]
    arm = group_treatment_arm(group)
    outcomes = []
    for idx, player in enumerate(players):
        partner_runtime = runtimes[1 - idx]
        outcomes.append(
            payoff(runtime=runtimes[idx], partner_runtime=partner_runtime, player_idx=idx, arm=arm)
        )

    min_expected = min(o["expected_utility"] for o in outcomes)
    for player, outcome in zip(players, outcomes):
        player.survival = outcome["survival"]
        player.consumption = outcome["consumption"]
        player.expected_utility = outcome["expected_utility"]
        player.payoff = tokenise(outcome["expected_utility"], min_expected)


class Constants(BaseConstants):
    name_in_url = "cournot_shared_risk"
    players_per_group = 2
    num_rounds = DEFAULT_NUM_ROUNDS


class Subsession(BaseSubsession):
    @staticmethod
    def creating_session(subsession: Subsession):
        players = subsession.get_players()
        if len(players) % Constants.players_per_group != 0:
            raise ValueError("Number of participants must be even for unique matching.")

        rng = random.Random()
        seed = subsession.session.config.get("random_seed")
        if seed is not None:
            rng.seed(seed + subsession.round_number)

        if subsession.round_number == 1:
            schedule = build_round_robin_schedule(players, rng)
            ensure_unique_pair_feasibility(len(players), Constants.num_rounds)
            subsession.session.vars["cournot_pair_schedule"] = schedule
        else:
            schedule = subsession.session.vars["cournot_pair_schedule"]

        round_pairs = schedule[subsession.round_number - 1]
        participant_lookup = {p.participant.id_in_session: p for p in players}
        matrix = [
            [participant_lookup[pair[0]], participant_lookup[pair[1]]] for pair in round_pairs
        ]
        subsession.set_group_matrix(matrix)

        groups = subsession.get_groups()
        assignments = draw_scenario_for_groups(num_groups=len(groups), rng=rng)
        for group, arm in zip(groups, assignments):
            assign_treatment_to_group(group, arm)


class Group(BaseGroup):
    treatment_label = models.StringField()
    kappa = models.FloatField()
    omega1 = models.FloatField()
    omega2 = models.FloatField()
    g1 = models.FloatField()
    g2 = models.FloatField()


class Player(BasePlayer):
    runtime_choice = models.FloatField(min=0, max=20, label="Choose your runtime")
    survival = models.FloatField(initial=0)
    consumption = models.FloatField(initial=0)
    expected_utility = models.FloatField(initial=0)


class Introduction(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            fixed=FIXED,
            treatments=[arm.as_dict() for arm in TREATMENTS],
            num_rounds=Constants.num_rounds,
        )


class Decision(Page):
    form_model = "player"
    form_fields = ["runtime_choice"]

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            treatment=group_treatment_arm(group).as_dict(),
            round_number=player.round_number,
            fixed=FIXED,
        )


class WaitForResults(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        set_group_payoffs(group)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        partner = player.get_others_in_group()[0]
        return dict(
            runtime=player.runtime_choice,
            partner_runtime=partner.runtime_choice,
            survival=player.survival,
            consumption=player.consumption,
            expected_utility=player.expected_utility,
            payoff=player.payoff,
            treatment=group_treatment_arm(player.group).as_dict(),
            round_number=player.round_number,
        )


page_sequence = [Introduction, Decision, WaitForResults, Results]
