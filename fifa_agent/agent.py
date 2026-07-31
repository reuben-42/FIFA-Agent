# agent.py — the sense -> decide -> act -> record loop

from datetime import datetime


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


def decide(score_diff, stamina, urgency, threat_level, possession, rating, position, minutes_left, has_yellow_card, team_red_cards, opp_red_cards, set_piece_type, set_piece_zone):
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
    # LAYER 2: SET PIECE OVERRIDE (Interrupts normal play)
    # ---------------------------------------------------------

    #set_piece_type = ["None", "Penalty", "Corner", "Free-kick", "Throw-in"]
    #set_piece_zone = ["Attacking", "Midfield", "Defending"]

    if set_piece_type != "None":
        
        # OFFENSIVE SET PIECES (We have the ball)
        if possession == True:
            if set_piece_type == "Penalty":
                actions.append("SET PIECE: Attempt high-power placed shot")
                
            elif set_piece_type == "Corner":
                actions.append("SET PIECE: Whip cross into the penalty box")
                
            elif set_piece_type == "Free-kick":
                if set_piece_zone == "Attacking":
                    actions.append("SET PIECE: Attempt direct shot on goal")
                else:
                    actions.append("SET PIECE: Safe pass to retain possession")
                    
            elif set_piece_type == "Throw-in":
                if set_piece_zone == "Attacking" and urgency >= 3.5:
                    actions.append("SET PIECE: Attempt long throw into the box")
                else:
                    actions.append("SET PIECE: Safe short throw to nearest teammate")
                    
        # DEFENSIVE SET PIECES (Opponent has the ball)
        else:
            if set_piece_type == "Penalty":
                if position.lower() == "goalkeeper":
                    actions.append("SET PIECE: Dive to save penalty")
                else:
                    actions.append("SET PIECE: Stand outside the box and prepare to clear rebound")
                    
            elif set_piece_type == "Corner" or set_piece_type == "Free-kick":
                actions.append("SET PIECE: Mark your man and prepare to clear")
                
            elif set_piece_type == "Throw-in":
                actions.append("SET PIECE: Mark nearest opponent tightly")
        
        # Immediately return to prevent Layers 3 and 4 from running
        return actions
    
    # ---------------------------------------------------------
    # LAYER 3: TEAM FORMATION TACTICS 
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
    # LAYER 4: INDIVIDUAL IMMEDIATE ACTIONS 
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
                actions.append("Hold possession and recycle ball (pass the ball backward or sideways away from pressure)")
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


def record(scenario_name, state, actions):
    # Append the full state and the chosen action to log.txt for later review.
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""==================================================\nSCENARIO: {scenario_name.upper()}\nTimestamp: {timestamp}\n==================================================\n"""
    
    log_entry += "Observed Game State:\n"
    for key, val in state.items():
        log_entry += f"  - {key}: {val}\n"
        
    log_entry += "\nTriggered Actions:\n"
    for action in actions:
        log_entry += f"  > {action}\n"

    log_entry += "\nPass Rate:\n"
    if actions == state["expected_outcome"]:
        log_entry += f"  > 100% PASS RATE\n"
    else:
        log_entry += f"  - ERROR: Expected {state["expected_outcome"]}\n"
        
    log_entry += "==================================================\n\n\n"
    
    with open("fifa_agent/log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)

