import sqlite3
from database import get_connection

class ReportController:
    def add_report(self, question_id, reason):
        # Adiciona uma denúncia para uma dúvida.
        conn = get_connection()
        try:
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
