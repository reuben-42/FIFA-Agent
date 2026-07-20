# agent.py — the sense -> decide -> act -> record loop

# import os

# LOG_PATH = os.path.join(os.path.dirname(__file__), "log.txt")


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


def decide(score_diff, stamina, urgency, threat_level, possession, rating, position, minutes_left):
    # Choose an action following a strict priority order:
    # 1. Fatigue overrides everything else.
    # 2. Being under threat with no ball forces a defensive response.
    # 3. Endgame tactics (final 10 minutes).
    # 4. Otherwise, urgency drives how aggressively the team plays.
    # 5. If none of the above apply, a highly-rated player on the ball tries something special.
    
    actions = []

    # ---------------------------------------------------------
    # LAYER 1: META / HEALTH ACTIONS:
    # ---------------------------------------------------------
    if stamina < 20:
        actions.append("Request Substitution")
    
    # ---------------------------------------------------------
    # LAYER 2: TEAM FORMATION TACTICS:
    # ---------------------------------------------------------
    if minutes_left <= 10:
        if score_diff <= 0:  # Losing or tied -> be aggressive
            actions.append("TEAM FORMATION: Rush - High Press")
        else:  # Winning comfortably -> consolidate
            actions.append("TEAM FORMATION: Defend - Hold Possession")
    
    elif urgency >= 3.5:
        actions.append("TEAM FORMATION: Rush - High Press")
    
    else:
        actions.append("TEAM FORMATION: Balanced - Normal Play")
    
    # ---------------------------------------------------------
    # LAYER 3: INDIVIDUAL IMMEDIATE ACTIONS:
    # ---------------------------------------------------------
    if not possession:
        # Off-Ball Actions
        if threat_level > 4:
            actions.append("Defend - Track Back")
        else:
            actions.append("Hold Defensive Formation")
    
    else:
        # On-Ball Actions
        if position.lower() == "striker":
            actions.append("Attempt goal")
        
        elif position.lower() == "defender":
            if threat_level >= 3:
                actions.append("Clear long")
            else:
                actions.append("Attempt safe pass")
        
        elif position.lower() == "winger":
            if rating > 65:
                actions.append("Attempt cross")
            else:
                actions.append("Attempt dribble")
        
        elif position.lower() == "midfielder":
            if rating > 75:
                actions.append("Attempt goal")
            else:
                actions.append("Attempt pass")
        
        elif position.lower() == "goalkeeper":
            if urgency >= 4:
                actions.append("Boot the ball downfield")
            else:
                actions.append("Pass to nearby player")
    
    return actions


def act(action):
    # Perform the chosen action. Here that just means printing it.
    print(f"Action: {action}")


def record(state, action):
    # Append the full state and the chosen action to log.txt for later review.
    # with open(LOG_PATH, "a") as log_file:
        # log_file.write(f"State: {state} --> Action: {action}\n")
    
    with open("fifa_agent/log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"State: {state} --> Action: {action}\n")
