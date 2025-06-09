import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController

class LoginScreen:
    def __init__(self, root, show_register, show_recover, show_home):
        # Inicializa a tela de login
        self.root = root
        self.show_register = show_register
        self.show_recover = show_recover
        self.show_home = show_home

        self._build_main_frame()
        self._build_title()
        self._build_form()
        self._build_buttons()

    def _build_main_frame(self):
        # Cria o frame principal com padding e cor de fundo
        self.frame = tk.Frame(self.root, bg="#f5f5f5", padx=40, pady=40)
        self.frame.pack(expand=True)

    def _build_title(self):
        # Título da tela
        tk.Label(
            self.frame, text="UniAjuda", font=("Arial", 22, "bold"),
            bg="#f5f5f5", fg="#2a4d69"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

    def _build_form(self):
        # Identificador
        tk.Label(
            self.frame, text="Matrícula ou E-mail:", font=("Arial", 13),
            bg="#f5f5f5"
        ).grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.identifier_entry = tk.Entry(self.frame, font=("Arial", 13), width=25)
        self.identifier_entry.grid(row=1, column=1, pady=8, ipadx=8, ipady=4)

        # Senha
        tk.Label(
            self.frame, text="Senha:", font=("Arial", 13),
            bg="#f5f5f5"
        ).grid(row=2, column=0, sticky="e", pady=8, padx=5)
        self.password_entry = tk.Entry(self.frame, show="*", font=("Arial", 13), width=25)
        self.password_entry.grid(row=2, column=1, pady=8, ipadx=8, ipady=4)

    def _build_buttons(self):
        # Entrar
        self.login_btn = tk.Button(
            self.frame, text="Entrar", font=("Arial", 13),
            bg="#2a4d69", fg="white", command=self.login
        )
        self.login_btn.grid(row=3, column=0, columnspan=2, pady=(15, 5), sticky="ew")

        # Cadastrar
        self.register_btn = tk.Button(
            self.frame, text="Cadastrar", font=("Arial", 13),
            command=self.show_register
        )
        self.register_btn.grid(row=4, column=0, columnspan=2, pady=5, sticky="ew")

        # Esqueci minha senha
        self.recover_btn = tk.Button(
            self.frame, text="Esqueci minha senha", font=("Arial", 11),
            command=self.show_recover
        )
        self.recover_btn.grid(row=5, column=0, columnspan=2, pady=(5, 0), sticky="ew")

    def login(self):
        # Método para autenticar o usuário
        identifier = self.identifier_entry.get()
        password = self.password_entry.get()

        user = UserController.authenticate_user(identifier, password)
        if user:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {user.name}!")
            self.show_home()  # Redireciona para a HomeScreen
        else:
            self.identifier_entry.config(bg="#ffcccc")
            self.password_entry.config(bg="#ffcccc")
            messagebox.showerror("Erro", "Matrícula/E-mail ou senha incorretos.")
