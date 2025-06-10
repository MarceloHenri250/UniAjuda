import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from controllers.question_controller import QuestionController
from controllers.answer_controller import AnswerController
from controllers.user_controller import UserController

class ProfileScreen:
    def __init__(self, parent, logout_callback):
        self.parent = parent
        self.logout_callback = logout_callback
        self.question_controller = QuestionController()
        self.answer_controller = AnswerController()
        self.avatar_path = None
        self.edit_mode = False
        self.render_profile()

    def render_profile(self):
        user = UserController.get_logged_user()
        self._clear_screen()
        self.parent.update_idletasks()
        # Frame central expansivo
        center_frame = tk.Frame(self.parent, bg="#f8fafc")
        center_frame.pack(expand=True, fill=tk.BOTH)
        center_inner = tk.Frame(center_frame, bg="#f8fafc")
        center_inner.place(relx=0.5, rely=0.5, anchor="center")
        # Título
        tk.Label(center_inner, text="Meu Perfil", font=("Segoe UI", 30, "bold"), bg="#f8fafc", fg="#0077b6").pack(pady=(18, 10))
        # Card horizontal
        card = tk.Frame(center_inner, bg="#fff", bd=0, relief=tk.FLAT, highlightbackground="#b0bec5", highlightthickness=2)
        card.pack(pady=(0, 28), padx=10, fill=tk.BOTH, expand=True)
        card.configure(borderwidth=0)
        # Layout horizontal: avatar à esquerda, info à direita
        card.grid_columnconfigure(0, weight=0)
        card.grid_columnconfigure(1, weight=1)
        card.grid_rowconfigure(0, weight=1)
        avatar_side = tk.Frame(card, bg="#fff")
        avatar_side.grid(row=0, column=0, sticky="nsw", padx=(32, 24), pady=24)
        self._render_avatar(user, parent=avatar_side)
        info_side = tk.Frame(card, bg="#fff")
        info_side.grid(row=0, column=1, sticky="nsew", pady=24, padx=(0, 32))
        # Inicializa variáveis editáveis sempre que renderiza
        self.name_var = tk.StringVar(value=user.name)
        self.course_var = tk.StringVar(value=user.course)
        self._render_fields(user, parent=info_side)
        # Botões de ação (abaixo do card, centralizados)
        btns_frame = tk.Frame(center_inner, bg="#f8fafc")
        btns_frame.pack(pady=(0, 10))
        if self.edit_mode:
            self._render_save_button(parent=btns_frame)
        else:
            self._render_edit_button(parent=btns_frame)
        # Botão Sair
        self._render_logout_button(parent=center_inner)

    def _clear_screen(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def _render_avatar(self, user, parent=None):
        parent = parent or self.parent
        avatar_frame = tk.Frame(parent, bg="#f8fafc")
        avatar_frame.pack(pady=(0, 10))
        # Usa avatar_path temporário se estiver em edição e um novo avatar foi selecionado
        avatar_path = self.avatar_path if self.edit_mode and self.avatar_path else user.avatar
        avatar_img = self._get_avatar_image(avatar_path, size=120)
        # Avatar circular com fallback
        avatar_canvas = tk.Canvas(avatar_frame, width=120, height=120, bg="#f8fafc", highlightthickness=0)
        avatar_canvas.create_oval(5, 5, 115, 115, fill="#e0e7ef", outline="#b0bec5", width=2)
        avatar_canvas.create_image(60, 60, image=avatar_img)
        avatar_canvas.image = avatar_img
        avatar_canvas.pack()
        if self.edit_mode:
            btn_avatar = tk.Button(
                avatar_frame, text="Alterar Avatar", font=("Segoe UI", 11),
                command=self._change_avatar, bg="#e0e7ef", fg="#0077b6",
                bd=0, relief=tk.FLAT, cursor="hand2", activebackground="#d0e7f7"
            )
            btn_avatar.pack(pady=(8, 0))
            btn_avatar.bind('<Enter>', lambda e: btn_avatar.config(bg="#b0bec5"))
            btn_avatar.bind('<Leave>', lambda e: btn_avatar.config(bg="#e0e7ef"))
        avatar_frame.pack(anchor="center")

    def _render_fields(self, user, parent=None):
        parent = parent or self.parent
        form_frame = tk.Frame(parent, bg="#fff")
        form_frame.pack(pady=(0, 10), fill=tk.X)
        labels = ["Nome:", "Matrícula:", "Curso:", "E-mail:", "Instituição:"]
        values = [user.name, user.registration, user.course, user.email, user.institution]
        for i, (label, value) in enumerate(zip(labels, values)):
            tk.Label(form_frame, text=label, font=("Segoe UI", 13, "bold"), bg="#fff").grid(row=i, column=0, sticky="e", padx=8, pady=4)
            if self.edit_mode and label == "Nome:":
                entry = tk.Entry(form_frame, textvariable=self.name_var, font=("Segoe UI", 13), width=max(28, len(self.name_var.get())+2),
                                 bg="#f4f8fb", fg="#212529", relief=tk.FLAT, highlightthickness=2, highlightbackground="#b0bec5", highlightcolor="#0077b6")
                entry.grid(row=i, column=1, sticky="w", pady=4, ipady=4, ipadx=4)
                entry.configure(bd=0, insertbackground="#0077b6")
                entry.after(100, lambda e=entry: e.focus_set())
            elif self.edit_mode and label == "Curso:":
                entry = tk.Entry(form_frame, textvariable=self.course_var, font=("Segoe UI", 13), width=max(28, len(self.course_var.get())+2),
                                 bg="#f4f8fb", fg="#212529", relief=tk.FLAT, highlightthickness=2, highlightbackground="#b0bec5", highlightcolor="#0077b6")
                entry.grid(row=i, column=1, sticky="w", pady=4, ipady=4, ipadx=4)
                entry.configure(bd=0, insertbackground="#0077b6")
            else:
                tk.Label(form_frame, text=value, font=("Segoe UI", 13), bg="#fff").grid(row=i, column=1, sticky="w", pady=4)

    def _render_edit_button(self, parent=None):
        parent = parent or self.parent
        # Evita múltiplos botões
        for widget in parent.winfo_children():
            widget.destroy()
        btn = tk.Button(
            parent, text="Editar Perfil", font=("Segoe UI", 12, "bold"),
            bg="#0077b6", fg="#fff", activebackground="#023e8a",
            activeforeground="#fff", bd=0, relief=tk.FLAT, width=18, height=1,
            cursor="hand2", command=self._enable_edit
        )
        btn.pack(pady=(10, 0))
        btn.bind('<Enter>', lambda e: btn.config(bg="#023e8a"))
        btn.bind('<Leave>', lambda e: btn.config(bg="#0077b6"))

    def _enable_edit(self):
        self.edit_mode = True
        self.render_profile()

    def _render_save_button(self, parent=None):
        parent = parent or self.parent
        # Evita múltiplos botões
        for widget in parent.winfo_children():
            widget.destroy()
        btn = tk.Button(
            parent, text="Salvar Alterações", font=("Segoe UI", 12, "bold"),
            bg="#0077b6", fg="#fff", activebackground="#023e8a",
            activeforeground="#fff", bd=0, relief=tk.FLAT, width=18, height=1,
            cursor="hand2", command=self._save_changes
        )
        btn.pack(pady=(10, 0))
        btn.bind('<Enter>', lambda e: btn.config(bg="#023e8a"))
        btn.bind('<Leave>', lambda e: btn.config(bg="#0077b6"))

    def _render_logout_button(self, parent=None):
        parent = parent or self.parent
        btn = tk.Button(
            parent, text="Sair", font=("Segoe UI", 12, "bold"),
            bg="#adb5bd", fg="#212529", activebackground="#6c757d",
            activeforeground="#fff", bd=0, relief=tk.FLAT, width=12, height=1,
            cursor="hand2", command=self.logout
        )
        btn.pack(pady=(30, 0))
        btn.bind('<Enter>', lambda e: btn.config(bg="#6c757d", fg="#fff"))
        btn.bind('<Leave>', lambda e: btn.config(bg="#adb5bd", fg="#212529"))

    def _get_avatar_image(self, avatar_path, size=120):
        try:
            if avatar_path and os.path.exists(avatar_path):
                img = Image.open(avatar_path)
                img = img.resize((size, size))
                return ImageTk.PhotoImage(img)
        except Exception:
            pass
        img = Image.new('RGB', (size, size), color='#e0e7ef')
        return ImageTk.PhotoImage(img)

    def _change_avatar(self):
        file_path = filedialog.askopenfilename(
            filetypes=[('Imagens', '*.png;*.jpg;*.jpeg;*.gif')]
        )
        if file_path:
            self.avatar_path = file_path
            # Re-renderiza toda a tela mantendo modo edição e novo avatar
            self.edit_mode = True
            self.render_profile()

    def _save_changes(self):
        user = UserController.get_logged_user()
        name = self.name_var.get().strip()
        course = self.course_var.get().strip()
        institution = user.institution  # Instituição não é mais editável
        avatar = self.avatar_path if self.avatar_path else user.avatar
        if not name or not course or not institution:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios.")
            return
        success = UserController.update_user(user.id, name, course, institution, avatar)
        if success:
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
            self.edit_mode = False
            self.render_profile()
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar os dados.")

    def _open_question(self, question_id):
        # Abre modal com detalhes da dúvida (cartão completo)
        import datetime
        import webbrowser
        from controllers.user_controller import UserController
        q = self.question_controller.get_all_questions_full()
        q = [item for item in q if item[0] == int(question_id)]
        if not q:
            messagebox.showerror("Erro", "Dúvida não encontrada.")
            return
        q = q[0]
        user = UserController.get_logged_user()
        # Modal
        modal = tk.Toplevel(self.parent)
        modal.title("Detalhes da Dúvida - UniAjuda")
        modal.configure(bg="#e9ecef")
        modal.grab_set()
        modal.resizable(False, False)
        modal.transient(self.parent.winfo_toplevel())
        # Centralizar
        modal.update_idletasks()
        w, h = 700, 480
        ws = modal.winfo_screenwidth()
        hs = modal.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        modal.geometry(f"{w}x{h}+{x}+{y}")
        # Card
        card = tk.Frame(modal, bg="#fff", bd=0, relief=tk.FLAT, highlightbackground="#e0e7ef", highlightthickness=2)
        card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=w-30, height=h-30)
        # Título
        tk.Label(card, text=q[1], font=("Arial", 20, "bold"), bg="#fff", fg="#023e8a").pack(pady=(18, 4), anchor="center")
        # Info
        user_name = q[6] if len(q) > 6 else "?"
        subject_str = f" | Disciplina: {q[3]}" if len(q) > 3 and q[3] else ""
        data_str = ""
        if len(q) > 7 and q[7]:
            try:
                data_str = f" | {datetime.datetime.strptime(q[7], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')}"
            except Exception:
                data_str = " | Hoje"
        else:
            data_str = " | Hoje"
        tk.Label(card, text=f"por {user_name}{subject_str}{data_str}", font=("Arial", 12, "italic"), bg="#fff", fg="#0077b6").pack(anchor="center")
        # Votos
        votos = q[4] if len(q) > 4 else 0
        tk.Label(card, text=f"🟢 {votos} votos", font=("Arial", 13, "bold"), bg="#fff", fg="#38b000").pack(anchor="center", pady=(0, 8))
        # Descrição
        tk.Label(card, text=q[2], font=("Arial", 15), bg="#fff", fg="#495057", anchor="w", wraplength=w-80, justify="left").pack(fill=tk.X, padx=36, pady=(0, 12))
        # Anexo
        anexo = q[7] if len(q) > 7 else None
        if anexo:
            def abrir_anexo():
                try:
                    if anexo.startswith('http'):
                        webbrowser.open(anexo)
                    else:
                        os.startfile(anexo)
                except Exception:
                    tk.messagebox.showerror("Erro", "Não foi possível abrir o anexo.")
            import os
            anexo_label = "Ver Anexo" if anexo.startswith('http') else os.path.basename(anexo)
            tk.Button(card, text=f"📎 {anexo_label}", font=("Arial", 13, "bold"), bg="#e0e7ef", fg="#0077b6", bd=0, relief=tk.FLAT, cursor="hand2", command=abrir_anexo, activebackground="#d0e7f7", activeforeground="#023e8a").pack(anchor="w", padx=36, pady=(0, 10))
        # Respostas
        respostas = self.answer_controller.get_answers_by_question_id(q[0])
        resp_label = tk.Label(card, text="Respostas:", font=("Arial", 14, "bold"), bg="#fff", fg="#0077b6")
        resp_label.pack(anchor="w", padx=36, pady=(8, 0))
        resp_frame = tk.Frame(card, bg="#fff")
        resp_frame.pack(fill=tk.BOTH, expand=False, padx=36, pady=(0, 8))
        if respostas:
            for r in respostas[:5]:
                resp_user = r[4] if len(r) > 4 else "?"
                tk.Label(resp_frame, text=f"- {r[2]} (por {resp_user})", font=("Arial", 12), bg="#f1f3f4", fg="#212529", anchor="w", wraplength=w-120, justify="left").pack(fill=tk.X, pady=(0, 2))
            if len(respostas) > 5:
                tk.Label(resp_frame, text=f"...e mais {len(respostas)-5} respostas.", font=("Arial", 11, "italic"), bg="#fff", fg="#adb5bd").pack(anchor="w")
        else:
            tk.Label(resp_frame, text="Ainda sem respostas.", font=("Arial", 12, "italic"), bg="#fff", fg="#adb5bd").pack(anchor="w")
        # Botão fechar
        tk.Button(card, text="Fechar", font=("Arial", 12, "bold"), bg="#adb5bd", fg="#212529", activebackground="#6c757d", activeforeground="#fff", bd=0, relief=tk.FLAT, width=14, cursor="hand2", command=modal.destroy).pack(pady=(10, 0))

    def logout(self):
        if tk.messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
            from controllers.user_controller import UserController
            if hasattr(UserController, 'set_logged_user'):
                UserController.set_logged_user(None)
            else:
                if hasattr(UserController, '_logged_user'):
                    UserController._logged_user = None
            # Usa o callback correto do main.py
            self.logout_callback()
