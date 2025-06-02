import sqlite3
from database import get_connection

class QuestionController:
    def create_question(self, title, description, disciplina, user_id):
        conn = get_connection()
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    disciplina TEXT,
                    votes INTEGER DEFAULT 0,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES usuarios(id)
                )
                """
            )
            conn.execute(
                "INSERT INTO questions (title, description, disciplina, user_id) VALUES (?, ?, ?, ?)",
                (title, description, disciplina, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print("Erro ao criar dúvida:", e)
            return False
        finally:
            conn.close()

    def get_all_questions(self):
        conn = get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL
                )
            """)
            cursor = conn.execute("SELECT id, title FROM questions")
            return cursor.fetchall()
        finally:
            conn.close()

    def add_vote(self, question_id):
        conn = get_connection()
        try:
            conn.execute("""
                ALTER TABLE questions ADD COLUMN votes INTEGER DEFAULT 0
            """)
        except Exception:
            pass  # coluna já existe
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
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT q.id, q.title, q.description, q.disciplina, COALESCE(q.votes, 0), q.user_id, u.nome
                FROM questions q
                LEFT JOIN usuarios u ON q.user_id = u.id
            """)
            return cursor.fetchall()
        finally:
            conn.close()

    def add_answer(self, question_id, answer):
        conn = get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            """)
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
        conn = get_connection()
        try:
            cursor = conn.execute("SELECT id, title, description FROM questions WHERE id = ?", (question_id,))
            return cursor.fetchone()
        finally:
            conn.close()

    def get_user_questions(self, user_id):
        conn = get_connection()
        try:
            cursor = conn.execute("""
                SELECT q.id, q.title, q.description, q.disciplina, COALESCE(q.votes, 0), q.user_id, u.nome
                FROM questions q
                LEFT JOIN usuarios u ON q.user_id = u.id
                WHERE q.user_id = ?
            """, (user_id,))
            return cursor.fetchall()
        finally:
            conn.close()

    def user_liked_question(self, user_id, question_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM likes WHERE user_id = ? AND question_id = ?", (user_id, question_id))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def like_question(self, user_id, question_id):
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
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM likes WHERE user_id = ? AND question_id = ?", (user_id, question_id))
        cursor.execute("UPDATE questions SET votes = votes - 1 WHERE id = ? AND votes > 0", (question_id,))
        conn.commit()
        conn.close()
