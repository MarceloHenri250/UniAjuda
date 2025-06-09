import tkinter as tk
from tkinter import messagebox
from controllers.user_controller import UserController
import re

class RecoverScreen:
    def __init__(self, root, show_login):
        # Inicializa a tela de recuperação de senha
        self.root = root
        self.show_login = show_login

        # Frame principal
        self.frame = tk.Frame(root, bg="#f5f5f5", padx=40, pady=40)
        self.frame.pack(expand=True)

        # Título
        tk.Label(
            self.frame, text="Recuperar Senha",
            font=("Arial", 22, "bold"), bg="#f5f5f5", fg="#2a4d69"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Campo de e-mail
        tk.Label(
            self.frame, text="E-mail cadastrado:",
            font=("Arial", 13), bg="#f5f5f5"
        ).grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.email_entry = tk.Entry(self.frame, font=("Arial", 13), width=25)
        self.email_entry.grid(row=1, column=1, pady=8, ipadx=8, ipady=4)

        # Botão para verificar e-mail
        self.verify_btn = tk.Button(
            self.frame, text="Verificar",
            font=("Arial", 13), bg="#2a4d69", fg="white",
            command=self.verify_email
        )
        self.verify_btn.grid(row=2, column=0, columnspan=2, pady=(5, 15), sticky="ew")

        # Campo para nova senha (desabilitado inicialmente)
        tk.Label(
            self.frame, text="Nova Senha:",
            font=("Arial", 13), bg="#f5f5f5"
        ).grid(row=3, column=0, sticky="e", pady=8, padx=5)
        self.new_password_entry = tk.Entry(self.frame, font=("Arial", 13), width=25, show="*")
        self.new_password_entry.grid(row=3, column=1, pady=8, ipadx=8, ipady=4)
        self.new_password_entry.config(state="disabled")

        # Campo para confirmação de senha (desabilitado inicialmente)
        tk.Label(
            self.frame, text="Confirmação da Senha:",
            font=("Arial", 13), bg="#f5f5f5"
        ).grid(row=4, column=0, sticky="e", pady=8, padx=5)
        self.confirm_password_entry = tk.Entry(self.frame, font=("Arial", 13), width=25, show="*")
        self.confirm_password_entry.grid(row=4, column=1, pady=8, ipadx=8, ipady=4)
        self.confirm_password_entry.config(state="disabled")

        # Botão para redefinir senha (desabilitado inicialmente)
        self.recover_btn = tk.Button(
            self.frame, text="Redefinir Senha",
            font=("Arial", 13), bg="#2a4d69", fg="white",
            command=self.recover
        )
        self.recover_btn.grid(row=5, column=0, columnspan=2, pady=(15, 5), sticky="ew")
        self.recover_btn.config(state="disabled")

        # Botão para voltar à tela de login
        self.back_btn = tk.Button(
            self.frame, text="Voltar",
            font=("Arial", 13), command=self.show_login
        )
        self.back_btn.grid(row=6, column=0, columnspan=2, pady=5, sticky="ew")

    def verify_email(self):
        # Verifica se o e-mail existe no sistema
        email = self.email_entry.get()
        self.email_entry.config(bg="white")

        if not email:
            self.email_entry.config(bg="#ffcccc")
            messagebox.showerror("Erro", "Preencha o e-mail.")
            return

        if UserController.email_exists(email):
            # Habilita os campos de senha
            self.new_password_entry.config(state="normal")
            self.confirm_password_entry.config(state="normal")
            self.recover_btn.config(state="normal")
            messagebox.showinfo("Sucesso", "E-mail encontrado! Agora defina sua nova senha.")
        else:
            self.email_entry.config(bg="#ffcccc")
            messagebox.showerror("Erro", "E-mail não encontrado.")

    def recover(self):
        # Recupera os valores das entradas de nova senha e confirmação
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        error = False

        # Resetar cores dos campos
        self.new_password_entry.config(bg="white")
        self.confirm_password_entry.config(bg="white")

        # Validação de senha forte
        strong_password = (
            len(new_password) >= 8 and
            re.search(r'[A-Z]', new_password) and
            re.search(r'\d', new_password)
        )

        if not strong_password:
            self.new_password_entry.config(bg="#ffcccc")
            messagebox.showerror(
                "Erro",
                "A senha deve ter pelo menos 8 caracteres, uma letra maiúscula e um número."
            )
            error = True

        # Verifica se as senhas coincidem
        if new_password != confirm_password:
            self.new_password_entry.config(bg="#ffcccc")
            self.confirm_password_entry.config(bg="#ffcccc")
            messagebox.showerror("Erro", "As senhas não coincidem.")
            error = True

        if error:
            return

        # Atualiza a senha no sistema
        email = self.email_entry.get()
        if UserController.update_password(email, new_password):
            messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
            self.show_login()
        else:
            messagebox.showerror("Erro", "Erro ao redefinir senha.")