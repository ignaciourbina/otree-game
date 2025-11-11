# Custom Apps Project

This project provides local copies of the Public Goods and Survey apps so they
can be customised independently of the templates bundled with the `otree`
distribution. Both apps live inside the `apps/` package and are referenced by
the project `settings.py` module using their fully-qualified module paths.

In addition, the project hosts a bespoke two-player `ai_growth_risk` app that
translates the Jones (2023) AI growth–risk formal model into an experimental
oTree game. Participants no longer manipulate the model primitives directly;
instead, researchers curate a catalogue of deployment-plan scenarios (each
mapping to a runtime in the formal model) and the incentive-compatible
conversion from model utility into lab tokens. At session start the app
randomly assigns each two-player group to one of these hard-coded scenarios,
ensuring a between-subjects design without exposing a configuration UI.
Players simply pick among the labelled plans and earn tokens based on the
average runtime, while the app records the underlying consumption, risk, and
utility outcomes for structural estimation.

To run the project once the dependencies are available:

```bash
source ../../.venv/bin/activate
otree devserver --settings projects.custom_apps.settings
```

Passing the settings module ensures oTree loads the configuration that points to
these local clones. You can freely extend the game logic or pages within the app
folders.
