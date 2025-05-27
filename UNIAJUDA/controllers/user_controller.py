import sqlite3
from models.user import User
from database import get_connection

class UserController:
    @staticmethod
    def cadastrar_usuario(nome, matricula, curso, email, instituicao, senha):
        # Cadastra um novo usuário no sistema.
        conn = get_connection()
        try:
            conn.execute(
                """
                INSERT INTO usuarios (nome, matricula, curso, email, instituicao, senha)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (nome, matricula, curso, email, instituicao, senha)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def autenticar_usuario(identificador, senha):
        # Autentica o usuário com base na matrícula ou email e senha.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, nome, matricula, curso, email, instituicao, senha
            FROM usuarios
            WHERE (matricula = ? OR email = ?) AND senha = ?
            """,
            (identificador, identificador, senha)
        )
        row = cursor.fetchone()
        conn.close()
        return User(*row) if row else None

    @staticmethod
    def atualizar_senha(email, nova_senha):
        # Atualiza a senha do usuário com base no email.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE email = ?",
            (nova_senha, email)
        )
        conn.commit()
        sucesso = cursor.rowcount > 0
        conn.close()
        return sucesso

    @staticmethod
    def email_existe(email):
        # Verifica se o email já está cadastrado.
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM usuarios WHERE email = ?",
            (email,)
        )
        existe = cursor.fetchone() is not None
        conn.close()
        return existe
