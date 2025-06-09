import tkinter as tk
from tkinter import messagebox
from controllers.question_controller import QuestionController
from controllers.answer_controller import AnswerController
from controllers.user_controller import UserController

class AnswerQuestionScreen:
    def __init__(self, root, show_home, question_id=None):
        self.root = root
        self.show_home = show_home
        self.question_controller = QuestionController()
        self.answer_controller = AnswerController()
        self.user = UserController.get_logged_user()
        self.question_id = question_id

        # Cria uma janela modal sobre a Home
        self.window = tk.Toplevel(self.root)
        self.window.title("Responder Dúvida - UniAjuda")
        self.window.configure(bg="#e9ecef")
        self.window.grab_set()
        self.window.resizable(False, False)
        self.window.transient(self.root)

        # Centralizar o modal na tela
        self.window.update_idletasks()
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = (ws // 2) - (540 // 2)
        y = (hs // 2) - (400 // 2)
        self.window.geometry(f"540x400+{x}+{y}")

        # Frame principal com sombra e bordas arredondadas
        self.bg_frame = tk.Frame(self.window, bg="#e9ecef")
        self.bg_frame.pack(fill=tk.BOTH, expand=True)
        self.card = tk.Frame(self.bg_frame, bg="#fff", bd=0, relief=tk.FLAT, highlightbackground="#b0bec5", highlightthickness=2)
        self.card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=540, height=400)

        tk.Label(self.card, text="Responder uma dúvida", font=("Arial", 22, "bold"), bg="#fff", fg="#0077b6").pack(pady=(28, 10))

        if self.question_id:
            q = self.question_controller.get_question_by_id(self.question_id)
            tk.Label(self.card, text=f"{q[1]}", font=("Arial", 15, "bold"), bg="#fff").pack(pady=(6, 0))
            tk.Label(self.card, text=f"{q[2]}", font=("Arial", 12), bg="#fff", fg="#495057", wraplength=420, justify="center").pack(pady=(0, 10))
        else:
            tk.Label(self.card, text="Dúvida não encontrada.", font=("Arial", 12), bg="#fff").pack(pady=20)
            return

        tk.Label(self.card, text="Sua resposta:", font=("Arial", 12, "bold"), bg="#fff").pack(anchor="w", padx=36, pady=(10, 0))
        self.answer_text = tk.Text(self.card, font=("Arial", 12), width=38, height=6, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#0077b6")
        self.answer_text.pack(padx=36, pady=4)
        self.answer_text.insert("1.0", "Digite sua resposta aqui...")
        self.answer_text.bind('<FocusIn>', lambda e: self._clear_text_placeholder(self.answer_text, "Digite sua resposta aqui..."))
        self.answer_text.bind('<FocusOut>', lambda e: self._restore_text_placeholder(self.answer_text, "Digite sua resposta aqui..."))

        btn_frame = tk.Frame(self.card, bg="#fff")
        btn_frame.pack(pady=(22, 0))
        self.submit_btn = tk.Button(
            btn_frame, text="Enviar Resposta", font=("Arial", 13, "bold"), bg="#0077b6", fg="#fff",
            activebackground="#023e8a", activeforeground="#fff", bd=0, relief=tk.FLAT, width=18, height=2, cursor="hand2",
            command=self.submit_answer
        )
        self.submit_btn.pack(side=tk.LEFT, padx=(0, 12))
        self.back_btn = tk.Button(
            btn_frame, text="Voltar", font=("Arial", 13), bg="#adb5bd", fg="#212529",
            activebackground="#6c757d", activeforeground="#fff", bd=0, relief=tk.FLAT, width=18, height=2, cursor="hand2",
            command=self.fechar_janela
        )
        self.back_btn.pack(side=tk.LEFT)

    def _clear_text_placeholder(self, text, placeholder):
        if text.get("1.0", tk.END).strip() == placeholder:
            text.delete("1.0", tk.END)
            text.config(fg="#212529")
    def _restore_text_placeholder(self, text, placeholder):
        if not text.get("1.0", tk.END).strip():
            text.insert("1.0", placeholder)
            text.config(fg="#adb5bd")

    def submit_answer(self):
        answer = self.answer_text.get("1.0", tk.END).strip()
        if not answer or answer == "Digite sua resposta aqui...":
            messagebox.showwarning("Campo obrigatório", "Escreva sua resposta antes de enviar.")
            return
        if not self.user:
            messagebox.showerror("Erro", "Usuário não identificado.")
            return
        success = self.answer_controller.add_answer(self.question_id, answer, self.user.id)
        if success:
            messagebox.showinfo("Sucesso", "Resposta enviada com sucesso!")
            self.show_home()
        else:
            messagebox.showerror("Erro", "Não foi possível enviar a resposta. Tente novamente.")

    def fechar_janela(self):
        self.window.destroy()
