# main.py — entry point: runs one default scenario, then all test scenarios

from state import get_score_state, get_time_state, get_threat_level, get_urgency
from agent import sense, decide, act, record
import tests


def run_default_scenario():
    # Run the full sense -> decide -> act -> record loop for one default scenario.
    raw_state = sense()

    score_state = get_score_state(raw_state["goal_gap"])
    time_state = get_time_state(raw_state["minutes_left"])
    threat_level = get_threat_level(raw_state["rating_gap"])
    urgency = get_urgency(score_state, time_state, threat_level, raw_state["possession"])

    action = decide(
        raw_state["stamina"], 
        urgency, 
        threat_level,
        raw_state["possession"], 
        raw_state["rating"], 
        raw_state["position"],
        raw_state["minutes_left"]
    )

    print(f"[SCENARIO: Default] State: {raw_state} --> Action: {action}")
    act(action)
    record(raw_state, action)


if __name__ == "__main__":
    run_default_scenario()
    tests.run_tests()
