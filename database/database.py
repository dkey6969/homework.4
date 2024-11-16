import sqlite3

class Database:
    def __init__(self, db_name="bot_database.db"):
        self.db_name = db_name
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone_or_instagram TEXT,
            visit_date TEXT,
            food_rating INTEGER,
            cleanliness_rating INTEGER,
            extra_comments TEXT
        )
        """)
        self.connection.commit()

    def execute(self, query, params):
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetchall(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()


database = Database()