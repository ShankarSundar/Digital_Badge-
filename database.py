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

def insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge):
    sheet.append_row([name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge])

def update_community_score(email, community_score, community_badge, overall_score, overall_badge):
    records = sheet.get_all_records()
    for idx, row in enumerate(records, start=2):
        if row.get("Email", "").strip().lower() == email.strip().lower():
            sheet.update(f"E{idx}", str(community_score))
            sheet.update(f"F{idx}", community_badge)
            sheet.update(f"G{idx}", str(overall_score))
            sheet.update(f"H{idx}", overall_badge)
            break

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
