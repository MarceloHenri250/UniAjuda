import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from controllers.question_controller import QuestionController
from controllers.user_controller import UserController

class PostQuestionScreen:
    def __init__(self, root, show_home):
        self.root = root
        self.show_home = show_home
        self.question_controller = QuestionController()
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

        # Frame principal
        self.bg_frame = tk.Frame(self.window, bg="#e9ecef")
        self.bg_frame.pack(fill=tk.BOTH, expand=True)
        self.card = tk.Frame(self.bg_frame, bg="#fff", bd=0, relief=tk.FLAT, highlightbackground="#b0bec5", highlightthickness=2)
        self.card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=520, height=480)

        # Título principal
        tk.Label(self.card, text="Postar uma nova dúvida", font=("Arial", 22, "bold"), bg="#fff", fg="#0077b6").grid(row=0, column=0, columnspan=2, pady=(24, 18))

        # Título da dúvida
        title_label = tk.Label(self.card, text="Título da dúvida:", font=("Arial", 12, "bold"), bg="#fff")
        title_label.grid(row=1, column=0, sticky="w", padx=(36, 8), pady=(4, 0))
        self.title_entry = tk.Entry(self.card, font=("Arial", 12), width=36, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#0077b6", fg="#adb5bd")
        self.title_entry.grid(row=1, column=1, padx=(0, 36), pady=(4, 0), sticky="ew")
        self.title_entry.insert(0, "Ex: Como usar listas em Python?")
        self.title_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.title_entry, "Ex: Como usar listas em Python?"))
        self.title_entry.bind('<FocusOut>', lambda e: self._restore_placeholder(self.title_entry, "Ex: Como usar listas em Python?"))
        self.title_entry.focus_set()

        # Disciplina
        disc_label = tk.Label(self.card, text="Disciplina:", font=("Arial", 12, "bold"), bg="#fff")
        disc_label.grid(row=2, column=0, sticky="w", padx=(36, 8), pady=(10, 0))
        self.subject_entry = tk.Entry(self.card, font=("Arial", 12), width=36, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#0077b6", fg="#adb5bd")
        self.subject_entry.grid(row=2, column=1, padx=(0, 36), pady=(10, 0), sticky="ew")
        self.subject_entry.insert(0, "Ex: Algoritmos")
        self.subject_entry.bind('<FocusIn>', lambda e: self._clear_placeholder(self.subject_entry, "Ex: Algoritmos"))
        self.subject_entry.bind('<FocusOut>', lambda e: self._restore_placeholder(self.subject_entry, "Ex: Algoritmos"))

        # Descrição
        desc_label = tk.Label(self.card, text="Descrição:", font=("Arial", 12, "bold"), bg="#fff")
        desc_label.grid(row=3, column=0, sticky="nw", padx=(36, 8), pady=(10, 0))
        self.desc_text = tk.Text(self.card, font=("Arial", 12), width=36, height=5, relief=tk.GROOVE, bd=2, highlightthickness=1, highlightcolor="#0077b6", fg="#adb5bd")
        self.desc_text.grid(row=3, column=1, padx=(0, 36), pady=(10, 0), sticky="ew")
        self.desc_text.insert("1.0", "Descreva sua dúvida com detalhes...")
        self.desc_text.bind('<FocusIn>', lambda e: self._clear_text_placeholder(self.desc_text, "Descreva sua dúvida com detalhes..."))
        self.desc_text.bind('<FocusOut>', lambda e: self._restore_text_placeholder(self.desc_text, "Descreva sua dúvida com detalhes..."))

        # Anexo (arquivo ou link)
        attachment_label = tk.Label(self.card, text="Anexo (opcional):", font=("Arial", 12, "bold"), bg="#fff")
        attachment_label.grid(row=4, column=0, sticky="w", padx=(36, 8), pady=(10, 0))
        self.attachment_var = tk.StringVar()
        attach_frame = tk.Frame(self.card, bg="#fff")
        attach_frame.grid(row=4, column=1, padx=(0, 36), pady=(10, 0), sticky="ew")
        self.attachment_entry = tk.Entry(attach_frame, textvariable=self.attachment_var, font=("Arial", 12), width=28, relief=tk.GROOVE, bd=2, fg="#495057")
        self.attachment_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        btn_file = tk.Button(
            attach_frame, text="📎", font=("Arial", 13), bg="#f1f3f4", fg="#0077b6",
            activebackground="#e0e7ef", bd=1, relief=tk.RAISED,
            command=self.selecionar_anexo, cursor="hand2", width=2, height=1
        )
        btn_file.pack(side=tk.LEFT, padx=(6, 0))
        # Tooltip para o botão de anexo
        self._add_tooltip(btn_file, "Selecionar arquivo para anexar")

        # Botões
        btn_frame = tk.Frame(self.card, bg="#fff")
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(28, 0))
        self.submit_btn = tk.Button(
            btn_frame, text="Postar Dúvida", font=("Arial", 13, "bold"), bg="#0077b6", fg="#fff",
            activebackground="#023e8a", activeforeground="#fff", bd=0, relief=tk.FLAT, width=16, height=2, cursor="hand2",
            command=self.submit_question
        )
        self.submit_btn.pack(side=tk.LEFT, padx=(0, 16))
        self.back_btn = tk.Button(
            btn_frame, text="Voltar", font=("Arial", 13), bg="#adb5bd", fg="#212529",
            activebackground="#6c757d", activeforeground="#fff", bd=0, relief=tk.FLAT, width=16, height=2, cursor="hand2",
            command=self.fechar_janela
        )
        self.back_btn.pack(side=tk.LEFT)

        # Ajuste de grid para responsividade
        self.card.grid_rowconfigure(3, weight=1)
        self.card.grid_columnconfigure(1, weight=1)

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

    def selecionar_anexo(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            import os
            filename = os.path.basename(file_path)
            self.attachment_var.set(filename)

    def _add_tooltip(self, widget, text):
        # Tooltip simples para widgets
        def on_enter(event):
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            x = widget.winfo_rootx() + 40
            y = widget.winfo_rooty() + 20
            self.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(self.tooltip, text=text, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("Arial", 9))
            label.pack(ipadx=4)
        def on_leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def submit_question(self):
        title = self.title_entry.get().strip()
        subject = self.subject_entry.get().strip()
        desc = self.desc_text.get("1.0", tk.END).strip()
        attachment = self.attachment_var.get().strip() if hasattr(self, 'attachment_var') else None
        if not title or title == "Ex: Como usar listas em Python?" or not subject or subject == "Ex: Algoritmos" or not desc or desc == "Descreva sua dúvida com detalhes...":
            messagebox.showwarning("Campos obrigatórios", "Preencha corretamente o título, a disciplina e a descrição da dúvida.")
            return
        if not self.user:
            messagebox.showerror("Erro", "Usuário não identificado.")
            return
        success = self.question_controller.create_question(title, desc, subject, self.user.id, attachment)
        if success:
            messagebox.showinfo("Sucesso", "Dúvida postada com sucesso!")
            self.show_home()
            self.fechar_janela()
        else:
            messagebox.showerror("Erro", "Não foi possível postar a dúvida. Tente novamente.")
