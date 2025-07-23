def score_to_badge(score):
    if score >= 9:
        return "Gold"
    elif score >= 6:
        return "Silver"
    elif score >= 3:
        return "Bronze"
    else:
        return "No Badge"
