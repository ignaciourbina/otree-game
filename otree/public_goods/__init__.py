from otree.api import *

class Constants(BaseConstants):
    name_in_url = 'public_goods'
    players_per_group = 3
    num_rounds = 1
    endowment = cu(20)
    efficiency_factor = 1.5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField(initial=0)
    individual_share = models.CurrencyField(initial=0)

    def set_payoffs(self):
        players = self.get_players()
        total = sum(p.contribution for p in players)
        self.total_contribution = total
        if Constants.players_per_group:
            share = total * Constants.efficiency_factor / Constants.players_per_group
        else:
            share = cu(0)
        self.individual_share = share
        for p in players:
            p.payoff = Constants.endowment - p.contribution + share


class Player(BasePlayer):
    contribution = models.CurrencyField(
        min=0,
        max=Constants.endowment,
        label='How much will you contribute to the group project?',
    )




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
