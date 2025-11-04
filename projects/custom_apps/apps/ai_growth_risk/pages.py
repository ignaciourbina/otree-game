from otree.api import *

from .models import Group, Player


class Introduction(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        options = group.runtime_options()
        return dict(
            options=options,
            benchmark_runtime=group.bounded_optimal_runtime,
            benchmark_tokens=max(option['token_preview'] for option in options),
            scenario_label=group.scenario_label,
        )


class Decision(Page):
    form_model = 'player'
    form_fields = ['runtime_choice']

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            options=group.runtime_options(),
            current_choice=player.runtime_choice,
            scenario_label=group.scenario_label,
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group: Group = player.group
        partner = player.get_others_in_group()[0]
        options = group.runtime_options()
        choice_labels = {option['id']: option['label'] for option in options}
        player_label = choice_labels.get(player.runtime_choice, player.runtime_choice)
        partner_label = choice_labels.get(partner.runtime_choice, partner.runtime_choice)
        return dict(
            scenario_label=group.scenario_label,
            player_choice=player.runtime_choice,
            partner_choice=partner.runtime_choice,
            player_runtime_years=player.runtime_years,
            partner_runtime_years=partner.runtime_years,
            collective_runtime=group.collective_runtime,
            benchmark_runtime=group.bounded_optimal_runtime,
            runtime_gap=player.runtime_gap,
            collective_consumption=group.collective_consumption,
            collective_survival_prob=group.collective_survival_prob,
            collective_extinction_prob=group.collective_extinction_prob,
            collective_expected_utility=group.collective_expected_utility,
            optimal_consumption=group.optimal_consumption,
            optimal_survival_prob=group.optimal_survival_prob,
            optimal_extinction_prob=group.optimal_extinction_prob,
            optimal_expected_utility=group.optimal_expected_utility,
            optimal_tokens=group.optimal_tokens,
            collective_tokens=group.collective_tokens,
            player_tokens=player.token_payoff,
            partner_tokens=partner.token_payoff,
            player_label=player_label,
            partner_label=partner_label,
        )


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
