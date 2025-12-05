# Your First Experiment

This guide walks you through running your first complete experiment session with the Cournot Shared Risk game.

## Prerequisites

- Completed [Quick Start](../getting-started/quickstart.md)
- Server running at `http://localhost:8000`
- At least 2 browser windows (or real participants)

## Step 1: Configure the Session

### Option A: Use Demo Mode (Testing)

1. Navigate to [http://localhost:8000](http://localhost:8000)
2. Click **"Demo"** in the navigation bar
3. Select **"Cournot Shared-Risk (6 rounds)"**
4. Click **"Create demo session"**

This creates a test session with 6 simulated participants.

### Option B: Create a Real Session

1. Navigate to [http://localhost:8000/sessions](http://localhost:8000/sessions)
2. Click **"Create new session"**
3. Configure:
   - **Session config**: Cournot Shared-Risk (6 rounds)
   - **Number of participants**: Even number (e.g., 6)
   - **Room name**: (optional) Link to a persistent room
4. Click **"Create"**

## Step 2: Distribute Participant Links

After creating the session, you'll see a list of participant links:

```
Participant 1: http://localhost:8000/InitializeParticipant/abc123
Participant 2: http://localhost:8000/InitializeParticipant/def456
...
```

### For Lab Sessions

- Print or display links via lab software (ORSEE, hroot)
- Use room URLs for persistent links across sessions

### For Testing

- Open multiple browser tabs/windows
- Use incognito/private mode for separate sessions

## Step 3: Run the Experiment

### Introduction Page

Participants see:
- Experiment overview
- Key mechanics (runtime choices, shared risk)
- Consent/understanding check

### Decision Page

Each round, participants:
1. View their treatment parameters (κ, ω, g)
2. Enter runtime choice (continuous slider or input)
3. Submit decision

### Wait Page

After decisions:
- Synchronized wait for partner
- Payoffs computed when both submit

### Results Page

Participants see:
- Their runtime choice
- Partner's runtime choice  
- Survival probability
- Consumption level
- Expected utility
- Token payout

## Step 4: Monitor Progress

### Admin View

The session admin page shows:
- Which page each participant is on
- Completion status per round
- Any stalled participants

Access via: [http://localhost:8000/SessionMonitor/[session_code]](http://localhost:8000)

### Key Metrics

| Metric | Location |
|--------|----------|
| Current round | Session monitor |
| Participant status | Session monitor |
| Treatment assignments | Data export |
| Decisions & payoffs | Data export |

## Step 5: Export Data

After all participants complete:

1. Go to **Data** tab in admin
2. Select your session
3. Click **"Download wide (CSV)"**

### Data Structure

The exported CSV includes:

| Column | Description |
|--------|-------------|
| `participant.code` | Unique participant ID |
| `player.runtime_choice` | Runtime decision |
| `player.survival` | Computed survival probability |
| `player.consumption` | Final consumption |
| `player.expected_utility` | Expected utility |
| `player.payoff` | Token payout |
| `group.treatment_label` | Treatment condition |
| `group.kappa` | Hazard curvature |
| `group.g1`, `group.g2` | Growth rates |
| `subsession.round_number` | Round number |

## Step 6: Analyze Results

### Quick Analysis in Python

```python
import pandas as pd

# Load data
df = pd.read_csv("cournot_shared_risk_2024-01-15.csv")

# Summary statistics by treatment
summary = df.groupby("group.treatment_label").agg({
    "player.runtime_choice": ["mean", "std"],
    "player.survival": "mean",
    "player.payoff": "mean",
})
print(summary)

# Plot runtime distributions
import matplotlib.pyplot as plt
df.boxplot(column="player.runtime_choice", by="group.treatment_label")
plt.title("Runtime by Treatment")
plt.ylabel("Runtime (years)")
plt.show()
```

### Key Analyses

1. **Treatment effects**: Compare mean runtimes across κ values
2. **Strategic substitutability**: Correlation between T₁ and T₂
3. **Learning**: Runtime trends across rounds
4. **Risk tolerance**: Relationship between choices and survival

## Troubleshooting

### Participant Stuck on Wait Page

**Cause**: Partner hasn't submitted  
**Solution**: Check partner's status; use admin advance if needed

### Missing Data

**Cause**: Participant dropped out  
**Solution**: Export partial data; exclude incomplete groups

### Wrong Number of Rounds

**Cause**: Unique pair constraint  
**Solution**: Ensure rounds ≤ N-1 for N participants

## Best Practices

### Before the Session

- [ ] Test with demo session
- [ ] Verify treatment parameters in `settings.py`
- [ ] Prepare participant instructions
- [ ] Set up payment processing

### During the Session

- [ ] Monitor progress in admin
- [ ] Have backup participants ready
- [ ] Note any technical issues

### After the Session

- [ ] Export data immediately
- [ ] Back up database
- [ ] Debrief participants
- [ ] Process payments

## Next Steps

- **[Session Configuration →](./session-config.md)** — Customize treatments
- **[Cournot Shared Risk API →](../api/cournot-shared-risk.md)** — Understand the model
