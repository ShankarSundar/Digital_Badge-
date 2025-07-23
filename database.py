import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import streamlit as st
import json

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_dict = st.secrets["gcp_service_account"]
credentials_json = json.loads(json.dumps(credentials_dict))
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_json, scope)
client = gspread.authorize(credentials)
sheet = client.open("Digital Badge Leaderboard")

def insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge):
    worksheet = sheet.worksheet("Leaderboard")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()

    if "email" in df.columns and email in df["email"].values:
        idx = df[df["email"] == email].index[0] + 2
        worksheet.update(f"A{idx}:H{idx}", [[name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge]])
    else:
        worksheet.append_row([name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge])

def get_quiz_leaderboard():
    worksheet = sheet.worksheet("Leaderboard")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()
    if "quiz_score" in df.columns:
        return df[["name", "email", "quiz_score", "quiz_badge"]].sort_values(by="quiz_score", ascending=False)
    return pd.DataFrame()

def get_community_leaderboard():
    worksheet = sheet.worksheet("Leaderboard")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()
    if "community_score" in df.columns:
        return df[["name", "email", "community_score", "community_badge"]].sort_values(by="community_score", ascending=False)
    return pd.DataFrame()

def get_overall_leaderboard():
    worksheet = sheet.worksheet("Leaderboard")
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
    df.columns = df.columns.str.strip().str.lower()
    if {"name", "email", "quiz_score", "quiz_badge", "community_score", "community_badge", "overall_score", "overall_badge"}.issubset(df.columns):
        return df[["name", "email", "quiz_score", "quiz_badge", "community_score", "community_badge", "overall_score", "overall_badge"]].sort_values(by="overall_score", ascending=False)
    return pd.DataFrame()