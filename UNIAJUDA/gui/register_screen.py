import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController
import re

class RegisterScreen:
    def __init__(self, root, show_login):
        # Inicializa a tela de cadastro
        self.root = root
        self.show_login = show_login

        # Cria o frame principal com padding e cor de fundo
        self.frame = tk.Frame(root, bg="#f5f5f5", padx=40, pady=40)
        self.frame.pack(expand=True)

        # Título da tela
        tk.Label(
            self.frame,
            text="Cadastro",
            font=("Arial", 22, "bold"),
            bg="#f5f5f5",
            fg="#2a4d69"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Lista de labels dos campos do formulário
        labels = [
            "Nome:", "Matrícula:", "Curso:",
            "E-mail:", "Instituição:", "Senha:", "Confirmar Senha:"
        ]
        self.entries = []

        # Cria os campos de entrada (Entry) para cada label
        for i, label in enumerate(labels):
            tk.Label(
                self.frame,
                text=label,
                font=("Arial", 13),
                bg="#f5f5f5"
            ).grid(row=i+1, column=0, sticky="e", pady=8, padx=5)

            # Campos de senha ficam ocultos
            entry = tk.Entry(
                self.frame,
                font=("Arial", 13),
                width=25,
                show="*" if "Senha" in label else ""
            )
            entry.grid(row=i+1, column=1, pady=8, ipadx=8, ipady=4)
            self.entries.append(entry)

        # Botão de cadastro
        self.register_btn = tk.Button(
            self.frame,
            text="Cadastrar",
            font=("Arial", 13),
            bg="#2a4d69",
            fg="white",
            command=self.register
        )
        self.register_btn.grid(row=8, column=0, columnspan=2, pady=(15, 5), sticky="ew")

        # Botão para voltar à tela de login
        self.back_btn = tk.Button(
            self.frame,
            text="Voltar",
            font=("Arial", 13),
            command=self.show_login
        )
        self.back_btn.grid(row=9, column=0, columnspan=2, pady=5, sticky="ew")

    def register(self):
        # Obtém os valores dos campos
        name, registration, course, email, institution, password, confirm_password = [e.get() for e in self.entries]
        error = False

        # Reseta a cor de fundo dos campos
        for entry in self.entries:
            entry.config(bg="white")

        # Validação de senha forte: pelo menos 8 caracteres, uma letra maiúscula e um número
        strong_password = (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'\d', password)
        )

        # Verifica se todos os campos foram preenchidos
        if not all([name, registration, course, email, institution, password, confirm_password]):
            messagebox.showerror("Erro", "Preencha todos os campos.")
            error = True

        # Valida a força da senha
        if not strong_password:
            self.entries[5].config(bg="#ffcccc")
            messagebox.showerror(
                "Erro",
                "A senha deve ter pelo menos 8 caracteres, uma letra maiúscula e um número."
            )
            error = True

        # Verifica se as senhas coincidem
        if password != confirm_password:
            self.entries[5].config(bg="#ffcccc")
            self.entries[6].config(bg="#ffcccc")
            messagebox.showerror("Erro", "As senhas não coincidem.")
            error = True

        # Se houve erro, interrompe o cadastro
        if error:
            return

        # Tenta cadastrar o usuário usando o UserController
        if UserController.register_user(name, registration, course, email, institution, password):
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.show_login()
        else:
            # Matrícula ou e-mail já cadastrados
            self.entries[1].config(bg="#ffcccc")
            self.entries[3].config(bg="#ffcccc")
            messagebox.showerror("Erro", "Matrícula ou e-mail já cadastrados.")