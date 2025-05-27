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
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT UNIQUE NOT NULL,
            curso TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            instituicao TEXT NOT NULL,
            senha TEXT NOT NULL
        );
    """)
    conn.commit()  # Salva as alterações no banco de dados
    conn.close()   # Fecha a conexão

def limpar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios;")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    # Descomente a linha abaixo para limpar o banco ao rodar o arquivo
    # limpar_banco()

