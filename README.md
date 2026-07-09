# FIFA/EA FC 26 Baseline Agent

A sophisticated AI agent for FIFA/EA FC 26 that makes intelligent in-game decisions based on real-time match state. The agent uses a data-driven approach to balance offensive, defensive, and tactical decisions based on stamina, score, time, and player ratings.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Configuration & Parameters](#configuration--parameters)
- [Test Scenarios](#test-scenarios)
- [Output & Logging](#output--logging)

---

## Project Overview

This project implements a **multi-module AI decision-making system** for FIFA/EA FC 26 gameplay. The agent observes the current game state and decides on the best action (offensive, defensive, or balanced play) based on:

- **Player stamina** (0-100)
- **Score difference** (own goals - opponent goals)
- **Time remaining** (0-90 minutes)
- **Player ratings** (individual skill level)
- **Player position** (Winger, Striker, Midfielder, Defender)
- **Ball possession** (whether the team has the ball)
- **Threat level** (opponent strength assessment)

The agent follows a **strict priority system** where critical factors (like fatigue) override other considerations, ensuring realistic and safe gameplay decisions.

---

## Architecture

The codebase is organized into **4 modular Python files** for clean separation of concerns:

```
fifa_agent/
├── agent.py          # Core decision-making logic (sense → decide → act → record)
├── state.py          # State conversion functions (raw match data → 1-5 scales)
├── main.py           # Entry point for running default scenarios
├── tests.py          # Pre-configured test scenarios
└── log.txt           # Generated at runtime (session logs)
```

### Module Responsibilities

| Module | Purpose | Key Functions |
|--------|---------|---|
| **agent.py** | Core agent loop and decision making | `sense()`, `decide()`, `act()`, `record()` |
| **state.py** | Converts raw match numbers into agent reasoning scales | `get_score_state()`, `get_time_state()`, `get_threat_level()`, `get_urgency()` |
| **main.py** | Entry point that runs default scenario + test suite | `run_default_scenario()` |
| **tests.py** | Pre-configured match scenarios for testing | `run_tests()`, `SCENARIOS` dict |

---

## How It Works

### 1. **Sense Phase** (`agent.py:sense()`)

The agent observes the current game state:

```python
{
    "stamina": 75,           # Player energy (0-100)
    "goal_gap": -1,          # Score difference (our goals - opponent goals)
    "minutes_left": 82,      # Time remaining in match
    "rating_gap": 10,        # Opponent strength vs player strength
    "possession": False,     # Do we have the ball?
    "rating": 85,            # Player's overall rating (0-100)
    "position": "Winger"     # Position on field
}
```

### 2. **State Conversion Phase** (`state.py`)

Raw match numbers are converted into **1-5 reasoning scales** for easier decision-making:

#### **Score State** (`get_score_state()`)
Converts goal difference into urgency:
- **1** = Winning by 3+ goals (comfortable)
- **2** = Winning by 1-3 goals
- **3** = Tied
- **4** = Losing by 1-3 goals
- **5** = Losing by 3+ goals (critical)

#### **Time State** (`get_time_state()`)
Converts remaining minutes into pressure:
- **1** = 76-90 minutes left (plenty of time)
- **2** = 46-75 minutes left
- **3** = 21-45 minutes left
- **4** = 6-20 minutes left
- **5** = 0-5 minutes left (final moments)

#### **Threat Level** (`get_threat_level()`)
Assesses opponent strength (rating gap):
- **1** = Opponent much weaker (gap ≤ -20)
- **2** = Opponent weaker (-20 to -5)
- **3** = Similar strength (-5 to +5)
- **4** = Opponent stronger (+5 to +20)
- **5** = Opponent much stronger (gap > +20)

#### **Urgency Score** (`get_urgency()`)
Combines score, time, and threat into a single 0-5 urgency metric:

**With possession (have the ball):**
```
Urgency = 0.5 × Score State + 0.5 × Time State
```

**Without possession (defending):**
```
Urgency = 0.35 × Score State + 0.30 × Threat Level + 0.35 × Time State
```

### 3. **Decision Phase** (`agent.py:decide()`)

The agent follows a **strict priority hierarchy** to choose an action:

```
Priority 1: FATIGUE CHECK
  └─ If stamina < 30 → "Conservative — safe passes only"

Priority 2: EMERGENCY DEFENSE
  └─ If threat_level > 4 AND no possession → "Defend — track back"

Priority 3: ENDGAME TACTICS (final 10 minutes)
  ├─ If losing/tied (urgency ≥ 3.5) → "Rush — High Press"
  └─ If winning (urgency < 3.5) → "Defend — Hold Possession"

Priority 4: URGENCY-DRIVEN PLAY
  ├─ If urgency ≥ 3.5 → "Rush — High Press"
  ├─ If urgency ≥ 2.0 → "Balanced — normal play"
  └─ Otherwise → Continue to Priority 5

Priority 5: STAR PLAYER MOVES (only with possession + rating > 80)
  ├─ If Winger → "Attempt dribble or cross"
  ├─ If Striker → "Attempt goal"
  ├─ If Midfielder → "Attempt pass or goal"
  └─ Otherwise → Continue to default

Default: "Hold Possession"
```

### 4. **Act Phase** (`agent.py:act()`)

The chosen action is executed and printed:
```
Action: Rush — High Press
```

### 5. **Record Phase** (`agent.py:record()`)

The state and action are logged to `log.txt` for later review:
```
State: {'stamina': 75, 'goal_gap': -1, ...} --> Action: Rush — High Press
```

---

## Installation & Setup

### Requirements
- **Python 3.7+**
- No external dependencies required (uses only standard library)

### Clone & Setup

```bash
# Clone the repository
git clone https://github.com/reuben-42/MSFT-Group4.git
cd MSFT-Group4

# Navigate to the agent folder
cd fifa_agent
```

---

## Usage

### Run All Scenarios (Default + Tests)

```bash
python main.py
```

**Output:**
```
[SCENARIO: Default] State: {...} --> Action: Balanced — normal play
Action: Balanced — normal play
[SCENARIO: Easy] State: {...} --> Action: Attempt dribble or cross
Action: Attempt dribble or cross
[SCENARIO: Balanced] State: {...} --> Action: Balanced — normal play
Action: Balanced — normal play
[SCENARIO: High Pressure] State: {...} --> Action: Conservative — safe passes only
Action: Conservative — safe passes only
[SCENARIO: Endgame Losing] State: {...} --> Action: Rush — High Press
Action: Rush — High Press
[SCENARIO: Endgame Winning] State: {...} --> Action: Defend — Hold Possession
Action: Defend — Hold Possession
```

### Run Only Test Scenarios

```bash
python tests.py
```

### Integrate Into Your Own Code

```python
from agent import sense, decide, act, record
from state import get_score_state, get_time_state, get_threat_level, get_urgency

# Get raw game state
raw_state = sense()

# Convert to reasoning scales
score_state = get_score_state(raw_state["goal_gap"])
time_state = get_time_state(raw_state["minutes_left"])
threat_level = get_threat_level(raw_state["rating_gap"])
urgency = get_urgency(score_state, time_state, threat_level, raw_state["possession"])

# Make decision
action = decide(
    raw_state["stamina"], urgency, threat_level,
    raw_state["possession"], raw_state["rating"], 
    raw_state["position"], raw_state["minutes_left"]
)

# Execute and record
act(action)
record(raw_state, action)
```

---

## Configuration & Parameters

### Adjustable Thresholds

All thresholds can be tuned in the respective files:

#### **Stamina Threshold** (`agent.py` line 28)
```python
if stamina < 30:  # Change to 40, 50, etc. for more/less conservative play
    return "Conservative — safe passes only"
```

#### **Threat Response Threshold** (`agent.py` line 31)
```python
elif threat_level > 4 and possession == False:  # Change > 4 to > 3 for earlier defense
    return "Defend — track back"
```

#### **Star Player Rating Threshold** (`agent.py` line 57)
```python
if possession == True and rating > 80:  # Change 80 to 75, 85, etc.
    return special_move
```

#### **Endgame Time Window** (`agent.py` line 35)
```python
elif minutes_left <= 10:  # Change to <= 15 for longer endgame phase
    # Endgame tactics
```

#### **Urgency Thresholds** (`agent.py` lines 44-46)
```python
elif urgency >= 3.5:      # Change for more/less aggressive play
    return "Rush — High Press"
elif urgency >= 2:        # Change for balanced play threshold
    return "Balanced — normal play"
```

#### **Score/Time/Threat Weighting** (`state.py` lines 54-56)
```python
if possession:
    return 0.5 * score_state + 0.5 * time_state
else:
    return 0.35 * score_state + 0.30 * threat_level + 0.35 * time_state
    # Adjust weights to emphasize different factors
```

---

## Test Scenarios

The agent is tested with **5 predefined scenarios** covering diverse match situations:

| Scenario | Goal Gap | Minutes Left | Stamina | Possession | Rating | Position | Rating Gap | Expected Action |
|----------|----------|--------------|---------|------------|--------|----------|------------|-----------------|
| **Easy** | +2 (winning) | 30 | 80 | Yes | 85 | Winger | -10 | Balanced - normal play |
| **Balanced** | 0 (tied) | 50 | 60 | Yes | 75 | Midfielder | 5 | Balanced - normal play |
| **High Pressure** | -2 (losing) | 85 | 25 | No | 85 | Defender | 15 | Conservative - safe passes only |
| **Endgame Losing** | -1 (losing) | 8 | 45 | Yes | 82 | Striker | 2 | Rush - High Press |
| **Endgame Winning** | +2 (winning) | 5 | 50 | Yes | 79 | Midfielder | -5 | Rush - High Press |

### Running Specific Tests

To run only test scenarios (without default):
```bash
python tests.py
```

To add your own scenario, edit `tests.py` and add to `SCENARIOS` dict:
```python
"My Custom Scenario": {
    "goal_gap": 1,
    "minutes_left": 45,
    "stamina": 70,
    "possession": True,
    "rating": 82,
    "position": "Striker",
    "rating_gap": -5
},
```

---

## Output & Logging

### Console Output

Each scenario prints a summary line:
```
[SCENARIO: Endgame Losing] State: {'stamina': 45, 'goal_gap': -1, 'minutes_left': 8, ...} --> Action: Rush — High Press
Action: Rush — High Press
```

### File Logging (`log.txt`)

All decisions are appended to `fifa_agent/log.txt` for analysis:
```
State: {'stamina': 75, 'goal_gap': -1, 'minutes_left': 82, 'rating_gap': 10, 'possession': False, 'rating': 85, 'position': 'Winger'} --> Action: Balanced — normal play
State: {'stamina': 80, 'goal_gap': 2, 'minutes_left': 30, 'rating_gap': -10, 'possession': True, 'rating': 85, 'position': 'Winger'} --> Action: Attempt dribble or cross
```

### Analyzing Logs

```python
# Quick Python script to parse logs
with open("log.txt", "r") as f:
    for line in f:
        print(line.strip())
```

---

## Key Features

✅ **Priority-Based Decision Making** — Critical factors (fatigue, threat) override less important ones

✅ **Scaled State Representation** — Complex match data simplified to 1-5 scales for intuitive reasoning

✅ **Endgame Tactics** — Special strategy for final 10 minutes (aggressive when losing, defensive when winning)

✅ **Star Player Exploitation** — High-rated players with possession attempt special moves

✅ **Modular Design** — Easy to test, extend, and integrate into other systems

✅ **Comprehensive Logging** — All decisions recorded for post-match analysis

✅ **Thoroughly Tested** — 5 diverse scenarios covering edge cases

---

## Future Enhancements

- [ ] Add more player positions (Defender, Center-back, Goalkeeper)
- [ ] Implement learning from match outcomes to adjust weights
- [ ] Add formation-based tactics (3-5-2, 4-2-3-1, etc.)
- [ ] Real-time integration with EA FC 26 API
- [ ] Multi-player coordination (team-wide decision making)
- [ ] Injury and substitution logic
- [ ] Set-piece handling (corners, free-kicks, penalties)
- [ ] Opponent style adaptation

---

## Team

**University Game AI Project** — MSFT Group 4

---

## License

This project is part of an academic assignment for Microsoft/university collaboration.

---

## Questions?

For questions or issues, refer to the comments in each module or check the test scenarios for usage examples.
