import json
import math
import random

from otree.api import *

from formal_model.jones_models import SimpleAIGrowthRiskModel, Utility


class Constants(BaseConstants):
    name_in_url = 'ai_growth_risk'
    players_per_group = 2
    num_rounds = 1

    #: Hard-coded scenario catalogue for between-subject randomisation. Each
    #: entry stores the structural primitives, runtime menu, and incentive
    #: mapping calibrated from the Jones (2023) model. Researchers can edit
    #: this table to add/remove scenarios without exposing configuration
    #: controls to participants.
    SCENARIOS = [
        dict(
            code='baseline',
            label='Balanced benchmark',
            base_params=dict(
                c0=1.0,
                g=0.10,
                delta_=0.01,
                gamma=2.0,
                target_v=6.0,
            ),
            runtime_menu=[
                dict(
                    id='conservative',
                    label='Safety First',
                    description='Prioritise containment and shut down earlier.',
                    runtime=4.0,
                ),
                dict(
                    id='balanced',
                    label='Balanced Benchmark',
                    description='Aligns closely with the theoretical optimum.',
                    runtime=8.0,
                ),
                dict(
                    id='ambitious',
                    label='Growth Push',
                    description='Extend runtime to pursue additional growth.',
                    runtime=12.0,
                ),
            ],
            token_floor=10.0,
            token_scale=150.0,
        ),
        dict(
            code='growth_tilt',
            label='High growth environment',
            base_params=dict(
                c0=1.0,
                g=0.13,
                delta_=0.01,
                gamma=2.0,
                target_v=6.5,
            ),
            runtime_menu=[
                dict(
                    id='rapid',
                    label='Rapid Shutdown',
                    description='Lock in gains quickly despite the growth potential.',
                    runtime=4.0,
                ),
                dict(
                    id='extended',
                    label='Extended Deployment',
                    description='Keep systems online longer to capture higher growth.',
                    runtime=10.0,
                ),
                dict(
                    id='maximal',
                    label='Maximal Run',
                    description='Run to the practical limit to chase growth.',
                    runtime=14.0,
                ),
            ],
            token_floor=10.0,
            token_scale=160.0,
        ),
        dict(
            code='risk_tilt',
            label='High risk environment',
            base_params=dict(
                c0=1.0,
                g=0.09,
                delta_=0.02,
                gamma=2.0,
                target_v=5.5,
            ),
            runtime_menu=[
                dict(
                    id='safest',
                    label='Early Shutdown',
                    description='Terminate quickly to avoid heightened extinction risk.',
                    runtime=3.0,
                ),
                dict(
                    id='middle',
                    label='Moderate Run',
                    description='Balance risk and reward in a fragile environment.',
                    runtime=6.0,
                ),
                dict(
                    id='bold',
                    label='Bold Run',
                    description='Accept additional catastrophic risk to seek gains.',
                    runtime=9.0,
                ),
            ],
            token_floor=10.0,
            token_scale=140.0,
        ),
    ]


class Subsession(BaseSubsession):
    @staticmethod
    def _prepare_scenario(base_params, runtime_menu, token_floor, token_scale):
        model = SimpleAIGrowthRiskModel(**base_params)
        summary = model.summary()
        util = Utility(base_params['gamma'], summary['ubar'])

        optimal_runtime = summary['T_star']
        optimal_consumption = base_params['c0'] * math.exp(
            base_params['g'] * optimal_runtime
        )
        optimal_survival_prob = math.exp(-base_params['delta_'] * optimal_runtime)
        optimal_expected_utility = optimal_survival_prob * util.u(optimal_consumption)

        options = []
        expected_utilities = []
        for option in runtime_menu:
            runtime = float(option['runtime'])
            consumption = base_params['c0'] * math.exp(base_params['g'] * runtime)
            survival_prob = math.exp(-base_params['delta_'] * runtime)
            expected_utility = survival_prob * util.u(consumption)
            expected_utilities.append(expected_utility)
            options.append(
                dict(
                    id=option['id'],
                    label=option.get('label', option['id'].title()),
                    description=option.get('description', ''),
                    runtime=runtime,
                    survival_prob=survival_prob,
                    extinction_prob=1 - survival_prob,
                    expected_utility=expected_utility,
                )
            )

        min_expected_utility = min(expected_utilities)
        for option in options:
            shifted = max(option['expected_utility'] - min_expected_utility, 0)
            option['token_preview'] = token_floor + token_scale * shifted

        runtime_lookup = {opt['id']: opt['runtime'] for opt in options}
        bounded_optimal_runtime = min(
            max(optimal_runtime, min(runtime_lookup.values())),
            max(runtime_lookup.values()),
        )

        optimal_shifted = max(optimal_expected_utility - min_expected_utility, 0)
        optimal_tokens = token_floor + token_scale * optimal_shifted

        return dict(
            options=options,
            runtime_lookup=runtime_lookup,
            summary=summary,
            optimal_runtime=optimal_runtime,
            optimal_consumption=optimal_consumption,
            optimal_survival_prob=optimal_survival_prob,
            optimal_expected_utility=optimal_expected_utility,
            bounded_optimal_runtime=bounded_optimal_runtime,
            optimal_tokens=optimal_tokens,
            min_expected_utility=min_expected_utility,
        )

    def creating_session(self):
        scenarios = Constants.SCENARIOS
        if not scenarios:
            raise ValueError('Constants.SCENARIOS must define at least one scenario')

        rng = random.Random()
        seed = self.session.config.get('random_seed')
        if seed is not None:
            rng.seed(seed)

        groups = self.get_groups()
        repetitions = math.ceil(len(groups) / len(scenarios))
        expanded = scenarios * repetitions
        rng.shuffle(expanded)
        assignments = expanded[: len(groups)]

        for group, scenario in zip(groups, assignments):
            base_params = scenario['base_params']
            runtime_menu = scenario['runtime_menu']
            token_floor = scenario['token_floor']
            token_scale = scenario['token_scale']

            prepared = self._prepare_scenario(
                base_params, runtime_menu, token_floor, token_scale
            )

            group.scenario_code = scenario['code']
            group.scenario_label = scenario.get('label', scenario['code'].title())
            group.c0 = base_params['c0']
            group.g = base_params['g']
            group.delta = base_params['delta_']
            group.gamma = base_params['gamma']
            group.target_v = base_params['target_v']
            group.ubar = prepared['summary']['ubar']
            group.c_star = prepared['summary']['c_star']
            group.optimal_runtime = prepared['optimal_runtime']
            group.bounded_optimal_runtime = prepared['bounded_optimal_runtime']
            group.optimal_consumption = prepared['optimal_consumption']
            group.optimal_survival_prob = prepared['optimal_survival_prob']
            group.optimal_extinction_prob = prepared['summary']['extinction_prob']
            group.optimal_expected_utility = prepared['optimal_expected_utility']
            group.optimal_tokens = prepared['optimal_tokens']
            group.token_floor = token_floor
            group.token_scale = token_scale
            group.min_expected_utility = prepared['min_expected_utility']
            group.runtime_choices_blob = json.dumps(prepared['options'])

        for player in self.get_players():
            options = player.group.runtime_options()
            default_choice = options[0]
            player.runtime_choice = default_choice['id']
            player.runtime_years = default_choice['runtime']


