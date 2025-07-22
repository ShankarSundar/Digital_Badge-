# leaderboard.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="🏅 Full Leaderboard", layout="wide")
st.title("📊 Full User Performance Leaderboard")

try:
    df = pd.read_excel("leaderboard.xlsx")
    # Show only relevant columns
    st.dataframe(df[["name", "quiz_score", "community_score", "overall_score", "overall_badge"]], use_container_width=True)

    st.download_button(
        label="⬇ Download Leaderboard as Excel",
        data=df.to_excel(index=False, engine='openpyxl'),
        file_name="full_leaderboard.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
except FileNotFoundError:
    st.error("Leaderboard not available yet. Please complete a quiz first.")