import sqlite3
from database import get_connection

class ReportController:
    def add_report(self, question_id, reason):
        conn = get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            """)
            conn.execute(
                "INSERT INTO reports (question_id, reason) VALUES (?, ?)",
                (question_id, reason)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao adicionar denúncia:", e)
            return False
        finally:
            conn.close()
