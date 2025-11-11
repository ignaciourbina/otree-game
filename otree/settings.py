from os import environ

SESSION_CONFIGS = [
    dict(
        name='cournot_shared_risk_lab',
        display_name='Cournot Shared-Risk (6 rounds)',
        num_demo_participants=6,
        app_sequence=['cournot_shared_risk'],
        random_seed=42,
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
SECRET_KEY = 'custom-apps-secret-key'

INSTALLED_APPS = ['otree']
