import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
import streamlit as st

def get_worksheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds_dict = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open("Digital Badge Leaderboard")  # Replace with your actual sheet name
    return sheet.worksheet("Sheet1")  # Ensure this matches the name of the sheet tab

def insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge):
    ws = get_worksheet()
    ws.append_row([
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
    ws = get_worksheet()
    records = ws.get_all_records()
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=["name", "email", "quiz_score", "quiz_badge"])
    df.sort_values(by="quiz_score", ascending=False, inplace=True)
    return df[["name", "email", "quiz_score", "quiz_badge"]]

def get_community_leaderboard():
    ws = get_worksheet()
    records = ws.get_all_records()
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=["name", "email", "community_score", "community_badge"])
    df.sort_values(by="community_score", ascending=False, inplace=True)
    return df[["name", "email", "community_score", "community_badge"]]

def get_overall_leaderboard():
    ws = get_worksheet()
    records = ws.get_all_records()
    df = pd.DataFrame(records)
    if df.empty:
        return pd.DataFrame(columns=[
            "name", "email", "quiz_score", "quiz_badge",
            "community_score", "community_badge",
            "overall_score", "overall_badge"
        ])
    df.sort_values(by="overall_score", ascending=False, inplace=True)
    return df
