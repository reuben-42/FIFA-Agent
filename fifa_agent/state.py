# state.py — converts raw match numbers into the small 1-5 scales the agent reasons over


def get_score_state(goal_gap):
    # Convert the real goal difference (own goals - opponent goals) into a 1-5 scale.
    # 1 = comfortably winning, 5 = badly losing.
    if goal_gap > 3:
        return 1
    elif goal_gap >= 1:
        return 2
    elif goal_gap == 0:
        return 3
    elif goal_gap >= -3:
        return 4
    else:
        return 5


def get_time_state(minutes_left):
    # Convert real minutes left in the match into a 1-5 scale.
    # 1 = plenty of time left, 5 = final moments of the game.
    if minutes_left <= 5:
        return 5
    elif minutes_left <= 20:
        return 4
    elif minutes_left <= 45:
        return 3
    elif minutes_left <= 75:
        return 2
    else:
        return 1


def get_threat_level(rating_gap):
    # Convert the opponent's rating advantage (opponent rating - own rating) into a 1-5 threat scale.
    # 1 = opponent is much weaker, 5 = opponent is much stronger.
    if rating_gap <= -20:
        return 1
    elif rating_gap <= -5:
        return 2
    elif rating_gap <= 5:
        return 3
    elif rating_gap <= 20:
        return 4
    else:
        return 5


def get_urgency(score_state, time_state, threat_level, possession):
    # Combine score, time and threat into a single urgency score.
    # With the ball, threat doesn't matter as much as controlling score/clock.
    # Without the ball, threat level is factored in since danger is more immediate.
    if possession:
        return 0.5 * score_state + 0.5 * time_state
    else:
        return 0.35 * score_state + 0.30 * threat_level + 0.35 * time_state
