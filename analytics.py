import sqlite3

def get_analytics():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, COUNT(scans.id) FROM users LEFT JOIN scans ON users.id = scans.user_id GROUP BY users.id')
    analytics = cursor.fetchall()
    conn.close()
    return analytics