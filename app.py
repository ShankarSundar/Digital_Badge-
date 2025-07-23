from ace_tools import display_dataframe_to_user
import pandas as pd

# Recreate cleaned app.py content after code execution environment was reset
import json
from badge_logic import score_to_badge
from database import (
    insert_user,
    get_quiz_leaderboard,
    get_community_leaderboard,
    get_overall_leaderboard
)

st.set_page_config(page_title="Digital Badge Quiz", layout="centered")

# Login Section
st.title("🎓 Digital Badge Quiz")
st.markdown("Enter your university email to begin the quiz.")
name = st.text_input("Full Name")
email = st.text_input("University Email")

if name and email:
    st.success(f"Welcome {name}! Ready to begin the quiz.")

    # Quiz Questions (Demo)
    st.header("📝 Quiz")
    questions = {
        "What is the capital of France?": "Paris",
        "What is 2 + 2?": "4",
        "What is the boiling point of water?": "100",
        "What is the capital of Germany?": "Berlin",
        "What color is the sky on a clear day?": "Blue"
    }

    score = 0
    for q, ans in questions.items():
        user_ans = st.text_input(q, key=q)
        if user_ans.lower().strip() == ans.lower():
            score += 2

    if st.button("Submit Quiz"):
        quiz_score = score
        quiz_badge = score_to_badge(quiz_score)

        st.success(f"✅ Your quiz score: {quiz_score}")
        st.info(f"🏅 You earned the **{quiz_badge}** quiz badge!")

        # Insert initial quiz data
        insert_user(name, email, quiz_score, quiz_badge, 0, "", 0, "")

        st.markdown("---")
        st.subheader("🏅 Quiz Leaderboard")
        st.dataframe(get_quiz_leaderboard())

        # Community Score Input
        st.markdown("---")
        st.subheader("🌐 Enter Community Score")
        community_score = st.number_input("Community Score (0 to 10)", min_value=0, max_value=10, step=1)

        if st.button("Submit Community Score"):
            community_badge = score_to_badge(community_score)
            overall_score = round((quiz_score + community_score) / 2)
            overall_badge = score_to_badge(overall_score)

            # Update user with final scores
            insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge)

            st.success(f"🎯 Your overall score is {overall_score} and you earned the **{overall_badge}** badge!")

            # Show Community Leaderboard
            st.markdown("---")
            st.subheader("👥 Community Leaderboard")
            st.dataframe(get_community_leaderboard())

            # Show Final Summary + End Button
            st.markdown("---")
            st.subheader("🏆 Overall Leaderboard (Full view available on manager page)")
            df_all = get_overall_leaderboard()
            st.dataframe(df_all)

            if st.button("End"):
                st.success("✅ Quiz completed. You can now close the tab.")

