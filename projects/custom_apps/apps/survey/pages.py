from otree.api import *
from .models import Constants


class Survey(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'education',
        'economics_courses',
        'satisfaction',
        'comments',
    ]


class Results(Page):
    def vars_for_template(player: Player):
        return dict(
            age=player.age,
            gender=player.gender,
            education=player.education,
            economics_courses=player.economics_courses,
            satisfaction=player.satisfaction,
            comments=player.comments,
        )


page_sequence = [Survey, Results]
