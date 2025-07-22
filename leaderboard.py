import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="📊 Full Leaderboard", layout="wide")
st.title("🏆 Full User Performance Leaderboard")

try:
    df = pd.read_excel("leaderboard.xlsx")

    if df.empty:
        st.warning("Leaderboard is currently empty. Submit a quiz to populate it.")
        st.stop()

    # Display complete leaderboard
    st.dataframe(df[[
        "name", "email",
        "quiz_score", "quiz_badge",
        "community_score", "community_badge",
        "overall_score", "overall_badge"
    ]], use_container_width=True)

    # Create downloadable Excel in-memory
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')
    excel_buffer.seek(0)

    st.download_button(
        label="⬇ Download Leaderboard as Excel",
        data=excel_buffer,
        file_name="full_leaderboard.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

except FileNotFoundError:
    st.error("❌ Leaderboard file not found. Please make sure leaderboard.xlsx is uploaded.")
except Exception as e:
    st.error(f"⚠️ Unexpected error: {e}")
