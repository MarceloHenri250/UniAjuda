import sqlite3
from database import get_connection

class AnswerController:
    def add_answer(self, question_id, answer_text, user_id):
        # Adiciona uma resposta à dúvida.
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO answers (question_id, answer, user_id) VALUES (?, ?, ?)",
                (question_id, answer_text, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao adicionar resposta:", e)
            return False
        finally:
            conn.close()

    def get_answers_by_question_id(self, question_id):
        # Retorna todas as respostas de uma dúvida.
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT a.id, a.question_id, a.answer, a.user_id, u.name
                FROM answers a
                LEFT JOIN users u ON a.user_id = u.id
                WHERE a.question_id = ?
            """, (question_id,))
            return cursor.fetchall()
        finally:
            conn.close()
    
    def get_user_answers(self, user_id):
        # Retorna todas as respostas de um usuário.
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT a.id, a.question_id, a.answer, a.user_id, u.name
                FROM answers a
                LEFT JOIN users u ON a.user_id = u.id
                WHERE a.user_id = ?
            """, (user_id,))
            return cursor.fetchall()
        finally:
            conn.close()
