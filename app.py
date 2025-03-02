from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from database import get_db, init_db
from auth import register_user, login_user, get_user_profile
from credit import request_credits, reset_daily_credits, deduct_credit
from scan import upload_document, get_matching_documents
from analytics import get_analytics

import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')  # Required for session management

# Initialize database
init_db()

# Homepage
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile'))
    return render_template('index.html')

# User registration
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            register_user(username, password)
            return redirect(url_for('login'))
        except Exception as e:
            return str(e)
    return render_template('register.html')

# User login
@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            user = login_user(username, password)
            if user:
                session['user_id'] = user['id']
                reset_daily_credits(user['id'])  # Reset credits if needed
                return redirect(url_for('profile'))
            return render_template('login.html', error="Invalid credentials")
        except Exception as e:
            return render_template('login.html', error=str(e))
    return render_template('login.html')

# User profile
@app.route('/user/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = get_user_profile(session['user_id'])
    return render_template('profile.html', user=user)

# Document upload
@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['document']
        user_id = session['user_id']
        if deduct_credit(user_id):
            try:
                document_id = upload_document(user_id, file)
                return render_template('scan.html', document_id=document_id)
            except Exception as e:
                return f"An error occurred during upload: {str(e)}"
        return render_template('scan.html', error="Insufficient credits")
    return render_template('scan.html')

# Matching documents
@app.route('/matches/<int:doc_id>')
def matches(doc_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    matches = get_matching_documents(doc_id)
    return render_template('matches.html', matches=matches)

# Admin dashboard
@app.route('/admin/analytics')
def admin_analytics():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = get_user_profile(session['user_id'])
    if user['role'] != 'admin':
        return render_template('error.html', message="Unauthorized access")
    analytics = get_analytics()
    return render_template('admin.html', analytics=analytics)

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1', 't']
    app.run(debug=debug_mode)