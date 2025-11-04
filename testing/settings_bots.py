from os import environ

SESSION_CONFIGS = [
    dict(
        name='ai_growth_risk_bot',
        display_name='AI Growth Risk Bot Harness',
        num_demo_participants=2,
        app_sequence=['ai_growth_risk_bot'],
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
SECRET_KEY = 'ai-growth-risk-bot-secret-key'

INSTALLED_APPS = ['otree']

OTREE_APPS = ['ai_growth_risk_bot']
