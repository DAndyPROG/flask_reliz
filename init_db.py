from flask import Flask
from database import init_db
import os

app = Flask(__name__)

def initialize_database():
    try:
        # Перевіряємо наявність файлу schema.sql
        if not os.path.exists('schema.sql'):
            print("Помилка: Файл schema.sql не знайдено")
            return False
            
        init_db(app)
        print("База даних успішно ініціалізована")
        return True
    except Exception as e:
        print(f"Помилка при ініціалізації бази даних: {e}")
        return False

if __name__ == '__main__':
    initialize_database() 