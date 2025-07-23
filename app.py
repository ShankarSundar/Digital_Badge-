import streamlit as st
from badge_logic import score_to_badge
from database import (
    get_quiz_leaderboard,
    get_community_leaderboard,
    get_overall_leaderboard,
    insert_user
)

st.set_page_config(page_title="Digital Badge Quiz", layout="wide")
st.title("📝 Quiz")

# Login Info
with st.form("login_form"):
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your university email")
    submitted_login = st.form_submit_button("Login to Start Quiz")

if submitted_login and name and email:
    st.session_state["name"] = name
    st.session_state["email"] = email
    st.session_state["quiz_started"] = True
    st.rerun()

if "quiz_started" in st.session_state and st.session_state["quiz_started"]:
    st.header("📚 Quiz Questions")

    # Questions
    quiz_questions = [
        {
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "answer": "Paris"
        },
        {
            "question": "What is 2 + 2?",
            "options": ["3", "4", "5", "22"],
            "answer": "4"
        },
        {
            "question": "What is the boiling point of water?",
            "options": ["90°C", "100°C", "80°C", "120°C"],
            "answer": "100°C"
        },
        {
            "question": "What is the capital of Germany?",
            "options": ["Munich", "Berlin", "Frankfurt", "Hamburg"],
            "answer": "Berlin"
        },
        {
            "question": "What color is the sky on a clear day?",
            "options": ["Red", "Green", "Blue", "Yellow"],
            "answer": "Blue"
        }
    ]

    user_answers = []
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**{q['question']}**")
        user_choice = st.radio(f"Question {i+1}", q["options"], key=f"question_{i}")
        user_answers.append(user_choice)

    if st.button("Submit Quiz"):
        correct = sum([1 for i, q in enumerate(quiz_questions) if user_answers[i] == q["answer"]])
        st.session_state["quiz_score"] = correct
        st.session_state["quiz_badge"] = score_to_badge(correct)
        st.session_state["quiz_submitted"] = True
        st.rerun()

if "quiz_submitted" in st.session_state and st.session_state["quiz_submitted"]:
    st.success(f"✅ Your quiz score is: {st.session_state['quiz_score']}/5")
    st.info(f"🏅 Quiz Badge: {st.session_state['quiz_badge']}")

    st.markdown("---")
    st.subheader("📊 Quiz Leaderboard")
    st.dataframe(get_quiz_leaderboard())

    st.markdown("---")
    st.subheader("🤝 Community Contribution")

    community_score = st.number_input("Enter your Community Score (0 to 10):", min_value=0, max_value=10, step=1)
    if st.button("Submit Community Score"):
        community_badge = score_to_badge(community_score)
        overall_score = (st.session_state["quiz_score"] + community_score) / 2
        overall_badge = score_to_badge(overall_score)

        # Store user record
        insert_user(
            st.session_state["name"],
            st.session_state["email"],
            st.session_state["quiz_score"],
            st.session_state["quiz_badge"],
            community_score,
            community_badge,
            overall_score,
            overall_badge
        )

        st.success(f"🎯 Community Score: {community_score}/10")
        st.info(f"🏅 Community Badge: {community_badge}")

        st.markdown("---")
        st.subheader("👥 Community Leaderboard")
        st.dataframe(get_community_leaderboard())

        st.markdown("---")
        st.subheader("🏆 Overall Leaderboard")
        st.dataframe(get_overall_leaderboard())

        st.markdown("---")
        if st.button("End"):
            st.success("✅ Quiz completed. You can now close the tab.")