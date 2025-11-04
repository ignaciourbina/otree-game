# Custom Apps Project

This project provides local copies of the Public Goods and Survey apps so they
can be customised independently of the templates bundled with the `otree`
distribution. Both apps live inside the `apps/` package and are referenced by
the project `settings.py` module using their fully-qualified module paths.

To run the project once the dependencies are available:

```bash
source ../../.venv/bin/activate
otree devserver --settings projects.custom_apps.settings
```

Passing the settings module ensures oTree loads the configuration that points to
these local clones. You can freely extend the game logic or pages within the app
folders.
