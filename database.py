import sqlite3

# Create DB and users table if not exists
def init_db():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            quiz_score INTEGER,
            community_score INTEGER,
            score_badge TEXT,
            overall_badge TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Insert user attempt
def insert_user(name, email, quiz_score, community_score, score_badge, overall_badge):
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (name, email, quiz_score, community_score, score_badge, overall_badge)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, quiz_score, community_score, score_badge, overall_badge))
    conn.commit()
    conn.close()

# Fetch all usersstre
def get_all_users():
    conn = sqlite3.connect("user_data.db")
    c = conn.cursor()
    c.execute("SELECT name, email, quiz_score, community_score, score_badge, overall_badge FROM users")
    rows = c.fetchall()
    conn.close()
    return rows
