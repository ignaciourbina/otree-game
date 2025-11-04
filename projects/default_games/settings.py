from os import environ

SESSION_CONFIGS = [
    dict(
        name='public_goods',
        display_name='Public Goods',
        num_demo_participants=3,
        app_sequence=['public_goods'],
    ),
    dict(
        name='trust',
        display_name='Trust',
        num_demo_participants=2,
        app_sequence=['trust'],
    ),
    dict(
        name='dictator',
        display_name='Dictator',
        num_demo_participants=2,
        app_sequence=['dictator'],
    ),
    dict(
        name='matching_pennies',
        display_name='Matching Pennies',
        num_demo_participants=2,
        app_sequence=['matching_pennies'],
    ),
    dict(
        name='traveler_dilemma',
        display_name="Traveler's Dilemma",
        num_demo_participants=2,
        app_sequence=['traveler_dilemma'],
    ),
    dict(
        name='volunteer_dilemma',
        display_name='Volunteer Dilemma',
        num_demo_participants=3,
        app_sequence=['volunteer_dilemma'],
    ),
    dict(
        name='bargaining',
        display_name='Bargaining',
        num_demo_participants=2,
        app_sequence=['bargaining'],
    ),
    dict(
        name='cournot_competition',
        display_name='Cournot Competition',
        num_demo_participants=2,
        app_sequence=['cournot_competition'],
    ),
    dict(
        name='vickrey_auction',
        display_name='Vickrey Auction',
        num_demo_participants=4,
        app_sequence=['vickrey_auction'],
    ),
    dict(
        name='battle_of_the_sexes',
        display_name='Battle of the Sexes',
        num_demo_participants=2,
        app_sequence=['battle_of_the_sexes'],
    ),
    dict(
        name='common_value_auction',
        display_name='Common Value Auction',
        num_demo_participants=3,
        app_sequence=['common_value_auction'],
    ),
    dict(
        name='hold_up',
        display_name='Hold-Up',
        num_demo_participants=2,
        app_sequence=['hold_up'],
    ),
    dict(
        name='principal_agent',
        display_name='Principal Agent',
        num_demo_participants=2,
        app_sequence=['principal_agent'],
    ),
    dict(
        name='ultimatum',
        display_name='Ultimatum',
        num_demo_participants=2,
        app_sequence=['ultimatum'],
    ),
    dict(
        name='beauty_contest',
        display_name='Beauty Contest',
        num_demo_participants=3,
        app_sequence=['beauty_contest'],
    ),
    dict(
        name='coordination',
        display_name='Coordination',
        num_demo_participants=2,
        app_sequence=['coordination'],
    ),
    dict(
        name='prisoner',
        display_name="Prisoner's Dilemma",
        num_demo_participants=2,
        app_sequence=['prisoner'],
    ),
    dict(
        name='stag_hunt',
        display_name='Stag Hunt',
        num_demo_participants=2,
        app_sequence=['stag_hunt'],
    ),
    dict(
        name='bertrand_competition',
        display_name='Bertrand Competition',
        num_demo_participants=2,
        app_sequence=['bertrand_competition'],
    ),
    dict(
        name='survey',
        display_name='Survey',
        num_demo_participants=1,
        app_sequence=['survey'],
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.0,
    participation_fee=0.0,
    doc='',
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', 'password')

DEMO_PAGE_INTRO_HTML = ''
SECRET_KEY = 'default-games-secret-key'

INSTALLED_APPS = ['otree']
