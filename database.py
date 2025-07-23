import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
import json


scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


# Read credentials from Streamlit secrets
credentials_dict = st.secrets["gcp_service_account"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
client = gspread.authorize(credentials)
sheet = client.open("Digital Badge Leaderboard")

def init_db():
    try:
        sheet.worksheet("Quiz")
    except gspread.exceptions.WorksheetNotFound:
        sheet.add_worksheet(title="Quiz", rows="1000", cols="10")

    try:
        sheet.worksheet("Community")
    except gspread.exceptions.WorksheetNotFound:
        sheet.add_worksheet(title="Community", rows="1000", cols="10")

def insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge):
    worksheet = sheet.worksheet("Leaderboard")
    worksheet.append_row([
        name,
        email,
        quiz_score,
        quiz_badge,
        community_score,
        community_badge,
        overall_score,
        overall_badge
    ])


def get_quiz_leaderboard():
    worksheet = sheet.worksheet("Leaderboard")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    # Standardize column names
    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    # Only keep quiz-related columns
    df = df[["name", "email", "quiz_score", "quiz_badge"]]

    df_sorted = df.sort_values(by="quiz_score", ascending=False)
    return df_sorted


def get_community_leaderboard():
    worksheet = sheet.worksheet("Leaderboard")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]

    # Ensure required columns exist
    if "community_score" not in df.columns:
        st.warning("Missing 'community_score' column in Google Sheet.")
        return pd.DataFrame()

    df = df[["name", "email", "community_score", "community_badge"]]
    df_sorted = df.sort_values(by="community_score", ascending=False)
    return df_sorted


def get_overall_leaderboard():
    quiz_df = pd.DataFrame(sheet.worksheet("Quiz").get_all_records())
    community_df = pd.DataFrame(sheet.worksheet("Community").get_all_records())

    merged = pd.merge(quiz_df, community_df, on="email", how="outer")

    merged["quiz_score"] = merged["quiz_score"].fillna(0)
    merged["community_score"] = merged["community_score"].fillna(0)

    merged["overall_score"] = (merged["quiz_score"] + merged["community_score"]) / 2

    def score_to_badge(score):
        if score >= 9:
            return "Gold"
        elif score >= 6:
            return "Silver"
        elif score >= 3:
            return "Bronze"
        else:
            return "No Badge"

    merged["overall_badge"] = merged["overall_score"].apply(score_to_badge)

    merged = merged[[
        "name", "email", "quiz_score", "quiz_badge",
        "community_score", "community_badge",
        "overall_score", "overall_badge"
    ]]

    return merged.sort_values(by="overall_score", ascending=False)

def update_user_score(email, community_score, community_badge):
    worksheet = sheet.worksheet("Community")
    data = worksheet.get_all_records()

    for i, row in enumerate(data):
        if row["email"] == email:
            worksheet.update_cell(i + 2, 3, community_score)
            worksheet.update_cell(i + 2, 4, community_badge)
            return

    # If email not found, insert new
    user_name = get_user_name_by_email(email)
    worksheet.append_row([user_name, email, community_score, community_badge])

def get_user_name_by_email(email):
    quiz_data = pd.DataFrame(sheet.worksheet("Quiz").get_all_records())
    user_row = quiz_data[quiz_data["email"] == email]
    if not user_row.empty:
        return user_row.iloc[0]["name"]
    return "Unknown"
