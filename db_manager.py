import os
import sqlite3
import json
from config import DB_PATH

# Ensure the /db directory exists
DB_DIR = "db"
os.makedirs(DB_DIR, exist_ok=True)

def get_user_db(chat_id):
    """Get the path to the user's database file."""
    return os.path.join(DB_DIR, f"{chat_id}.db")

def initialize_user_db(chat_id):
    """Initialize a user-specific database if it doesn't exist."""
    db_path = get_user_db(chat_id)
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Create a table for storing conversation history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

def get_history(chat_id):
    """Retrieve the conversation history for a specific user."""
    db_path = get_user_db(chat_id)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM history ORDER BY id ASC")
    history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
    conn.close()
    return history

def add_message(chat_id, message):
    """Add a message to the user's conversation history."""
    db_path = get_user_db(chat_id)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (role, content) VALUES (?, ?)", (message["role"], message["content"]))
    conn.commit()
    conn.close()

def clear_history(chat_id):
    """Clear the conversation history for a specific user."""
    db_path = get_user_db(chat_id)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()