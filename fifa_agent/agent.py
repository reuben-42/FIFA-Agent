# agent.py — the sense -> decide -> act -> record loop

import os

LOG_PATH = os.path.join(os.path.dirname(__file__), "log.txt")


def sense():
    # Return a raw game-state dictionary describing what the agent currently observes.
    # In a real integration this would read live match data instead of fixed values.
    return {
        "stamina": 75,
        "goal_gap": -1,
        "minutes_left": 82,
        "rating_gap": 10,
        "possession": False,
        "rating": 85,
        "position": "Winger"
    }


def decide(stamina, urgency, threat_level, possession, rating, position):
    # Choose an action following a strict priority order:
    # 1. Fatigue overrides everything else.
    # 2. Being under threat with no ball forces a defensive response.
    # 3. Otherwise, urgency drives how aggressively the team plays.
    # 4. If none of the above apply, a highly-rated player on the ball tries something special.
    if stamina < 30:
        return "Conservative — safe passes only"
    elif threat_level > 4 and possession == False:
        return "Defend — track back"
    elif urgency >= 3.5:
        return "Rush — High Press"
    elif urgency >= 2:
        return "Balanced — normal play"

    if possession == True and rating > 80:
        if position == "Winger":
            return "Attempt dribble or cross"
        elif position == "Striker":
            return "Attempt goal"
        elif position == "Midfielder":
            return "Attempt pass or goal"

    return "Hold Possession"


def act(action):
    # Perform the chosen action. Here that just means printing it.
    print(f"Action: {action}")


def record(state, action):
    # Append the full state and the chosen action to log.txt for later review.
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"State: {state} --> Action: {action}\n")
