import sqlite3
import pandas as pd

DB_PATH = "users.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            email TEXT,
            quiz_score INTEGER,
            quiz_badge TEXT,
            community_score INTEGER,
            overall_score REAL,
            overall_badge TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(name, email, quiz_score, quiz_badge, community_score, overall_score, overall_badge):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (name, email, quiz_score, quiz_badge, community_score, overall_score, overall_badge)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, email, quiz_score, quiz_badge, community_score, overall_score, overall_badge))
    conn.commit()
    conn.close()

def get_quiz_leaderboard():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT name, email, quiz_score, community_score, quiz_badge FROM users ORDER BY quiz_score DESC", conn
    )
    conn.close()
    return df

def get_overall_leaderboard():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT name, email, quiz_score, community_score, overall_score, overall_badge FROM users ORDER BY overall_score DESC", conn
    )
    conn.close()
    return df
