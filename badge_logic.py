def assign_score_badge(score):
    if score >= 9:
        return "Gold"
    elif score >= 7:
        return "Silver"
    elif score >= 5:
        return "Bronze"
    else:
        return "No Badge"

def assign_overall_badge(avg_score):
    if 3 <= avg_score <= 5:
        return "Bronze"
    elif 6 <= avg_score <= 8:
        return "Silver"
    elif 9 <= avg_score <= 10:
        return "Gold"
    else:
        return "No Badge"
