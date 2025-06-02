import tkinter as tk
from tkinter import messagebox
from controllers.question_controller import QuestionController
from controllers.report_controller import ReportController

class ReportScreen:
    def __init__(self, root, show_home, question_id=None):
        self.root = root
        self.show_home = show_home
        self.q_controller = QuestionController()
        self.r_controller = ReportController()
        self.question_id = question_id

        # Cria uma janela modal sobre a Home
        self.window = tk.Toplevel(self.root)
        self.window.title("Denunciar Postagem - UniAjuda")
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
        y = (hs // 2) - (370 // 2)
        self.window.geometry(f"540x370+{x}+{y}")

        # Frame principal com sombra e bordas arredondadas
        self.bg_frame = tk.Frame(self.window, bg="#e9ecef")
        self.bg_frame.pack(fill=tk.BOTH, expand=True)
        self.card = tk.Frame(self.bg_frame, bg="#fff", bd=0, relief=tk.FLAT, highlightbackground="#d90429", highlightthickness=2)
        self.card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=540, height=370)

        tk.Label(self.card, text="Denunciar uma postagem", font=("Arial", 22, "bold"), bg="#fff", fg="#d90429").pack(pady=(28, 10))

        if self.question_id:
            q = self.q_controller.get_question_by_id(self.question_id)
            tk.Label(self.card, text=f"{q[1]}", font=("Arial", 15, "bold"), bg="#fff").pack(pady=(6, 0))
            tk.Label(self.card, text=f"{q[2]}", font=("Arial", 12), bg="#fff", fg="#495057", wraplength=420, justify="center").pack(pady=(0, 10))
        else:
            tk.Label(self.card, text="Dúvida não encontrada.", font=("Arial", 12), bg="#fff").pack(pady=20)
            return

        tk.Label(self.card, text="Motivo da denúncia:", font=("Arial", 12, "bold"), bg="#fff").pack(anchor="w", padx=36, pady=(10, 0))
        self.reason_text = tk.Text(self.card, font=("Arial", 12), width=38, height=4, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#d90429")
        self.reason_text.pack(padx=36, pady=4)
        self.reason_text.insert("1.0", "Descreva o motivo da denúncia...")
        self.reason_text.bind('<FocusIn>', lambda e: self._clear_text_placeholder(self.reason_text, "Descreva o motivo da denúncia..."))
        self.reason_text.bind('<FocusOut>', lambda e: self._restore_text_placeholder(self.reason_text, "Descreva o motivo da denúncia..."))

        btn_frame = tk.Frame(self.card, bg="#fff")
        btn_frame.pack(pady=(22, 0))
        self.submit_btn = tk.Button(
            btn_frame, text="Enviar Denúncia", font=("Arial", 13, "bold"), bg="#d90429", fg="#fff",
            activebackground="#a30015", activeforeground="#fff", bd=0, relief=tk.FLAT, width=18, height=2, cursor="hand2",
            command=self.submit_report
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

    def submit_report(self):
        reason = self.reason_text.get("1.0", tk.END).strip()
        if not reason or reason == "Descreva o motivo da denúncia...":
            messagebox.showwarning("Campo obrigatório", "Descreva o motivo da denúncia antes de enviar.")
            return
        success = self.r_controller.add_report(self.question_id, reason)
        if success:
            messagebox.showinfo("Sucesso", "Denúncia enviada com sucesso!")
            self.show_home()
        else:
            messagebox.showerror("Erro", "Não foi possível enviar a denúncia. Tente novamente.")

    def fechar_janela(self):
        self.window.destroy()
