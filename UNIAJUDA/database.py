import sqlite3

DB_NAME = "uniajuda.db"

def get_connection():
    # Retorna uma conexão com o banco de dados SQLite
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    # Cria a tabela de usuários, se não existir
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            registration TEXT UNIQUE NOT NULL,
            course TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            institution TEXT NOT NULL,
            password TEXT NOT NULL
        );
    """)
    # Cria a tabela de dúvidas (questions) com user_id, disciplina, votes e anexo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            subject TEXT,
            votes INTEGER DEFAULT 0,
            user_id INTEGER,
            attachment TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    # Cria a tabela de respostas (answers) com user_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (question_id) REFERENCES questions(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    # Cria a tabela de denúncias (reports)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            reason TEXT NOT NULL,
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );
    """)
    # Cria a tabela de likes (curtidas) para registrar curtidas de usuários em perguntas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            UNIQUE(user_id, question_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (question_id) REFERENCES questions(id)
        );
    """)
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()   # Fecha a conexão

def limpar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM questions;")
    cursor.execute("DELETE FROM answers;")
    cursor.execute("DELETE FROM reports;")
    cursor.execute("DELETE FROM likes;")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    # Descomente a linha abaixo para limpar o banco ao rodar o arquivo
    # limpar_banco()

