import streamlit as st
import pandas as pd
from database import get_overall_leaderboard

st.set_page_config(page_title="🏅 Leaderboard Summary", layout="wide")
st.title("📊 Overall Leaderboard")

st.markdown("Here is the complete performance table for all users:")

leaderboard_df = get_overall_leaderboard()
st.dataframe(leaderboard_df, use_container_width=True)

st.download_button(
    label="⬇ Download Leaderboard as Excel",
    data=leaderboard_df.to_excel(index=False, engine='openpyxl'),
    file_name="full_leaderboard.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

