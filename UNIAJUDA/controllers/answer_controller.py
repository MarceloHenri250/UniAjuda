import sqlite3
from database import get_connection

class AnswerController:
    def add_answer(self, question_id, answer, user_id):
        conn = get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY (question_id) REFERENCES questions(id),
                    FOREIGN KEY (user_id) REFERENCES usuarios(id)
                )
            """)
            conn.execute(
                "INSERT INTO answers (question_id, answer, user_id) VALUES (?, ?, ?)",
                (question_id, answer, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao adicionar resposta:", e)
            return False
        finally:
            conn.close()

    def get_answers_by_question_id(self, question_id):
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT a.id, a.question_id, a.answer, a.user_id, u.nome
                FROM answers a
                LEFT JOIN usuarios u ON a.user_id = u.id
                WHERE a.question_id = ?
            """, (question_id,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_user_answers(self, user_id):
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT a.id, a.question_id, a.answer, a.user_id, u.nome
                FROM answers a
                LEFT JOIN usuarios u ON a.user_id = u.id
                WHERE a.user_id = ?
            """, (user_id,))
            return cursor.fetchall()
        finally:
            conn.close()
