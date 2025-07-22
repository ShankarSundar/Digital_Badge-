import streamlit as st
import json
from badge_logic import score_to_badge
from database import init_db, insert_user, get_quiz_leaderboard, get_overall_leaderboard
import pandas as pd
import os

st.set_page_config(page_title="Knowledge Check Quiz", layout="centered")
st.title("📘 Knowledge Check Quiz")

init_db()

# Initialize session state
for key in ["name", "email", "quiz_submitted", "overall_calculated"]:
    if key not in st.session_state:
        st.session_state[key] = False if "_calculated" in key or "_submitted" in key else ""

# -------------------- LOGIN SECTION -------------------- #
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

# -------------------- DISPLAY QUIZ RESULT -------------------- #
if st.session_state.quiz_submitted and not st.session_state.overall_calculated:
    st.success(f"✅ Your Quiz Score: {st.session_state.quiz_score}/10")
    st.image(f"assets/{st.session_state.quiz_badge.lower()}.png", width=150, caption=f"🏅 Quiz Badge: {st.session_state.quiz_badge}")

    st.number_input("Enter community contribution score (0-10):", min_value=0, max_value=10, key="community_score")

    if st.button("Calculate Overall Badge"):
        avg_score = (st.session_state.quiz_score + st.session_state.community_score) / 2
        st.session_state.overall_score = avg_score

        st.session_state.community_score = community_score
        st.session_state.overall_score = avg_score
        st.session_state.overall_badge = overall_badge
        st.session_state.overall_calculated = True
        st.rerun()

# -------------------- DISPLAY OVERALL + LEADERBOARDS -------------------- #
if st.session_state.overall_calculated:
    st.info(f"📊 Overall Score: {st.session_state.overall_score:.1f}/10")
    st.image(f"assets/{st.session_state.overall_badge.lower()}.png", width=150, caption=f"🏅 Overall Badge: {st.session_state.overall_badge}")

    # Save result to DB
    insert_user(
        st.session_state.name,
        st.session_state.email,
        st.session_state.quiz_score,
        st.session_state.quiz_badge,
        st.session_state.community_score,
        st.session_state.overall_score,
        st.session_state.overall_badge
    )

    # Leaderboards
    st.markdown("---")
    st.subheader("📈 Quiz Leaderboard")
    st.dataframe(get_quiz_leaderboard())

    st.markdown("---")
    st.subheader("🏆 Overall Leaderboard")
    st.dataframe(get_overall_leaderboard())

    # Save to Excel
    df_all = get_overall_leaderboard()
    df_all.to_excel("quiz_results.xlsx", index=False)

    if st.button("End"):
        st.success("✅ Quiz completed. You can now close the tab.")
