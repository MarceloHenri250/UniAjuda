import sqlite3
from database import get_connection

class QuestionController:
    def create_question(self, title, description, subject, user_id, attachment=None):
        # Cria uma nova dúvida no banco de dados.
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO questions (title, description, subject, user_id, attachment) VALUES (?, ?, ?, ?, ?)",
                (title, description, subject, user_id, attachment)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao criar dúvida:", e)
            return False
        finally:
            conn.close()

    def get_all_questions(self):
        # Retorna todas as dúvidas (id e título).
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT id, title FROM questions")
            return cursor.fetchall()
        finally:
            conn.close()

    def add_vote(self, question_id):
        # Adiciona um voto à dúvida.
        conn = get_connection()
        try:
            conn.execute("UPDATE questions SET votes = COALESCE(votes, 0) + 1 WHERE id = ?", (question_id,))
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao votar:", e)
            return False
        finally:
            conn.close()

    def get_all_questions_full(self):
        # Retorna todas as dúvidas com informações completas.
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT q.id, q.title, q.description, q.subject, COALESCE(q.votes, 0), q.user_id, u.name, q.attachment
                FROM questions q
                LEFT JOIN users u ON q.user_id = u.id
            """)
            return cursor.fetchall()
        finally:
            conn.close()

    def add_answer(self, question_id, answer):
        # Adiciona uma resposta à dúvida.
        conn = get_connection()
        try:
            conn.execute(
                "INSERT INTO answers (question_id, answer) VALUES (?, ?)",
                (question_id, answer)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao adicionar resposta:", e)
            return False
        finally:
            conn.close()

    def get_question_by_id(self, question_id):
        # Retorna uma dúvida pelo id.
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT id, title, description FROM questions WHERE id = ?", (question_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def get_user_questions(self, user_id):
        # Retorna todas as dúvidas de um usuário.
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT q.id, q.title, q.description, q.subject, COALESCE(q.votes, 0), q.user_id, u.name, q.attachment
                FROM questions q
                LEFT JOIN users u ON q.user_id = u.id
                WHERE q.user_id = ?
            """, (user_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def user_liked_question(self, user_id, question_id):
        # Verifica se o usuário já curtiu a dúvida.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM likes WHERE user_id = ? AND question_id = ?", (user_id, question_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def like_question(self, user_id, question_id):
        # Adiciona uma curtida à dúvida.
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO likes (user_id, question_id) VALUES (?, ?)", (user_id, question_id))
            cursor.execute("UPDATE questions SET votes = votes + 1 WHERE id = ?", (question_id,))
            conn.commit()
        except Exception:
            pass  # Já curtiu
        finally:
            conn.close()

    def unlike_question(self, user_id, question_id):
        # Remove uma curtida da dúvida.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM likes WHERE user_id = ? AND question_id = ?", (user_id, question_id))
        cursor.execute("UPDATE questions SET votes = votes - 1 WHERE id = ? AND votes > 0", (question_id,))
        conn.commit()
        conn.close()
