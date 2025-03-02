import sqlite3
from datetime import datetime

def deduct_credit(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT credits, last_reset FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if user[0] > 0:
        cursor.execute('UPDATE users SET credits = credits - 1 WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def request_credits(user_id, credits):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO credit_requests (user_id, requested_credits) VALUES (?, ?)', (user_id, credits))
    conn.commit()
    conn.close()

def reset_daily_credits(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT last_reset FROM users WHERE id = ?', (user_id,))
    last_reset = cursor.fetchone()[0]
    today = datetime.now().date()
    if last_reset != today:
        cursor.execute('UPDATE users SET credits = 20, last_reset = ? WHERE id = ?', (today, user_id))
        conn.commit()
    conn.close()