# tests.py — runs a handful of fixed scenarios through the full agent pipeline

from state import get_score_state, get_time_state, get_threat_level, get_urgency
from agent import decide, act, record

# Three scenarios covering an easy match, a balanced match, and a high-pressure match.
# Plus an endgame scenario to test late-game tactics.
"""
SCENARIOS1 = {
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
"""
"""
SCENARIOS2 = {
    "Easy": {
        "goal_gap": 2, "minutes_left": 30, "stamina": 80,
        "possession": True, "rating": 85, "position": "Winger", "rating_gap": -10,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 1
    },
    "Balanced": {
        "goal_gap": 0, "minutes_left": 50, "stamina": 60,
        "possession": True, "rating": 75, "position": "Midfielder", "rating_gap": 5,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 0
    },
    "High Pressure": {
        "goal_gap": 1, "minutes_left": 85, "stamina": 25,
        "possession": False, "rating": 85, "position": "Defender", "rating_gap": 15,
        "has_yellow_card": True, "team_red_cards": 1, "opp_red_cards": 0
    },
    "Endgame Losing": {
        "goal_gap": -1, "minutes_left": 8, "stamina": 45,
        "possession": True, "rating": 82, "position": "Striker", "rating_gap": 2,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 0
    },
    "Endgame Winning": {
        "goal_gap": 2, "minutes_left": 5, "stamina": 15, 
        "possession": True, "rating": 79, "position": "Midfielder", "rating_gap": -5,
        "has_yellow_card": False, "team_red_cards": 1, "opp_red_cards": 0
    },
}
"""

SCENARIOS = {
    "Easy (Open Play)": {
        "goal_gap": 2, "minutes_left": 30, "stamina": 80,
        "possession": True, "rating": 85, "position": "Winger", "rating_gap": -10,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 1,
        "set_piece_type": "None", "set_piece_zone": "None"
    },
    "Balanced (Open Play)": {
        "goal_gap": 0, "minutes_left": 50, "stamina": 60,
        "possession": True, "rating": 75, "position": "Midfielder", "rating_gap": 5,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 0,
        "set_piece_type": "None", "set_piece_zone": "None"
    },
    "High Pressure (Defending Free-kick)": {
        "goal_gap": -2, "minutes_left": 85, "stamina": 15,
        "possession": False, "rating": 85, "position": "Defender", "rating_gap": 15,
        "has_yellow_card": True, "team_red_cards": 1, "opp_red_cards": 0,
        "set_piece_type": "Free-kick", "set_piece_zone": "Defending"
    },
    "Endgame Losing (Attacking Corner)": {
        "goal_gap": -1, "minutes_left": 8, "stamina": 45,
        "possession": True, "rating": 82, "position": "Striker", "rating_gap": 2,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 0,
        "set_piece_type": "Corner", "set_piece_zone": "Attacking"
    },
    "Endgame Winning (Open Play)": {
        "goal_gap": 2, "minutes_left": 5, "stamina": 15, 
        "possession": True, "rating": 79, "position": "Midfielder", "rating_gap": -5,
        "has_yellow_card": False, "team_red_cards": 1, "opp_red_cards": 0,
        "set_piece_type": "None", "set_piece_zone": "None"
    },
    "The Decisive Penalty (Attacking)": {
        "goal_gap": 0, "minutes_left": 2, "stamina": 60, 
        "possession": True, "rating": 88, "position": "Striker", "rating_gap": 0,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 0,
        "set_piece_type": "Penalty", "set_piece_zone": "Attacking"
    },
    "Last Ditch Save (Defending Penalty)": {
        "goal_gap": 0, "minutes_left": 2, "stamina": 85, 
        "possession": False, "rating": 82, "position": "Goalkeeper", "rating_gap": 0,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 0,
        "set_piece_type": "Penalty", "set_piece_zone": "Defending"
    },
    "Deep Defensive Throw-in": {
        "goal_gap": 1, "minutes_left": 65, "stamina": 55, 
        "possession": True, "rating": 72, "position": "Defender", "rating_gap": 5,
        "has_yellow_card": False, "team_red_cards": 0, "opp_red_cards": 0,
        "set_piece_type": "Throw-in", "set_piece_zone": "Defending"
    }
}


def run_tests():
    # Run every scenario through score/time/threat/urgency -> decide -> act -> record,
    # printing a clean readable line for each one.
    for name, raw_state in SCENARIOS.items():
        score_state = get_score_state(raw_state["goal_gap"])
        time_state = get_time_state(raw_state["minutes_left"])
        threat_level = get_threat_level(raw_state["rating_gap"], raw_state["team_red_cards"])
        urgency = get_urgency(score_state, time_state, threat_level, raw_state["possession"], raw_state["opp_red_cards"])

        action = decide(
            raw_state["goal_gap"],
            raw_state["stamina"], 
            urgency, 
            threat_level,
            raw_state["possession"], 
            raw_state["rating"], 
            raw_state["position"],
            raw_state["minutes_left"],
            raw_state["has_yellow_card"],
            raw_state["team_red_cards"],
            raw_state["opp_red_cards"],
            raw_state["set_piece_type"],
            raw_state["set_piece_zone"]
        )

        print(f"\n[SCENARIO: {name}] State: {raw_state} --> Action: {action}")
        act(action)
        record(raw_state, action)


if __name__ == "__main__":
    run_tests()
