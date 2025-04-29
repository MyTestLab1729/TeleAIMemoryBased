import sqlite3
import json
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            chat_id TEXT,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_history(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT message FROM chats WHERE chat_id = ?", (chat_id,))
    rows = c.fetchall()
    conn.close()
    return [json.loads(row[0]) for row in rows]

def add_message(chat_id, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chats (chat_id, message) VALUES (?, ?)", (chat_id, json.dumps(message)))
    conn.commit()
    conn.close()

def clear_history(chat_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM chats WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()