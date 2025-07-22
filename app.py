import streamlit as st
import json
import os
import pandas as pd
from badge_logic import assign_score_badge, assign_overall_badge
from database import init_db, insert_user, get_all_users

st.set_page_config(page_title="Digital Badge System", layout="wide")
init_db()

# ----------------------------
# Route via query parameter
# ----------------------------
query_params = st.query_params
route = query_params.get("page", "quiz").lower()

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = {}
if "page_state" not in st.session_state:
    st.session_state.page_state = "start"

# ----------------------------
# Route: Leaderboard only
# ----------------------------
if route == "leaderboard":
    st.title("🏆 Leaderboard - University Badges")
    rows = get_all_users()
    if rows:
        sorted_rows = sorted(rows, key=lambda x: (x[2] + x[3]) / 2, reverse=True)
        leaderboard_data = [
            {
                "Name": row[0],
                "Email": row[1],
                "Quiz Score": row[2],
                "Community Score": row[3],
                "Average": round((row[2] + row[3]) / 2, 1),
                "Overall Badge": row[5]
            }
            for row in sorted_rows
        ]
        st.table(leaderboard_data)
    else:
        st.warning("No submissions yet.")

# ----------------------------
# Route: Full Quiz + Badge flow
# ----------------------------
elif route == "quiz":

    # PAGE 1: Start
    if st.session_state.page_state == "start":
        st.title("🎓 University Badge System")
        with st.form("user_form"):
            name = st.text_input("Enter your name:")
            email = st.text_input("Enter your university email:")
            submitted = st.form_submit_button("Start Quiz")
            if submitted and name and email:
                st.session_state.name = name
                st.session_state.email = email
                st.session_state.page_state = "quiz"

    # PAGE 2: Quiz + Community
    elif st.session_state.page_state == "quiz":
        st.title("📝 Knowledge Check Quiz")
        with open("questions.json", "r") as f:
            questions = json.load(f)

        user_answers = []
        score = 0
        all_answered = True

        st.subheader("📝 Quiz Questions")

        for idx, q in enumerate(questions):
            selected = st.radio(
                q["question"],
                q["options"],
                key=f"q_{idx}",
                index=None  # 🟢 This ensures no default selection
            )

            if selected is None:
                all_answered = False

            user_answers.append({"selected": selected, "correct": q["answer"]})

        st.subheader("💬 Community Engagement Score")
        community_score = st.slider("Rate your community engagement (0–10)", 0, 10, 5)

        if st.button("Submit Quiz"):
            if not all_answered:
                st.warning("❗ Please answer all questions before submitting.")
            else:
                for ans in user_answers:
                    if ans["selected"] == ans["correct"]:
                        score += 1


            score_badge = assign_score_badge(score)
            avg_score = (score + community_score) / 2
            overall_badge = assign_overall_badge(avg_score)

            st.session_state.quiz_data = {
                "name": st.session_state.name,
                "email": st.session_state.email,
                "quiz_score": score,
                "community_score": community_score,
                "score_badge": score_badge,
                "overall_badge": overall_badge,
                "avg_score": avg_score
            }

            insert_user(
                st.session_state.name,
                st.session_state.email,
                score,
                community_score,
                score_badge,
                overall_badge
            )

            # Save to Excel
            record = pd.DataFrame([{
                "Name": st.session_state.name,
                "Email": st.session_state.email,
                "Quiz Score": score,
                "Community Score": community_score,
                "Average Score": avg_score,
                "Score Badge": score_badge,
                "Overall Badge": overall_badge
            }])

            excel_file = "user_submissions.xlsx"
            if os.path.exists(excel_file):
                existing = pd.read_excel(excel_file)
                combined = pd.concat([existing, record], ignore_index=True)
            else:
                combined = record

            combined.to_excel(excel_file, index=False)

            st.session_state.page_state = "results"
            st.rerun()

    # PAGE 3: Quiz Result (Score Badge)
    elif st.session_state.page_state == "results":
        st.title("🏅 Quiz Badge Result")
        qd = st.session_state.quiz_data
        st.success(f"{qd['name']}, you scored {qd['quiz_score']}/10.")
        st.info(f"🏅 Quiz Badge: **{qd['score_badge']}**")
        badge_path = f"assets/{qd['score_badge'].lower()}.png"
        if os.path.exists(badge_path):
            st.image(badge_path, width=150)
        else:
            st.warning("No badge image available.")

        if st.button("Next"):
            st.session_state.page_state = "overall"
            st.rerun()

    # PAGE 4: Final Result (Overall Badge + Leaderboard)
    elif st.session_state.page_state == "overall":
        st.title("🏆 Final Result & Leaderboard")
        qd = st.session_state.quiz_data
        st.success(f"✅ Average Score: {qd['avg_score']:.1f}")
        st.info(f"🏆 Overall Badge: **{qd['overall_badge']}**")
        badge_path = f"assets/{qd['overall_badge'].lower()}.png"
        if os.path.exists(badge_path):
            st.image(badge_path, width=150)
        else:
            st.warning("No badge image available.")

        st.markdown("---")
        st.subheader("📊 Leaderboard")
        rows = get_all_users()
        if rows:
            sorted_rows = sorted(rows, key=lambda x: (x[2] + x[3]) / 2, reverse=True)
            leaderboard_data = [
                {
                    "Name": row[0],
                    "Email": row[1],
                    "Quiz Score": row[2],
                    "Community Score": row[3],
                    "Average": round((row[2] + row[3]) / 2, 1),
                    "Overall Badge": row[5]
                }
                for row in sorted_rows
            ]
            st.table(leaderboard_data)
        else:
            st.warning("No submissions yet.")

        if st.button("End"):
            st.session_state.clear()
            st.session_state.page_state = "start"
            st.success("Thank you! You may now close this window.")
