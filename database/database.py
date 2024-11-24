import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dish_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS dishes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    category_id INTEGER,
                    FOREIGN KEY(category_id) REFERENCES dish_categories(id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    review TEXT,
                    FOREIGN KEY(telegram_id) REFERENCES users(telegram_id)
                )
            """)
            conn.commit()

    def execute(self, query: str, params: tuple):
        with sqlite3.connect(self.path) as conn:
            conn.execute(query, params)
            conn.commit()

    def fetch(self, query: str, params: tuple = None):
        with sqlite3.connect(self.path) as conn:
            if not params:
                params = tuple()
            result = conn.execute(query, params)
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(r) for r in data]