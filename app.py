import streamlit as st
import json
import random
from badge_logic import score_to_badge
from database import (
    insert_user,
    update_community_score,
    get_quiz_leaderboard,
    get_community_leaderboard,
    get_overall_leaderboard
)

st.set_page_config(page_title="Digital Badge Quiz", layout="wide")
st.title("🎓 Knowledge Quiz & Community Score")

if "step" not in st.session_state:
    st.session_state.step = 1

# Step 1: Login
if st.session_state.step == 1:
    st.subheader("Enter Your Details")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Start Quiz"):
        if name and email:
            st.session_state.name = name
            st.session_state.email = email
            try:
                with open("questions.json", "r", encoding="utf-8") as f:
                    questions = json.load(f)
                st.session_state.selected_questions = random.sample(questions, k=10)
            except Exception as e:
                st.error(f"Error loading questions: {e}")
                st.stop()
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Please enter both name and email to continue.")

# Step 2: Quiz
elif st.session_state.step == 2:
    st.subheader("🧠 Quiz Time!")

    for i, q in enumerate(st.session_state.selected_questions):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        options = ["-- Select an option --"] + q["options"]
        key = f"question_{i}_{q['question'][:10]}"
        selected = st.radio("Choose one:", options, key=key)
        st.markdown("---")

    if st.button("Submit Quiz"):
        user_answers = []
        for i, q in enumerate(st.session_state.selected_questions):
            key = f"question_{i}_{q['question'][:10]}"
            user_answer = st.session_state.get(key)
            if user_answer not in q["options"]:
                st.warning("Please answer all questions before submitting.")
                st.stop()
            user_answers.append((q["answer"], user_answer))

        score = sum(1 for correct, user_ans in user_answers if correct == user_ans)
        badge = score_to_badge(score)

        insert_user(st.session_state.name, st.session_state.email, score, badge, "", "", "", "")
        st.session_state.quiz_score = score
        st.session_state.quiz_badge = badge
        st.session_state.step = 3
        st.rerun()

# Step 3: Show Quiz Results
elif st.session_state.step == 3:
    st.success(f"✅ You scored {st.session_state.quiz_score}/10!")
    st.info(f"🏅 Quiz Badge: {st.session_state.quiz_badge}")
    st.subheader("📊 Quiz Leaderboard")
    st.dataframe(get_quiz_leaderboard(), use_container_width=True)
    if st.button("Enter Community Score"):
        st.session_state.step = 4
        st.rerun()

# Step 4: Enter Community Score
elif st.session_state.step == 4:
    st.subheader("🤝 Community Participation")
    community_score = st.number_input("Enter your community score (0–10):", 0, 10, step=1)

    if st.button("Submit Community Score"):
        try:
            community_score = float(community_score)
            community_badge = score_to_badge(community_score)
            overall_score = (st.session_state.quiz_score + community_score) / 2
            overall_badge = score_to_badge(overall_score)

            update_community_score(
                st.session_state.email,
                community_score,
                community_badge,
                overall_score,
                overall_badge
            )

            st.session_state.community_score = community_score
            st.session_state.community_badge = community_badge
            st.session_state.step = 5
            st.rerun()
        except Exception as e:
            st.error(f"Error submitting community data: {e}")

# Step 5: Show Community Leaderboard
elif st.session_state.step == 5:
    st.success(f"🫂 Community Score: {st.session_state.community_score}/10")
    st.info(f"🤝 Community Badge: {st.session_state.community_badge}")
    st.subheader("🌍 Community Leaderboard")
    st.dataframe(get_community_leaderboard(), use_container_width=True)
    if st.button("Next: View Overall Leaderboard"):
        st.session_state.step = 6
        st.rerun()

# Step 6: Overall Leaderboard
elif st.session_state.step == 6:
    st.subheader("🏆 Overall Leaderboard")
    st.dataframe(get_overall_leaderboard(), use_container_width=True)
    st.markdown("You may now close the app.")
