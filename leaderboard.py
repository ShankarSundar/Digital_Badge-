import streamlit as st
from database import get_overall_leaderboard
import pandas as pd

st.set_page_config(page_title="📊 Overall Leaderboard", layout="centered")
st.title("🏆 Digital Badge - Overall Leaderboard")

try:
    leaderboard_df = get_overall_leaderboard()
    if leaderboard_df.empty:
        st.info("No records found yet.")
    else:
        st.dataframe(leaderboard_df)
        st.success("Leaderboard loaded successfully.")
except Exception as e:
    st.error(f"❌ Failed to load leaderboard: {e}")
