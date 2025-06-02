import tkinter as tk
from tkinter import messagebox
from controllers.question_controller import QuestionController
from controllers.user_controller import UserController

class PostQuestionScreen:
    def __init__(self, root, show_home):
        self.root = root
        self.show_home = show_home
        self.controller = QuestionController()
        self.user = UserController.get_logged_user()

        # Cria uma janela modal sobre a Home
        self.window = tk.Toplevel(self.root)
        self.window.title("Nova Dúvida - UniAjuda")
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
        y = (hs // 2) - (500 // 2)
        self.window.geometry(f"540x500+{x}+{y}")

        # Frame principal com sombra e bordas arredondadas
        self.bg_frame = tk.Frame(self.window, bg="#e9ecef")
        self.bg_frame.pack(fill=tk.BOTH, expand=True)
        self.card = tk.Frame(self.bg_frame, bg="#fff", bd=0, relief=tk.FLAT, highlightbackground="#b0bec5", highlightthickness=2)
        self.card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=540, height=500)

        tk.Label(self.card, text="Postar uma nova dúvida", font=("Arial", 22, "bold"), bg="#fff", fg="#0077b6").pack(pady=(28, 16))

        # Título
        title_label = tk.Label(self.card, text="Título da dúvida:", font=("Arial", 12, "bold"), bg="#fff")
        title_label.pack(anchor="w", padx=36, pady=(6, 0))
        self.title_entry = tk.Entry(self.card, font=("Arial", 12), width=38, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#0077b6")
        self.title_entry.pack(padx=36, pady=4)
        self.title_entry.insert(0, "Ex: Como usar listas em Python?")
        self.title_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.title_entry, "Ex: Como usar listas em Python?"))
        self.title_entry.bind('<FocusOut>', lambda e: self._restore_placeholder(self.title_entry, "Ex: Como usar listas em Python?"))

        # Disciplina
        disc_label = tk.Label(self.card, text="Disciplina:", font=("Arial", 12, "bold"), bg="#fff")
        disc_label.pack(anchor="w", padx=36, pady=(10, 0))
        self.disciplina_entry = tk.Entry(self.card, font=("Arial", 12), width=38, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#0077b6")
        self.disciplina_entry.pack(padx=36, pady=4)
        self.disciplina_entry.insert(0, "Ex: Algoritmos")
        self.disciplina_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.disciplina_entry, "Ex: Algoritmos"))
        self.disciplina_entry.bind('<FocusOut>', lambda e: self._restore_placeholder(self.disciplina_entry, "Ex: Algoritmos"))

        # Descrição
        desc_label = tk.Label(self.card, text="Descrição:", font=("Arial", 12, "bold"), bg="#fff")
        desc_label.pack(anchor="w", padx=36, pady=(10, 0))
        self.desc_text = tk.Text(self.card, font=("Arial", 12), width=38, height=6, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#0077b6")
        self.desc_text.pack(padx=36, pady=4)
        self.desc_text.insert("1.0", "Descreva sua dúvida com detalhes...")
        self.desc_text.bind('<FocusIn>', lambda e: self._clear_text_placeholder(self.desc_text, "Descreva sua dúvida com detalhes..."))
        self.desc_text.bind('<FocusOut>', lambda e: self._restore_text_placeholder(self.desc_text, "Descreva sua dúvida com detalhes..."))

        # Botões
        btn_frame = tk.Frame(self.card, bg="#fff")
        btn_frame.pack(pady=(22, 0))
        self.submit_btn = tk.Button(
            btn_frame, text="Postar Dúvida", font=("Arial", 13, "bold"), bg="#0077b6", fg="#fff",
            activebackground="#023e8a", activeforeground="#fff", bd=0, relief=tk.FLAT, width=18, height=2, cursor="hand2",
            command=self.submit_question
        )
        self.submit_btn.pack(side=tk.LEFT, padx=(0, 12))
        self.back_btn = tk.Button(
            btn_frame, text="Voltar", font=("Arial", 13), bg="#adb5bd", fg="#212529",
            activebackground="#6c757d", activeforeground="#fff", bd=0, relief=tk.FLAT, width=18, height=2, cursor="hand2",
            command=self.fechar_janela
        )
        self.back_btn.pack(side=tk.LEFT)

    def fechar_janela(self):
        self.window.destroy()

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#212529")
    def _restore_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="#adb5bd")
    def _clear_text_placeholder(self, text, placeholder):
        if text.get("1.0", tk.END).strip() == placeholder:
            text.delete("1.0", tk.END)
            text.config(fg="#212529")
    def _restore_text_placeholder(self, text, placeholder):
        if not text.get("1.0", tk.END).strip():
            text.insert("1.0", placeholder)
            text.config(fg="#adb5bd")

    def submit_question(self):
        title = self.title_entry.get().strip()
        disciplina = self.disciplina_entry.get().strip()
        desc = self.desc_text.get("1.0", tk.END).strip()
        if not title or title == "Ex: Como usar listas em Python?" or not disciplina or disciplina == "Ex: Algoritmos" or not desc or desc == "Descreva sua dúvida com detalhes...":
            messagebox.showwarning("Campos obrigatórios", "Preencha corretamente o título, a disciplina e a descrição da dúvida.")
            return
        if not self.user:
            messagebox.showerror("Erro", "Usuário não identificado.")
            return
        success = self.controller.create_question(title, desc, disciplina, self.user.id)
        if success:
            messagebox.showinfo("Sucesso", "Dúvida postada com sucesso!")
            self.show_home()
        else:
            messagebox.showerror("Erro", "Não foi possível postar a dúvida. Tente novamente.")
