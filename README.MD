# oTree Game Setup

This repository initialises a Python virtual environment that targets the
`otree` and `flask` packages, and scaffolds two oTree project layouts:

1. **`projects/default_games`** mirrors the standard oTree starter project that
   references all of the demo apps bundled with the framework. The
   configuration is ready to run once the dependencies are installed.
2. **`projects/custom_apps`** contains local copies of the Public Goods and
   Survey apps so they can be customised independently of the originals.

## Getting Started

1. Create the virtual environment (already created in `.venv/`):
   ```bash
   python3 -m venv .venv
   ```
2. Install dependencies:
   ```bash
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
   > **Note:** Package installation may require network access. In restricted
   > environments configure the proxy variables or install wheels manually.
3. Run the default demo collection:
   ```bash
   source .venv/bin/activate
   otree devserver --settings projects.default_games.settings
   ```
4. Run the custom app project with the local clones:
   ```bash
   source .venv/bin/activate
   otree devserver --settings projects.custom_apps.settings
   ```

Each project directory includes a `settings.py` file that lists its session
configurations along with short documentation to guide usage.
