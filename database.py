import sqlite3
import pandas as pd

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            email TEXT,
            quiz_score INTEGER,
            quiz_badge TEXT,
            community_score INTEGER,
            community_badge TEXT,
            overall_score REAL,
            overall_badge TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (name, email, quiz_score, quiz_badge, community_score, community_badge, overall_score, overall_badge))
    conn.commit()
    conn.close()

def get_quiz_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT name, email, quiz_score, quiz_badge FROM users ORDER BY quiz_score DESC", conn)
    conn.close()
    return df

def get_community_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT name, email, community_score, community_badge FROM users ORDER BY community_score DESC", conn)
    conn.close()
    return df

def get_overall_leaderboard():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM users ORDER BY overall_score DESC", conn)
    conn.close()
    return df