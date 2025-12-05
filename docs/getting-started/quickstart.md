# Quick Start Guide

Get up and running with the oTree AI Growth-Risk Experiments in 5 minutes.

## TL;DR

```bash
# Clone and setup
git clone https://github.com/ignaciourbina/otree-game.git
cd otree-game
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the server
cd otree
otree devserver

# Open http://localhost:8000 in your browser
```

## Step-by-Step

### 1. Installation (2 minutes)

```bash
# Clone the repository
git clone https://github.com/ignaciourbina/otree-game.git
cd otree-game

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the Server (30 seconds)

```bash
cd otree
otree devserver
```

You should see:
```
Open your browser to http://localhost:8000/
To run a study, visit:
http://localhost:8000/demo
```

### 3. Run a Demo Session (2 minutes)

1. Open [http://localhost:8000](http://localhost:8000) in your browser
2. Click **"Demo"** in the navigation
3. Select **"Cournot Shared-Risk (6 rounds)"**
4. Click **"Create demo session"**
5. Open the participant links to interact with the experiment

### 4. Explore the Admin Interface

- **Sessions**: View and manage experiment sessions
- **Demo**: Quick-start demo sessions for testing
- **Data**: Export participant data as CSV
- **Rooms**: Set up persistent participant links

## What's Next?

| Task | Guide |
|------|-------|
| Configure a real lab session | [Running Experiments →](../experiments/first-experiment.md) |
| Understand the formal model | [Formal Model API →](../api/formal-model.md) |
| Customize experiments | [API Reference →](../api/README.md) |
| Run simulations | [Simulations Guide →](../api/simulations.md) |

## Verify Everything Works

Run the automated tests to ensure your setup is complete:

```bash
# From the project root
python testing/run_ai_growth_risk_bots.py --iterations 2
```

Expected output:
```
INFO - Running iteration 1/2...
INFO - Session completed successfully
INFO - Running iteration 2/2...
INFO - Session completed successfully
```

## Project Structure Overview

```
otree-game/
├── otree/                    # 🎮 oTree experiments
│   ├── settings.py           #    Session configuration
│   ├── cournot_shared_risk/  #    Two-player game
│   └── ai_growth_risk/       #    Single-player game
├── formal_model/             # 🧮 Economic models
│   └── jones_models.py       #    Jones (2023) implementation
├── simulations/              # 📊 Batch experiments
└── testing/                  # 🧪 Automated tests
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+C` | Stop the development server |
| `Ctrl+R` | Refresh browser page |
| `F12` | Open browser developer tools |

---

**Need help?** Check the [Troubleshooting Guide](./README.md#troubleshooting) or open an issue on GitHub.
