import tkinter as tk
from database import create_tables
from gui.login_screen import LoginScreen
from gui.register_screen import RegisterScreen
from gui.recover_screen import RecoverScreen
from gui.home_screen import HomeScreen

# =============================
# Função principal da aplicação
# =============================
def main():
    # Inicializa a aplicação UniAjuda
    create_tables()  # Garante as tabelas do banco

    root = tk.Tk()
    root.title("UniAjuda - Plataforma de Apoio Acadêmico")
    root.state('zoomed')
    root.configure(bg="#f5f5f5")

    def clear_window():
        # Remove todos os widgets antes de trocar de tela principal
        for widget in root.winfo_children():
            widget.destroy()

    # =============================
    # Funções de navegação principal
    # =============================
    def show_home():
        clear_window()
        HomeScreen(root, show_home)

    def show_login():
        clear_window()
        LoginScreen(root, show_register, show_recover, show_home)

    def show_register():
        clear_window()
        RegisterScreen(root, show_login)

    def show_recover():
        clear_window()
        RecoverScreen(root, show_login)

    # Inicia sempre pela tela de login
    show_login()
    root.mainloop()

if __name__ == "__main__":
    main()