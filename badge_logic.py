def score_to_badge(score):
    if 3 <= score <= 5:
        return "Bronze"
    elif 6 <= score <= 8:
        return "Silver"
    elif 9 <= score <= 10:
        return "Gold"
    else:
        return "No Badge"
