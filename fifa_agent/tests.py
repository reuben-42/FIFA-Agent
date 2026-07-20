# tests.py — runs a handful of fixed scenarios through the full agent pipeline

from state import get_score_state, get_time_state, get_threat_level, get_urgency
from agent import decide, act, record

# Three scenarios covering an easy match, a balanced match, and a high-pressure match.
# Plus an endgame scenario to test late-game tactics.
SCENARIOS = {
    "Easy": {
        "goal_gap": 2, "minutes_left": 30, "stamina": 80,
        "possession": True, "rating": 85, "position": "Winger", "rating_gap": -10
    },
    "Balanced": {
        "goal_gap": 0, "minutes_left": 50, "stamina": 60,
        "possession": True, "rating": 75, "position": "Midfielder", "rating_gap": 5
    },
    "High Pressure": {
        "goal_gap": -2, "minutes_left": 85, "stamina": 25,
        "possession": False, "rating": 85, "position": "Defender", "rating_gap": 15
    },
    "Endgame Losing": {
        "goal_gap": -1, "minutes_left": 8, "stamina": 45,
        "possession": True, "rating": 82, "position": "Striker", "rating_gap": 2
    },
    "Endgame Winning": {
        "goal_gap": 2, "minutes_left": 5, "stamina": 50,
        "possession": True, "rating": 79, "position": "Midfielder", "rating_gap": -5
    },
}


def run_tests():
    # Run every scenario through score/time/threat/urgency -> decide -> act -> record,
    # printing a clean readable line for each one.
    for name, raw_state in SCENARIOS.items():
        score_state = get_score_state(raw_state["goal_gap"])
        time_state = get_time_state(raw_state["minutes_left"])
        threat_level = get_threat_level(raw_state["rating_gap"])
        urgency = get_urgency(score_state, time_state, threat_level, raw_state["possession"])

        action = decide(
            raw_state["goal_gap"],
            raw_state["stamina"], 
            urgency, 
            threat_level,
            raw_state["possession"], 
            raw_state["rating"], 
            raw_state["position"],
            raw_state["minutes_left"]
        )

        print(f"\n[SCENARIO: {name}] State: {raw_state} --> Action: {action}")
        act(action)
        record(raw_state, action)


if __name__ == "__main__":
    run_tests()
