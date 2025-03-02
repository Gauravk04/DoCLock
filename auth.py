import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user[2], password):
        return {'id': user[0], 'username': user[1], 'role': user[3], 'credits': user[4]}
    return None

def get_user_profile(user_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return {'id': user[0], 'username': user[1], 'role': user[3], 'credits': user[4]}