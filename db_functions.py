import sqlite3
import os
from datetime import datetime
from functions import generate_code

if not os.path.exists('database.db'):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE keys
                      (access_code TEXT PRIMARY KEY,
                      usage_left INTEGER,
                      status TEXT,
                      created_at TEXT)''')
    cursor.execute('''CREATE TABLE users
                      (user_id INTEGER PRIMARY KEY,
                      username TEXT,
                      access_code TEXT,
                      usage_left INTEGER,
                      timestamp TEXT)''')
    cursor.execute('''CREATE TABLE admins
                      (user_id INTEGER PRIMARY KEY,
                      username TEXT,
                      timestamp TEXT)''')
    conn.commit()
    conn.close()


def add_key_to_database(access_code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    while True:
        cursor.execute("SELECT * FROM keys WHERE access_code=?", (access_code,))
        existing_key = cursor.fetchone()
        if existing_key is None:
            break
        else:
            access_code = generate_code()
    cursor.execute("INSERT INTO keys (access_code, usage_left, status, created_at) VALUES (?, ?, ?, ?)",
                   (access_code, 10, 'Active', created_at))
    conn.commit()
    conn.close()
    return access_code


def update_usage_left(access_code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usage_left FROM keys WHERE access_code=?", (access_code,))
    result = cursor.fetchone()
    if result is not None:
        usage_left = result[0]
        if usage_left > 0:
            usage_left -= 1
            cursor.execute("UPDATE keys SET usage_left=? WHERE access_code=?", (usage_left, access_code))
            conn.commit()
            if usage_left == 0:
                cursor.execute("DELETE FROM keys WHERE access_code=?", (access_code,))
                conn.commit()
    conn.close()


def update_usage_left_users(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usage_left FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    if result is not None:
        usage_left = result[0]
        if usage_left > 0:
            usage_left -= 1
            cursor.execute("UPDATE users SET usage_left=? WHERE user_id=?", (usage_left, user_id))
            conn.commit()
            if usage_left == 0:
                cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
                conn.commit()
    conn.close()


def save_user_to_database(user_id, username, telegram_link, access_code, usage_left):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO users (user_id, username, access_code, usage_left, timestamp) "
                   "VALUES (?, ?, ?, ?, ?)",
                   (user_id, username, access_code, usage_left, timestamp))
    conn.commit()
    conn.close()
