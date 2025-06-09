import sqlite3
from models.user import User
from database import get_connection

class UserController:
    @staticmethod
    def register_user(name, registration, course, email, institution, password, avatar=None):
        # Cadastra um novo usuário no sistema.
        conn = get_connection()
        try:
            conn.execute(
                """
                INSERT INTO users (name, registration, course, email, institution, password, avatar)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, registration, course, email, institution, password, avatar)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def authenticate_user(identifier, password):
        # Autentica o usuário com base na matrícula ou email e senha.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, name, registration, course, email, institution, password, avatar
            FROM users
            WHERE (registration = ? OR email = ?) AND password = ?
            """,
            (identifier, identifier, password)
        )
        row = cursor.fetchone()
        conn.close()
        return User(*row) if row else None

    @staticmethod
    def update_password(email, new_password):
        # Atualiza a senha do usuário com base no email.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password = ? WHERE email = ?",
            (new_password, email)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success

    @staticmethod
    def email_exists(email):
        # Verifica se o email já está cadastrado.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE email = ?",
            (email,)
        )
        exists = cursor.fetchone() is not None
        conn.close()
        return exists

    @staticmethod
    def get_logged_user():
        # Exemplo: retorna o primeiro usuário cadastrado (ajuste para autenticação real)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, registration, course, email, institution, password, avatar FROM users LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return User(*row) if row else None

    @staticmethod
    def update_user(user_id, name, course, institution, avatar=None):
        # Atualiza os dados do usuário
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET name = ?, course = ?, institution = ?, avatar = ? WHERE id = ?",
            (name, course, institution, avatar, user_id)
        )
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
