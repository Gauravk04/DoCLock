import os
import sqlite3

UPLOAD_FOLDER = 'uploads'

def upload_document(user_id, file):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO scans (user_id, document_path) VALUES (?, ?)', (user_id, file_path))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_matching_documents(doc_id):
    # Implement text matching logic here
    return []