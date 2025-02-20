from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, close_db, init_db
import re
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Змініть на власний секретний ключ

# Перевіряємо наявність бази даних при запуску
if not os.path.exists('database.db'):
    try:
        init_db(app)
    except Exception as e:
        print(f"Помилка при ініціалізації бази даних: {e}")

# Реєструємо функцію закриття з'єднання з БД
@app.teardown_appcontext
def close_connection(exception):
    close_db()

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    return len(password) >= 6

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if not email or not password:
            flash('Будь ласка, заповніть всі поля')
            return redirect(url_for('login'))
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['name']
            return redirect(url_for('index'))
        
        flash('Невірний email або пароль')
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm-password']
    
    if not all([name, email, password, confirm_password]):
        flash('Будь ласка, заповніть всі поля')
        return redirect(url_for('login'))
    
    if not is_valid_email(email):
        flash('Невірний формат email')
        return redirect(url_for('login'))
    
    if not is_valid_password(password):
        flash('Пароль повинен містити мінімум 6 символів')
        return redirect(url_for('login'))
    
    if password != confirm_password:
        flash('Паролі не співпадають')
        return redirect(url_for('login'))
    
    try:
        db = get_db()
        db.execute(
            'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
            (name, email, generate_password_hash(password))
        )
        db.commit()
        flash('Реєстрація успішна! Тепер ви можете увійти.')
    except sqlite3.IntegrityError:
        flash('Користувач з таким email вже існує')
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 