import streamlit as st
import json
from badge_logic import score_to_badge
from database import init_db, insert_user, get_quiz_leaderboard, get_community_leaderboard, get_overall_leaderboard
import pandas as pd
import os

st.set_page_config(page_title="Knowledge Check Quiz", layout="centered")
st.title("📘 Knowledge Check Quiz")

init_db()

# -------------------- SESSION INITIALIZATION -------------------- #
default_values = {
    "name": "",
    "email": "",
    "quiz_submitted": False,
    "overall_calculated": False,
    "quiz_score": 0,
    "quiz_badge": "",
    "community_score": 0,
    "community_badge": "",
    "overall_score": 0.0,
    "overall_badge": ""
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -------------------- LOGIN -------------------- #
if not st.session_state.name or not st.session_state.email:
    st.subheader("Login to Start Quiz")
    name = st.text_input("Enter your full name:")
    email = st.text_input("Enter your university email:")

    if st.button("Start Quiz"):
        if name.strip() != "" and "@" in email:
            st.session_state.name = name.strip()
            st.session_state.email = email.strip()
            st.rerun()
        else:
            st.warning("Please enter a valid name and email.")
    st.stop()

# -------------------- QUIZ SECTION -------------------- #
name = st.session_state.name
email = st.session_state.email

with open("questions.json", "r") as f:
    questions = json.load(f)

user_answers = []
all_answered = True

st.subheader("📝 Quiz Questions")

for i, q in enumerate(questions):
    st.markdown(f"**{q['question']}**")
    selected = st.radio("", q["options"], key=f"q{i}", index=None)
    if selected is None:
        all_answered = False
    user_answers.append({"selected": selected, "correct": q["answer"]})

# -------------------- SUBMIT QUIZ -------------------- #
if not st.session_state.quiz_submitted:
    if st.button("Submit Quiz"):
        if not all_answered:
            st.warning("❗ Please answer all questions before submitting.")
            st.stop()
        else:
            score = sum(1 for ans in user_answers if ans["selected"] == ans["correct"])
            quiz_badge = score_to_badge(score)
            st.session_state.quiz_score = score
            st.session_state.quiz_badge = quiz_badge
            st.session_state.quiz_submitted = True
            st.rerun()

# -------------------- DISPLAY QUIZ RESULT + LEADERBOARD -------------------- #
if st.session_state.quiz_submitted and not st.session_state.overall_calculated:
    st.success(f"✅ Your Quiz Score: {st.session_state.quiz_score}/10")
    st.image(f"assets/{st.session_state.quiz_badge.lower()}.png", width=150, caption=f"🏅 Quiz Badge: {st.session_state.quiz_badge}")

    st.markdown("---")
    st.subheader("📊 Quiz Leaderboard")
    quiz_df = get_quiz_leaderboard()
    st.dataframe(quiz_df)

    st.markdown("---")
    st.subheader("💬 Community Contribution")
    st.number_input("Enter community contribution score (0–10):", min_value=0, max_value=10, key="community_score")

    if st.button("Calculate Community Badge"):
        st.session_state.community_badge = score_to_badge(st.session_state.community_score)
        st.session_state.overall_score = (st.session_state.quiz_score + st.session_state.community_score) / 2
        st.session_state.overall_badge = score_to_badge(st.session_state.overall_score)
        st.session_state.overall_calculated = True
        st.rerun()

# -------------------- COMMUNITY RESULTS + COMMUNITY LEADERBOARD -------------------- #
if st.session_state.overall_calculated:
    st.info(f"💬 Community Score: {st.session_state.community_score}/10")
    st.image(f"assets/{st.session_state.community_badge.lower()}.png", width=150, caption=f"🏅 Community Badge: {st.session_state.community_badge}")

    insert_user(
        st.session_state.name,
        st.session_state.email,
        st.session_state.quiz_score,
        st.session_state.quiz_badge,
        st.session_state.community_score,
        st.session_state.community_badge,
        st.session_state.overall_score,
        st.session_state.overall_badge
    )

    st.markdown("---")
    st.subheader("👥 Community Leaderboard")
    community_df = get_community_leaderboard()
    st.dataframe(community_df)

    st.markdown("---")
    st.info("✅ Your full results have been saved. You may now close this tab or check the [📊 Public Leaderboard](https://your-app-url/leaderboard) for overall rankings.")

    # Save for external analysis
    all_df = get_overall_leaderboard()
    all_df.to_excel("user_submission.xlsx", index=False)

    if st.button("End"):
        st.success("✅ Quiz completed. You can now close the tab.")
