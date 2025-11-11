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
