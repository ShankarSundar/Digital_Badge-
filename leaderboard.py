import streamlit as st
from database import get_overall_leaderboard

st.set_page_config(page_title="Overall Leaderboard", layout="centered")
st.title("🏁 Overall Leaderboard")

st.markdown("View all users' performance across quiz and community contributions.")
df = get_overall_leaderboard()
st.dataframe(df)