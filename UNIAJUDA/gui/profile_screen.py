import tkinter as tk
from tkinter import messagebox
from controllers.question_controller import QuestionController
from controllers.answer_controller import AnswerController
from controllers.user_controller import UserController

class ProfileScreen:
    def __init__(self, parent, logout_callback):
        self.parent = parent
        self.logout_callback = logout_callback
        self.question_controller = QuestionController()
        self.answer_controller = AnswerController()
        self.render_profile()

    def render_profile(self):
        user = UserController.get_logged_user()
        for widget in self.parent.winfo_children():
            widget.destroy()
        tk.Label(self.parent, text="Meu Perfil", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#0077b6").pack(pady=(25, 12))
        if user:
            tk.Label(self.parent, text=f"Nome: {user.name}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
            tk.Label(self.parent, text=f"Matrícula: {user.registration}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
            tk.Label(self.parent, text=f"Curso: {user.course}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
            tk.Label(self.parent, text=f"E-mail: {user.email}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
            tk.Label(self.parent, text=f"Instituição: {user.institution}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
        else:
            tk.Label(self.parent, text="Usuário não identificado.", font=("Arial", 13), bg="#f8fafc", fg="#d90429").pack(anchor="w", padx=30)
            return
        # Minhas Perguntas
        tk.Label(self.parent, text="Minhas Perguntas:", font=("Arial", 13, "bold"), bg="#f8fafc", fg="#0077b6").pack(anchor="w", padx=30, pady=(20, 0))
        questions = self.question_controller.get_user_questions(user.id)
        if questions:
            for q in questions:
                tk.Label(self.parent, text=f"- {q[1]} (Disciplina: {q[3]})", font=("Arial", 12), bg="#f1f3f4", fg="#212529", anchor="w", wraplength=600, justify="left").pack(fill=tk.X, padx=40, pady=(0, 2))
        else:
            tk.Label(self.parent, text="Nenhuma pergunta cadastrada.", font=("Arial", 11, "italic"), bg="#f8fafc", fg="#adb5bd").pack(anchor="w", padx=40)
        # Minhas Respostas
        tk.Label(self.parent, text="Minhas Respostas:", font=("Arial", 13, "bold"), bg="#f8fafc", fg="#0077b6").pack(anchor="w", padx=30, pady=(20, 0))
        answers = self.answer_controller.get_user_answers(user.id)
        if answers:
            for a in answers:
                tk.Label(self.parent, text=f"- {a[2]} (Pergunta ID: {a[1]})", font=("Arial", 12), bg="#f1f3f4", fg="#212529", anchor="w", wraplength=600, justify="left").pack(fill=tk.X, padx=40, pady=(0, 2))
        else:
            tk.Label(self.parent, text="Nenhuma resposta cadastrada.", font=("Arial", 11, "italic"), bg="#f8fafc", fg="#adb5bd").pack(anchor="w", padx=40)
        # Botão de sair
        tk.Button(self.parent, text="Sair", font=("Arial", 12, "bold"), bg="#adb5bd", fg="#212529", activebackground="#6c757d", activeforeground="#fff", bd=0, relief=tk.FLAT, width=12, height=1, cursor="hand2", command=self.logout).pack(pady=(30, 0))

    def logout(self):
        if tk.messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
            self.logout_callback()
