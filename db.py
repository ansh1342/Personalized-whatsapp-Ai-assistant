import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

def get_user(phone):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE phone=%s", (phone,))
    user = cursor.fetchone()

    conn.close()
    return user

def create_user(phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT IGNORE INTO users (phone) VALUES (%s)", (phone,))
    conn.commit()

    conn.close()

def save_chat(phone, user_message, bot_reply):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (phone, user_message, bot_reply) VALUES (%s, %s, %s)",
        (phone, user_message, bot_reply)
    )
    conn.commit()
    conn.close()

def get_last_chats(phone, limit=5):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"SELECT user_message, bot_reply FROM chats WHERE phone=%s ORDER BY id DESC LIMIT {limit}"
    cursor.execute(query, (phone,))

    chats = cursor.fetchall()
    conn.close()

    return chats[::-1]

