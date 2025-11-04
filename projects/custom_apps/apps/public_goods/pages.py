from otree.api import *
from .models import Constants


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def vars_for_template(player: Player):
        return dict(
            endowment=Constants.endowment,
            efficiency_factor=Constants.efficiency_factor,
        )


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    def vars_for_template(player: Player):
        group = player.group
        return dict(
            contribution=player.contribution,
            total_contribution=group.total_contribution,
            individual_share=group.individual_share,
            payoff=player.payoff,
        )


page_sequence = [Contribute, ResultsWaitPage, Results]
