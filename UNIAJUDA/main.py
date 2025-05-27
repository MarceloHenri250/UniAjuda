import tkinter as tk
from database import create_tables
from gui.login_screen import LoginScreen
from gui.register_screen import RegisterScreen
from gui.recover_screen import RecoverScreen

def main():
    # Inicializa a aplicação UniAjuda

    # Cria as tabelas do banco de dados caso ainda não existam
    create_tables()

    # Cria a janela principal do Tkinter
    root = tk.Tk()
    root.title("UniAjuda - Plataforma de Apoio Acadêmico")
    root.state('zoomed')  # Deixa a janela maximizada ao abrir
    root.configure(bg="#f5f5f5")  # Define a cor de fundo da janela

    def clear_window():
        # Função para remover todos os widgets da janela antes de trocar de tela
        for widget in root.winfo_children():
            widget.destroy()

    def show_login():
        # Mostra a tela de login
        clear_window()
        LoginScreen(root, show_register, show_recover)

    def show_register():
        # Mostra a tela de cadastro
        clear_window()
        RegisterScreen(root, show_login)

    def show_recover():
        # Mostra a tela de recuperação de senha
        clear_window()
        RecoverScreen(root, show_login)

    # Começa mostrando a tela de login
    show_login()
    root.mainloop()

if __name__ == "__main__":
    main()