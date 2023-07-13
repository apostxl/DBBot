import sqlite3

def get_user_access_code(user_ID):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT access_code FROM users WHERE user_id=?", (user_ID,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return None

def get_usage_left(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT usage_left FROM users WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result is not None:
        return result[0]
    else:
        return 0