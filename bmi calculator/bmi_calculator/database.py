import sqlite3
import datetime

class DatabaseManager:
    def __init__(self, db_name="bmi_data.db"):
        self.db_name = db_name
        self.create_tables()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    weight REAL NOT NULL,
                    height REAL NOT NULL,
                    bmi REAL NOT NULL,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            conn.commit()

    def add_user(self, name):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None # User already exists

    def get_users(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM users ORDER BY name")
            return cursor.fetchall()

    def add_record(self, user_id, weight, height, bmi):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO records (user_id, weight, height, bmi)
                VALUES (?, ?, ?, ?)
            """, (user_id, weight, height, bmi))
            conn.commit()
            return cursor.lastrowid

    def get_records(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT weight, height, bmi, date FROM records
                WHERE user_id = ?
                ORDER BY date ASC
            """, (user_id,))
            return cursor.fetchall()

    def delete_records(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM records WHERE user_id = ?", (user_id,))
            conn.commit()
