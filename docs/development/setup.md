# Development Setup

Complete guide to setting up your development environment for the oTree AI Growth-Risk Experiments project.

## Prerequisites

### Required

- **Python 3.8+** (3.10+ recommended)
- **Git** 2.0+
- **pip** (usually included with Python)

### Recommended

- **VS Code** with Python extension
- **pyenv** for Python version management
- **Make** for task automation

## Step-by-Step Setup

### 1. Clone the Repository

```bash
# Clone your fork (recommended for contributing)
git clone https://github.com/YOUR_USERNAME/otree-game.git

# Or clone the main repo (for exploration)
git clone https://github.com/ignaciourbina/otree-game.git

cd otree-game
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (optional)
pip install pytest black isort mypy
```

### 4. Verify Installation

```bash
# Test formal model
python -c "from formal_model.jones_models import SimpleAIGrowthRiskModel; print(SimpleAIGrowthRiskModel().summary())"

# Test oTree server
cd otree
otree devserver

# Open http://localhost:8000 in browser
```

## IDE Configuration

### VS Code (Recommended)

#### Recommended Extensions

```json
// .vscode/extensions.json
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "ms-python.isort",
        "batisteo.vscode-django",
        "redhat.vscode-yaml"
    ]
}
```

#### Settings

```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter"
    },
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["testing"]
}
```

#### Launch Configuration

```json
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "oTree Server",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/.venv/bin/otree",
            "args": ["devserver"],
            "cwd": "${workspaceFolder}/otree",
            "console": "integratedTerminal"
        },
        {
            "name": "Run Simulations",
            "type": "python",
            "request": "launch",
            "module": "simulations.runner",
            "cwd": "${workspaceFolder}",
            "console": "integratedTerminal"
        }
    ]
}
```

### PyCharm

1. Open project folder
2. Configure Python interpreter: `.venv/bin/python`
3. Mark `otree/` as Sources Root
4. Enable Django support (optional)

## Project Configuration

### Python Path Setup

The project uses relative imports. Ensure proper module resolution:

```bash
# Add to .bashrc or .zshrc for persistent access
export PYTHONPATH="${PYTHONPATH}:/path/to/otree-game"
```

Or in Python:

```python
import sys
sys.path.insert(0, '/path/to/otree-game')
```

### Environment Variables

Create `.env` file for local development:

```bash
# .env (not committed to git)
OTREE_ADMIN_PASSWORD=devpassword
DEBUG=1
PYTHONDONTWRITEBYTECODE=1
```

## Development Tools

### Code Formatting

```bash
# Format with Black
black formal_model/ otree/ simulations/ testing/

# Sort imports
isort formal_model/ otree/ simulations/ testing/
```

### Type Checking

```bash
# Run mypy
mypy formal_model/ --ignore-missing-imports
```

### Linting

```bash
# Run flake8
flake8 formal_model/ otree/ simulations/ --max-line-length=100
```

## Database Management

### Reset Database

```bash
cd otree
otree resetdb  # Clears all data
```

### Migrate (if models change)

oTree handles migrations automatically on `devserver` startup.

## Running Tests

### Unit Tests

```bash
# From project root
python -m pytest testing/ -v
```

### Bot Tests

```bash
# Run bot sessions
python testing/run_ai_growth_risk_bots.py --iterations 5
```

### Integration Tests

```bash
# Start server in background
cd otree && otree devserver &

# Run browser tests (if implemented)
python -m pytest testing/integration/ -v
```

## Troubleshooting

### Common Issues

<details>
<summary><strong>ImportError: No module named 'otree'</strong></summary>

Ensure virtual environment is activated:
```bash
source .venv/bin/activate
pip install -r requirements.txt
```
</details>

<details>
<summary><strong>Database locked</strong></summary>

Stop any running oTree processes:
```bash
pkill -f otree
cd otree && otree resetdb
```
</details>

<details>
<summary><strong>Port 8000 in use</strong></summary>

Use alternative port:
```bash
otree devserver 8001
```

Or kill existing process:
```bash
lsof -ti:8000 | xargs kill
```
</details>

<details>
<summary><strong>Template not found</strong></summary>

Ensure working directory is correct:
```bash
cd otree
otree devserver
```
</details>

## Useful Commands

```bash
# Start development server
cd otree && otree devserver

# Reset database
cd otree && otree resetdb

# Run simulations
python -m simulations.runner

# Run bot tests
python testing/run_ai_growth_risk_bots.py

# Format code
black . && isort .

# Type check
mypy formal_model/
```

## Directory Permissions

Ensure write access to:
- `otree/db.sqlite3` (database)
- `out/` (simulation outputs)
- `.venv/` (virtual environment)

```bash
chmod -R u+w otree/ out/ .venv/
```

## Next Steps

- **[Contributing Guide →](./contributing.md)** — Submit your first PR
- **[Testing Guide →](./testing.md)** — Write and run tests
- **[Architecture →](../architecture/README.md)** — Understand the system
