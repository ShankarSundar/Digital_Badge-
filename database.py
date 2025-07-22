import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Setup Google Sheets connection
def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Digital Badge Leaderboard").sheet1
    return sheet

# Insert a new user record into the sheet
def insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge):
    sheet = get_sheet()
    sheet.append_row([
        name,
        email,
        quiz_score,
        quiz_badge,
        community_score,
        community_badge,
        overall_score,
        overall_badge
    ])

# Retrieve leaderboard data
def get_leaderboard():
    sheet = get_sheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df