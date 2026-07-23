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


def decide(score_diff, stamina, urgency, threat_level, possession, rating, position, minutes_left, has_yellow_card, team_red_cards, opp_red_cards):
    # Choose an action following a strict priority order:
    # 1. Fatigue overrides everything else.
    # 2. Being under threat with no ball forces a defensive response.
    # 3. Endgame tactics (final 10 minutes).
    # 4. Otherwise, urgency drives how aggressively the team plays.
    # 5. If none of the above apply, a highly-rated player on the ball tries something special.

    actions = []
    
    # ---------------------------------------------------------
    # CONSTRAINT VARIABLES (Modified by Layers 1 & 2)
    # ---------------------------------------------------------
    can_sprint = True
    can_tackle = True
    team_formation = "Balanced" 

    # ---------------------------------------------------------
    # LAYER 1: META / HEALTH (Sets Physical/Disciplinary Limits)
    # ---------------------------------------------------------
    if has_yellow_card:
        actions.append("Play Cautious - Already have 1 Yellow Card")
        can_tackle = False  # OVERRIDE: Prevents sliding tackles in Layer 3

    if stamina < 20:
        actions.append("Request Substitution")
        can_sprint = False  # OVERRIDE: Prevents aggressive sprints/presses in Layer 3
    
    # ---------------------------------------------------------
    # LAYER 2: TEAM FORMATION TACTICS 
    # ---------------------------------------------------------
    if minutes_left <= 10:
        if score_diff <= 0:  
            team_formation = "Rush"
            actions.append("TEAM FORMATION: 3-4-3 (Rush - High Press)")
        elif team_red_cards > opp_red_cards:
            team_formation = "Defensive"
            actions.append("TEAM FORMATION: 5-4-0 (Defensive - Compact Formation)") 
        else:  
            team_formation = "Defensive"
            actions.append("TEAM FORMATION: 4-2-3-1 (Defend - Hold Possession)")
            
    elif team_red_cards < opp_red_cards:
        team_formation = "Aggressive"
        actions.append("TEAM FORMATION: 4-3-3 (Aggressive - Exploit Numerical Advantage)")      

    elif team_red_cards > opp_red_cards:
        team_formation = "Defensive"
        actions.append("TEAM FORMATION: 4-4-1 (Defensive - Compact Formation)")

    elif urgency >= 3.5:
        team_formation = "Rush"
        actions.append("TEAM FORMATION: 3-4-3 (Rush - High Press)")
    
    else:
        team_formation = "Balanced"
        actions.append("TEAM FORMATION: 4-4-2 (Balanced - Normal Play)")
    
    # ---------------------------------------------------------
    # LAYER 3: INDIVIDUAL IMMEDIATE ACTIONS 
    # ---------------------------------------------------------
    # Off-Ball Actions
    if not possession:
        if threat_level > 4:
            if not can_tackle:
                actions.append("Defend - Jockey opponent (Cannot risk sliding tackle)")
            elif not can_sprint:
                actions.append("Defend - Hold position (Too tired to track back fast)")
            else:
                actions.append("Defend - Track Back Aggressively")
        else:
            actions.append("Hold Defensive Formation")
    
    # On-Ball Actions
    else:
        if position.lower() == "striker":
            if team_formation == "Defensive":
                actions.append("Hold up play and wait for support")
            elif not can_sprint:
                actions.append("Attempt quick shot or pass (Too tired to run)")
            else:
                actions.append("Attempt goal")
        
        elif position.lower() == "defender":
            if threat_level >= 3 or team_formation == "Defensive":
                actions.append("Clear long")
            else:
                actions.append("Attempt safe pass")
        
        elif position.lower() == "winger":
            if team_formation == "Defensive":
                actions.append("Pass backwards to retain possession")
            elif not can_sprint:
                actions.append("Attempt short pass (Too tired to cross or dribble)")
            elif rating > 65:
                actions.append("Sprint and attempt cross")
            else:
                actions.append("Attempt dribble")
        
        elif position.lower() == "midfielder":
            if team_formation == "Defensive":
                actions.append("Hold possession and recycle ball")
            elif rating > 75 and can_sprint:
                actions.append("Push forward and attempt goal")
            else:
                actions.append("Attempt pass")
        
        elif position.lower() == "goalkeeper":
            if urgency >= 4 or team_formation == "Rush":
                actions.append("Boot the ball downfield")
            else:
                actions.append("Pass to nearby player")
    
    return actions


def act(actions):
    # Perform the chosen action. Here that just means printing it.
    print(f"Actions: {actions}")


def record(state, actions):
    # Append the full state and the chosen action to log.txt for later review.
    # with open(LOG_PATH, "a") as log_file:
        # log_file.write(f"State: {state} --> Action: {action}\n")
    
    with open("fifa_agent/log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"State: {state} --> Actions: {actions}\n")
