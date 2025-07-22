import streamlit as st
import pandas as pd
from database import get_overall_leaderboard

st.set_page_config(page_title="🏅 Public Leaderboard", layout="wide")
st.title("📊 Full Overall Leaderboard")

leaderboard_df = get_overall_leaderboard()
st.dataframe(leaderboard_df, use_container_width=True)

st.download_button(
    label="⬇ Download Leaderboard as Excel",
    data=leaderboard_df.to_excel(index=False, engine='openpyxl'),
    file_name="full_leaderboard.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.success("Share this page link with your faculty or project manager.")
