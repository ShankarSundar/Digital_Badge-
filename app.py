import streamlit as st
import json
from database import init_db, insert_user, get_quiz_leaderboard, get_overall_leaderboard
from badge_logic import score_to_badge
import os

# Initialize DB
init_db()

# App layout
st.set_page_config(page_title="Digital Badge System", layout="centered")
st.title("📘 Knowledge Check Quiz")

# Get query params to route pages
query_params = st.query_params
route = query_params.get("page", "quiz").lower()

if route == "quiz":
    st.header("📄 Quiz Questions")

    # Step 1: User Authentication
    if "email" not in st.session_state:
        email = st.text_input("Enter your university email:")
        if st.button("Start Quiz"):
            if email and "@university" in email:
                st.session_state.email = email
            else:
                st.warning("Please enter a valid university email (e.g., yourname@university.edu)")
        st.stop()

    email = st.session_state.email

    # Step 2: Load questions
    try:
        with open("questions.json", "r") as f:
            questions = json.load(f)
    except FileNotFoundError:
        st.error("Quiz file not found.")
        st.stop()

    user_answers = []
    score = 0
    all_answered = True

    st.subheader("📝 Quiz Questions")

    for idx, q in enumerate(questions):
        selected = st.radio(
            q["question"],
            q["options"],
            index=None,
            key=f"q_{idx}"
        )
        if selected is None:
            all_answered = False
        user_answers.append({"selected": selected, "correct": q["answer"]})

    if st.button("Submit Quiz"):
        if not all_answered:
            st.warning("❗ Please answer all questions before submitting.")
            st.stop()
        else:
            for ans in user_answers:
                if ans["selected"] == ans["correct"]:
                    score += 1

            # 🎯 Quiz badge
            quiz_badge = score_to_badge(score)
            st.success(f"✅ Your Quiz Score: {score}/10")
            st.image(f"assets/{quiz_badge.lower()}.png", width=150, caption=f"🏅 Quiz Badge: {quiz_badge}")

            # 📥 Community input
            community_score = st.number_input("Enter community contribution score (0-10):", min_value=0, max_value=10)

            if st.button("Calculate Overall Badge"):
                avg_score = (score + community_score) / 2
                overall_badge = score_to_badge(avg_score)
                st.info(f"📊 Overall Score: {avg_score:.1f}/10")
                st.image(f"assets/{overall_badge.lower()}.png", width=150, caption=f"🏅 Overall Badge: {overall_badge}")

                # Save results
                insert_user(email, score, quiz_badge, community_score, avg_score, overall_badge)

                st.markdown("---")
                st.subheader("📈 Quiz Leaderboard")
                st.dataframe(get_quiz_leaderboard())

                st.markdown("---")
                st.subheader("🏆 Overall Leaderboard")
                st.dataframe(get_overall_leaderboard())

elif route == "leaderboard":
    st.header("📊 Leaderboards")
    st.subheader("📈 Quiz Leaderboard")
    st.dataframe(get_quiz_leaderboard())

    st.subheader("🏆 Overall Leaderboard")
    st.dataframe(get_overall_leaderboard())

else:
    st.error("Page not found.")
