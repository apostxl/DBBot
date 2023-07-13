import configparser
import sqlite3


def check_admins_database(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM admins WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False

def check_admin_status(user_id):
    config = configparser.ConfigParser()
    config.read('config.ini')
    adminIDs = config.get('Bot', 'adminID')
    if str(user_id) in adminIDs or check_admins_database(user_id):
        return True
    else:
        return False

def check_access_key(key):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM keys WHERE access_code=?", (key,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


def check_user_in_database(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    if user:
        usage_left = user[4]
        if usage_left == 0:
            cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
            conn.commit()
        conn.close()
        return True

    conn.close()
    return False
