def sense(position, stamina, rating, possession, our_goals, opponent_goals, time_remaining, curr_ball_carrier_rating):
    score_diff = our_goals - opponent_goals

    if not possession:
        gap = curr_ball_carrier_rating - rating
        threat_level = calculate_threat_level(gap)
    else:
        threat_level = None
    
    if possession:
        urgency = 0.5 * score_diff_scale(score_diff) + 0.5 * time_remaining_scale(time_remaining)
    else:
        urgency = 0.35 * score_diff_scale(score_diff) + 0.30 * threat_level + 0.35 * time_remaining_scale(time_remaining)
    
    # Game State
    game_state = {
        "position": position,
        "stamina": stamina,
        "rating": rating,
        "possession": possession,
        "score_diff": score_diff,
        "time_remaining": time_remaining,
        "threat_level": threat_level,
        "urgency": urgency
    }

    return game_state


def decide(state):
    actions = []

    # Winning/Losing/Tie Tactics
    if state["time_remaining"] <= 10 and state["score_diff"] <= 0:  # Losing or Tie tactic
        actions.append("Rush (High Press)")
    elif state["time_remaining"] <= 10 and state["score_diff"] > 0: # Winning tactic
        actions.append("Defend (Hold Possession)")
    
    # Fatigue Management
    if state["stamina"] < 30:
        actions.append("Slow down, safe passes only")
    
    # Emergency Defense
    if state["threat_level"] is not None and state["threat_level"] > 4 and state["possession"] == False:
        actions.append("Defend, track back")
    
    # Star Player Attack
    if state["position"].lower() == "winger" and state["posession"] and state["rating"] > 80:
        actions.append("Attempt dribble or cross")
    elif state["position"].lower() == "striker" and state["possession"] and state["rating"] > 80:
        actions.append("Attempt goal")
    elif state["position"].lower() == "midfielder" and state["posession"] and state["rating"] > 80:
        actions.append("Attempt pass or goal")
    
    # Default State
    if not actions:  # if list is empty
        actions.append("Balanced: Maintain Position")
    
    return actions

def act(actions):
    for action in actions:
        print(f"Taking action: {action}")

def record(state, actions):
    print(f"Log: {state}  ->  {actions}")


def calculate_threat_level(gap):
    if gap <= -20:
        threat_level = 1
    elif -20 < gap <= -5:
        threat_level = 2
    elif -5 < gap <= 5:
        threat_level = 3
    elif 5 < gap <= 20:
        threat_level = 4
    else: # gap > 20
        threat_level = 5
    
    return threat_level

def score_diff_scale(score_diff):
    if score_diff < -3:
        score_diff_scale = 5
    elif -3 <= score_diff <= -1:
        score_diff_scale = 4
    elif score_diff == 0:
        score_diff_scale = 3
    elif 1 <= score_diff <= 3:
        score_diff_scale = 2
    else: # score_diff > 3
        score_diff_scale = 1
    
    return score_diff_scale

def time_remaining_scale(time_remaining):
    if 0 <= time_remaining <= 5:
        time_remaining_scale = 5
    elif 6 <= time_remaining <= 20:
        time_remaining_scale = 4
    elif 21 <= time_remaining <= 45:
        time_remaining_scale = 3
    elif 46 <= time_remaining <= 75:
        time_remaining_scale = 2
    else: # 76 <= time_remaining <= 90
        time_remaining_scale = 1
    
    return time_remaining_scale


if __name__ == "__main__":
    game_state = sense(position="Striker", stamina=90, rating=87, possession=True, our_goals=3, opponent_goals=2, time_remaining=90, curr_ball_carrier_rating=90)
    actions = decide(game_state)
    act(actions)
    record(game_state, actions)