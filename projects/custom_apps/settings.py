from os import environ

SESSION_CONFIGS = [
    dict(
        name='public_goods_clone',
        display_name='Public Goods (Local Copy)',
        num_demo_participants=3,
        app_sequence=['projects.custom_apps.apps.public_goods'],
    ),
    dict(
        name='survey_clone',
        display_name='Survey (Local Copy)',
        num_demo_participants=1,
        app_sequence=['projects.custom_apps.apps.survey'],
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