class Group(BaseGroup):
    scenario_code = models.StringField()
    scenario_label = models.StringField()
    c0 = models.FloatField()
    g = models.FloatField()
    delta = models.FloatField()
    gamma = models.FloatField()
    target_v = models.FloatField()
    ubar = models.FloatField()

    c_star = models.FloatField()
    optimal_runtime = models.FloatField()
    bounded_optimal_runtime = models.FloatField()
    optimal_consumption = models.FloatField()
    optimal_survival_prob = models.FloatField()
    optimal_extinction_prob = models.FloatField()
    optimal_expected_utility = models.FloatField()
    optimal_tokens = models.FloatField()

    token_floor = models.FloatField()
    token_scale = models.FloatField()
    min_expected_utility = models.FloatField()
    runtime_choices_blob = models.LongStringField()

    collective_runtime = models.FloatField(initial=0)
    collective_consumption = models.FloatField(initial=0)
    collective_survival_prob = models.FloatField(initial=0)
    collective_extinction_prob = models.FloatField(initial=0)
    collective_expected_utility = models.FloatField(initial=0)
    collective_tokens = models.FloatField(initial=0)

    def runtime_options(self):
        return json.loads(self.runtime_choices_blob)

    def runtime_for_choice(self, choice_id: str) -> float:
        for option in self.runtime_options():
            if option['id'] == choice_id:
                return option['runtime']
        raise ValueError(f'Unknown runtime choice: {choice_id}')

    def set_payoffs(self):
        players = self.get_players()
        runtimes = []
        for player in players:
            runtime_years = self.runtime_for_choice(player.runtime_choice)
            player.runtime_years = runtime_years
            runtimes.append(runtime_years)

        runtime = sum(runtimes) / len(runtimes)
        self.collective_runtime = runtime

        consumption = self.c0 * math.exp(self.g * runtime)
        survival_prob = math.exp(-self.delta * runtime)
        extinction_prob = 1 - survival_prob

        util = Utility(self.gamma, self.ubar)
        expected_utility = survival_prob * util.u(consumption)

        shifted_expected = max(expected_utility - self.min_expected_utility, 0)
        tokens = self.token_floor + self.token_scale * shifted_expected

        self.collective_consumption = consumption
        self.collective_survival_prob = survival_prob
        self.collective_extinction_prob = extinction_prob
        self.collective_expected_utility = expected_utility
        self.collective_tokens = tokens

        runtime_gap = runtime - self.optimal_runtime
        for player in players:
            player.payoff = cu(tokens)
            player.token_payoff = tokens
            player.realized_consumption = consumption
            player.realized_survival_prob = survival_prob
            player.realized_extinction_prob = extinction_prob
            player.realized_expected_utility = expected_utility
            player.runtime_gap = runtime_gap


class Player(BasePlayer):
    runtime_choice = models.StringField()
    runtime_years = models.FloatField()
    realized_consumption = models.FloatField()
    realized_survival_prob = models.FloatField()
    realized_extinction_prob = models.FloatField()
    realized_expected_utility = models.FloatField()
    runtime_gap = models.FloatField()
    token_payoff = models.FloatField()

    def runtime_choice_choices(self):
        return [
            (option['id'], option['label'])
            for option in self.group.runtime_options()
        ]

    def runtime_choice_error_message(self, value):
        if value not in {option['id'] for option in self.group.runtime_options()}:
            return 'Please select one of the available runtime plans.'
