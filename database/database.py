import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                    CREATE TABLE IF NOT EXISTS survey_results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        phone_or_instagram INTEGER,
                        visit_date TEXT,
                        food_rating TEXT,
                        cleanliness_rating TEXT,
                        extra_comments_rating TEXT
                    )
                """
            )
            conn.commit()