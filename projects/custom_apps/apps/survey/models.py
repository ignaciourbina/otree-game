from otree.api import *


class Constants(BaseConstants):
    name_in_url = 'survey'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='What is your age?', min=13, max=125)
    gender = models.StringField(
        label='How do you describe your gender?',
        choices=['Female', 'Male', 'Non-binary', 'Prefer not to say'],
    )
    education = models.StringField(
        label='What is the highest degree or level of school you have completed?',
        choices=[
            'Some high school',
            'High school diploma or equivalent',
            'Some college',
            'Bachelor\'s degree',
            'Graduate degree',
        ],
    )
    economics_courses = models.IntegerField(
        label='How many economics or game theory courses have you taken?',
        min=0,
        max=20,
    )
    satisfaction = models.IntegerField(
        label='How satisfied are you with your experience today?',
        choices=[1, 2, 3, 4, 5],
        widget=widgets.RadioSelectHorizontal,
    )
    comments = models.LongStringField(
        label='Please share any additional comments you may have:',
        blank=True,
    )
