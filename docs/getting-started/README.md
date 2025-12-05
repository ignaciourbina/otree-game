# Getting Started

Welcome! This guide will help you set up the oTree AI Growth-Risk Experiments project and run your first experiment.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** (3.10+ recommended)
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- A modern web browser (Chrome, Firefox, Safari, or Edge)

## Quick Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ignaciourbina/otree-game.git
cd otree-game
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
cd otree
otree devserver
```

Open [http://localhost:8000](http://localhost:8000) in your browser. You should see the oTree admin interface.

## Next Steps

| Guide | Description |
|-------|-------------|
| [Quick Start](./quickstart.md) | 5-minute guide to running your first session |
| [Development Setup](../development/setup.md) | Full development environment configuration |
| [First Experiment](../experiments/first-experiment.md) | Detailed experiment walkthrough |

## Troubleshooting

### Common Issues

<details>
<summary><strong>ModuleNotFoundError: No module named 'otree'</strong></summary>

Ensure you've activated the virtual environment:
```bash
source .venv/bin/activate
```
</details>

<details>
<summary><strong>Address already in use</strong></summary>

Another process is using port 8000. Either stop it or use a different port:
```bash
otree devserver 8001
```
</details>

<details>
<summary><strong>Database errors on startup</strong></summary>

Reset the database:
```bash
otree resetdb
```
</details>

## Documentation Map

```
docs/
├── getting-started/     ◄── You are here
│   ├── README.md
│   └── quickstart.md
├── architecture/
├── api/
├── experiments/
└── development/
```
