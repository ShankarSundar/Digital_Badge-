# leaderboard.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="🏅 Public Leaderboard", layout="wide")
st.title("📊 Full Overall Leaderboard")

try:
    df = pd.read_excel("leaderboard.xlsx")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        label="⬇ Download Leaderboard as Excel",
        data=df.to_excel(index=False, engine='openpyxl'),
        file_name="full_leaderboard.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success("Share this link with others to show user performance.")
except FileNotFoundError:
    st.error("Leaderboard not yet available. Complete a quiz to generate it.")
