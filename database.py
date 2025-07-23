import gspread
import pandas as pd
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials_dict = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)
sheet = client.open("Digital Badge Leaderboard").worksheet("Leaderboard")

HEADERS = ["Name", "Email", "Quiz_Score", "Quiz_Badge", "Community_Score", "Community_Badge", "Overall_Score", "Overall_Badge"]

def insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge):
    existing = sheet.get_all_values()
    if not existing:
        sheet.append_row(HEADERS)
    sheet.append_row([name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge])

def update_community_score(email, community_score, community_badge, overall_score, overall_badge):
    df = pd.DataFrame(sheet.get_all_records())

    if df.empty:
        st.error("Google Sheet is empty.")
        return

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    email_col = "email"

    if email_col not in df.columns:
        st.error(f"Column '{email_col}' not found in sheet. Found columns: {df.columns.tolist()}")
        return

    email = email.strip().lower()
    found = False

    for i, row in df.iterrows():
        if str(row[email_col]).strip().lower() == email:
            df.at[i, "community_score"] = community_score
            df.at[i, "community_badge"] = community_badge
            df.at[i, "overall_score"] = overall_score
            df.at[i, "overall_badge"] = overall_badge
            found = True
            break

    if not found:
        st.warning("User not found in leaderboard for community update.")
        return

    # Push updated data
    sheet.clear()
    sheet.append_row(["Name", "Email", "Quiz_Score", "Quiz_Badge", "Community_Score", "Community_Badge", "Overall_Score", "Overall_Badge"])
    for row in df.itertuples(index=False):
        sheet.append_row(list(row))


def get_quiz_leaderboard():
    df = pd.DataFrame(sheet.get_all_records())
    df.columns = [col.lower().strip() for col in df.columns]
    df["quiz_score"] = pd.to_numeric(df["quiz_score"], errors="coerce")
    return df[["name", "email", "quiz_score", "quiz_badge"]].sort_values(by="quiz_score", ascending=False)

def get_community_leaderboard():
    df = pd.DataFrame(sheet.get_all_records())
    df.columns = [col.lower().strip() for col in df.columns]
    df["community_score"] = pd.to_numeric(df["community_score"], errors="coerce")
    return df[["name", "email", "community_score", "community_badge"]].sort_values(by="community_score", ascending=False)

def get_overall_leaderboard():
    df = pd.DataFrame(sheet.get_all_records())
    df.columns = [col.lower().strip() for col in df.columns]
    df["overall_score"] = pd.to_numeric(df["overall_score"], errors="coerce")
    return df[["name", "email", "quiz_score", "quiz_badge", "community_score", "community_badge", "overall_score", "overall_badge"]].sort_values(by="overall_score", ascending=False)
