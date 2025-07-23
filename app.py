import streamlit as st
import json
import random
from badge_logic import score_to_badge
from database import (
    insert_user,
    get_quiz_leaderboard,
    get_community_leaderboard,
    get_overall_leaderboard
)

st.set_page_config(page_title="Digital Badge Quiz", layout="centered")

st.title("🎓 Digital Badge Assessment")

# Session state
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "community_submitted" not in st.session_state:
    st.session_state.community_submitted = False

# User login
with st.form("login_form"):
    st.subheader("🔐 Login")
    user_name = st.text_input("Enter your name")
    user_email = st.text_input("Enter your university email")
    submitted_login = st.form_submit_button("Start Quiz")
    if submitted_login:
        if user_name and user_email:
            st.session_state.user_name = user_name
            st.session_state.user_email = user_email
        else:
            st.warning("Please enter both name and email to continue.")

if "user_name" in st.session_state and "user_email" in st.session_state:
    st.success(f"Welcome {st.session_state.user_name}! Start answering the quiz below.")

    # Load questions
    try:
        with open("questions.json", "r", encoding="utf-8") as f:
            questions = json.load(f)
        random.shuffle(questions)
        selected_questions = questions[:5]
    except Exception as e:
        st.error(f"Error loading questions: {e}")
        st.stop()

    # Quiz
    answers = {}
    with st.form("quiz_form"):
        st.subheader("📝 Quiz")
        for i, q in enumerate(selected_questions):
            st.markdown(f"**Q{i+1}: {q['question']}**")
            options = q.get("options", [])
            if options:
                answers[q["question"]] = st.radio("", options, key=f"q{i}")
        submitted_quiz = st.form_submit_button("Submit Quiz")

    if submitted_quiz and not st.session_state.quiz_submitted:
        score = 0
        for q in selected_questions:
            user_ans = answers[q["question"]]
            if user_ans == q["answer"]:
                score += 1
        quiz_badge = score_to_badge(score)
        st.success(f"✅ You scored {score}/5. Your Quiz Badge: 🏅 {quiz_badge}")
        insert_user(st.session_state.user_name, st.session_state.user_email, score, quiz_badge, 0, "", 0, "")
        st.session_state.quiz_submitted = True

        st.markdown("---")
        st.subheader("📊 Quiz Leaderboard")
        st.dataframe(get_quiz_leaderboard())

    # Community section
    if st.session_state.quiz_submitted and not st.session_state.community_submitted:
        st.markdown("---")
        st.subheader("🌐 Community Contribution Score")
        community_score = st.slider("Enter your Community Score (0-10)", 0, 10, 0)
        if st.button("Submit Community Score"):
            community_badge = score_to_badge(community_score)
            st.success(f"Community Score: {community_score}, Badge: 🏅 {community_badge}")
            # Update entry
            insert_user(
                st.session_state.user_name,
                st.session_state.user_email,
                score,
                quiz_badge,
                community_score,
                community_badge,
                (score + community_score) / 2,
                score_to_badge((score + community_score) / 2)
            )
            st.session_state.community_submitted = True

            st.markdown("---")
            st.subheader("👥 Community Leaderboard")
            st.dataframe(get_community_leaderboard())

            if st.button("Go to Overall Leaderboard"):
                st.switch_page("https://digital-badge-leaderboard.streamlit.app")
