import streamlit as st
import pandas as pd
from database import get_leaderboard
from io import BytesIO

st.set_page_config(page_title="🏆 Leaderboard", layout="wide")
st.title("📊 Full Performance Leaderboard")

try:
    df = get_leaderboard()

    if df.empty:
        st.warning("Leaderboard is currently empty.")
    else:
        st.dataframe(df, use_container_width=True)

        excel_buffer = BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)

        st.download_button(
            label="⬇ Download Leaderboard (Excel)",
            data=excel_buffer,
            file_name="leaderboard.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
except Exception as e:
    st.error(f"❌ Failed to load leaderboard: {e}")