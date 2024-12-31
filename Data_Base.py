import sqlite3
import hashlib


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect('drug_search.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Search history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            drug_name TEXT NOT NULL,
            search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                           (username, hashed_password))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        cursor = self.conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('SELECT id FROM users WHERE username = ? AND password = ?',
                       (username, hashed_password))
        result = cursor.fetchone()
        return result[0] if result else None

    def add_search_history(self, user_id, drug_name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO search_history (user_id, drug_name) VALUES (?, ?)',
                       (user_id, drug_name))
        self.conn.commit()

    def get_user_history(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT drug_name, search_date 
            FROM search_history 
            WHERE user_id = ? 
            ORDER BY search_date DESC
            LIMIT 10
        ''', (user_id,))
        return cursor.fetchall()