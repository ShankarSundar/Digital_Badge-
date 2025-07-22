def score_to_badge(score):
    if 9 <= score <= 10:
        return "Gold"
    elif 6 <= score <= 8:
        return "Silver"
    elif 3 <= score <= 5:
        return "Bronze"
    else:
        return "No Badge"