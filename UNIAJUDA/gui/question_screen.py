import tkinter as tk
from tkinter import ttk
from controllers.question_controller import QuestionController
from controllers.report_controller import ReportController
from controllers.answer_controller import AnswerController

class QuestionScreen:
    def __init__(
        self, parent, show_post_callback,
        answer_controller=None, question_controller=None, report_controller=None
    ):
        # --- Controllers and State ---
        self.parent = parent
        self.show_post = show_post_callback
        self.question_controller = question_controller or QuestionController()
        self.report_controller = report_controller or ReportController()
        self.answer_controller = answer_controller or AnswerController()
        self.expanded_questions = {}
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar()
        self.filter_var.set("")
        self.build_ui()

    # =========================
    # UI BUILDING
    # =========================
    def build_ui(self):
        # Fundo principal ocupa toda a tela
        self.frame = tk.Frame(self.parent, bg="#f4f8fb")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Container central ocupa toda a largura
        content_container = tk.Frame(self.frame, bg="#f4f8fb")
        content_container.pack(fill=tk.BOTH, expand=True)

        # Título centralizado
        tk.Label(
            content_container, text="Dúvidas Recentes",
            font=("Arial", 32, "bold"), bg="#f4f8fb", fg="#0077b6"
        ).pack(pady=(10, 24), anchor="center")

        # Topbar e área de dúvidas
        self._build_topbar(content_container)
        self._build_questions_area(content_container)

    # --- Topbar (Search & Filter) ---
    def _build_topbar(self, parent):
        # Topbar ocupa toda a largura
        topbar_card = tk.Frame(
            parent, bg="#fff", bd=0, relief=tk.FLAT,
            highlightbackground="#e0e7ef", highlightthickness=2
        )
        topbar_card.pack(fill=tk.X, padx=60, pady=(0, 24), ipadx=12, ipady=14)
        topbar = tk.Frame(topbar_card, bg="#fff")
        topbar.pack(fill=tk.X, padx=18, pady=6)

        search_frame = tk.Frame(topbar, bg="#fff")
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Campo de Busca
        search_icon = tk.Label(search_frame, text="🔍", font=("Arial", 13), bg="#fff", fg="#0077b6")
        search_icon.pack(side=tk.LEFT, padx=(0, 2))
        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, font=("Arial", 13), width=32,
            relief=tk.GROOVE, bd=2, highlightthickness=2, highlightcolor="#0077b6"
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=3)
        search_entry.insert(0, "Buscar por título ou descrição...")
        search_entry.bind('<FocusIn>', lambda e: self._on_entry_click(search_entry, "Buscar por título ou descrição..."))
        search_entry.bind('<FocusOut>', lambda e: self._on_focusout(search_entry, "Buscar por título ou descrição..."))
        search_entry.config(
            fg="#adb5bd", relief=tk.GROOVE, bd=2,
            highlightbackground="#e0e7ef", highlightcolor="#0077b6", borderwidth=2
        )

        # Campo de Filtro
        disc_icon = tk.Label(search_frame, text="📚", font=("Arial", 13), bg="#fff", fg="#0077b6")
        disc_icon.pack(side=tk.LEFT, padx=(8, 2))
        filter_entry = tk.Entry(
            search_frame, textvariable=self.filter_var, font=("Arial", 13), width=18,
            relief=tk.GROOVE, bd=2, highlightthickness=2, highlightcolor="#0077b6"
        )
        filter_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=3)
        filter_entry.insert(0, "Filtrar por disciplina...")
        filter_entry.bind('<FocusIn>', lambda e: self._on_entry_click(filter_entry, "Filtrar por disciplina..."))
        filter_entry.bind('<FocusOut>', lambda e: self._on_focusout(filter_entry, "Filtrar por disciplina..."))
        filter_entry.config(
            fg="#adb5bd", relief=tk.GROOVE, bd=2,
            highlightbackground="#e0e7ef", highlightcolor="#0077b6", borderwidth=2
        )

        filter_btn = tk.Button(
            search_frame, text="Filtrar", font=("Arial", 12, "bold"),
            bg="#0077b6", fg="#fff", bd=0, relief=tk.FLAT,
            activebackground="#023e8a", activeforeground="#fff",
            cursor="hand2", command=self.render_questions, height=1, width=10
        )
        filter_btn.pack(side=tk.LEFT, padx=(8, 0))
        filter_btn.bind('<Enter>', lambda e: filter_btn.config(bg="#023e8a"))
        filter_btn.bind('<Leave>', lambda e: filter_btn.config(bg="#0077b6"))

        # Botão Nova Dúvida à direita
        self.create_btn = tk.Button(
            topbar,
            text="➕ Nova Dúvida",
            font=("Arial", 16, "bold"),
            bg="#38b000",
            fg="#fff",
            activebackground="#007f00",
            activeforeground="#fff",
            bd=0,
            relief=tk.FLAT,
            width=18,
            height=2,
            cursor="hand2",
            command=self.abrir_nova_duvida
        )
        self.create_btn.pack(side=tk.RIGHT, padx=(32, 0))

    # --- Placeholder Handlers ---
    def _on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#212529")

    def _on_focusout(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#adb5bd")

    # --- Questions List Area ---
    def _build_questions_area(self, parent):
        center_frame = tk.Frame(parent, bg="#f4f8fb")
        center_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        self.questions_canvas = tk.Canvas(
            center_frame, bg="#f4f8fb", highlightthickness=0
        )
        self.questions_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Modern.Vertical.TScrollbar",
            gripcount=0,
            background="#b0bec5",
            darkcolor="#b0bec5",
            lightcolor="#b0bec5",
            troughcolor="#e0e7ef",
            bordercolor="#e0e7ef",
            arrowcolor="#0077b6",
            relief="flat",
            borderwidth=0,
            width=10
        )
        style.map("Modern.Vertical.TScrollbar",
            background=[('active', '#0077b6'), ('!active', '#b0bec5')],
            arrowcolor=[('active', '#023e8a'), ('!active', '#0077b6')]
        )
        self.questions_scrollbar = ttk.Scrollbar(
            center_frame, orient="vertical", command=self.questions_canvas.yview,
            style="Modern.Vertical.TScrollbar"
        )
        self.questions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.questions_canvas.configure(yscrollcommand=self.questions_scrollbar.set)
        self.questions_frame = tk.Frame(self.questions_canvas, bg="#f4f8fb")
        self.questions_canvas.create_window((0, 0), window=self.questions_frame, anchor="nw")

        def _on_mousewheel(event):
            bbox = self.questions_canvas.bbox("all")
            if bbox and bbox[3] > self.questions_canvas.winfo_height():
                self.questions_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.questions_canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.questions_canvas.bind_all("<Button-4>", lambda e: _on_mousewheel(e))
        self.questions_canvas.bind_all("<Button-5>", lambda e: _on_mousewheel(e))

        def update_scrollbar(*_):
            self.questions_canvas.update_idletasks()
            bbox = self.questions_canvas.bbox("all")
            if bbox and bbox[3] > self.questions_canvas.winfo_height():
                self.questions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                self.questions_scrollbar.pack_forget()
        self.questions_frame.bind("<Configure>", lambda e: (self._update_scrollregion(), update_scrollbar()))
        self.questions_canvas.bind("<Configure>", lambda e: update_scrollbar())

        # Impede rolagem além do conteúdo
        def _limit_scroll(*_):
            self.questions_canvas.update_idletasks()
            bbox = self.questions_canvas.bbox("all")
            if bbox:
                y1, y2 = self.questions_canvas.yview()
                if y1 <= 0:
                    self.questions_canvas.yview_moveto(0)
                elif y2 >= 1:
                    self.questions_canvas.yview_moveto(1 - (y2 - y1))
        self.questions_canvas.bind('<Configure>', _limit_scroll)
        self.questions_canvas.bind('<Enter>', lambda e: self.questions_canvas.bind_all('<MouseWheel>', _on_mousewheel))
        self.questions_canvas.bind('<Leave>', lambda e: self.questions_canvas.unbind_all('<MouseWheel>'))

        self.render_questions()

    def _update_scrollregion(self):
        self.questions_canvas.update_idletasks()
        bbox = self.questions_canvas.bbox("all")
        if bbox:
            # Impede rolagem para cima além do topo
            self.questions_canvas.configure(scrollregion=(0, 0, bbox[2], bbox[3]))
            # Remove o auto-scroll para o topo, mantém posição do usuário

    # =========================
    # QUESTIONS RENDERING
    # =========================
    def render_questions(self):
        from controllers.user_controller import UserController
        import datetime

        user = UserController.get_logged_user()
        for widget in self.questions_frame.winfo_children():
            widget.destroy()

        questions = self.question_controller.get_all_questions_full()
        search = self.search_var.get().strip().lower()
        if search == "buscar por título ou descrição...":
            search = ""
        discipline = self.filter_var.get().strip().lower()
        if discipline == "filtrar por disciplina...":
            discipline = ""

        filtered = [
            q for q in questions
            if (not search or search in q[1].lower() or search in q[2].lower())
            and (not discipline or (len(q) > 3 and discipline in (q[3] or '').lower()))
        ]

        if not filtered:
            tk.Label(
                self.questions_frame, text="Nenhuma dúvida encontrada.",
                font=("Arial", 13), bg="#f1f3f4", fg="#6c757d"
            ).pack(pady=30)
            return

        for q in filtered:
            self._render_question(q, user)

    # --- Render a Question Card ---
    def _render_question(self, q, user):
        import datetime
        import webbrowser
        qid = q[0]
        # Centraliza o cartão com padding lateral confortável
        card_outer = tk.Frame(self.questions_frame, bg="#f4f8fb", bd=0, highlightthickness=0)
        card_outer.pack(fill=tk.X, pady=12, padx=0)
        max_width = 900
        lateral_padding = 48  # padding lateral confortável
        q_frame = tk.Frame(
            card_outer, bg="#fff", bd=0,
            highlightbackground="#e0e7ef", highlightthickness=1, relief=tk.FLAT,
            width=max_width
        )
        q_frame.pack(padx=lateral_padding, anchor='center', pady=0, ipady=16, fill=None)
        q_frame.pack_propagate(True)  # Permite que o conteúdo ajuste a altura

        # Top row: title, user, subject, date, votes, like
        top_row = tk.Frame(q_frame, bg="#fff")
        top_row.pack(fill=tk.X, padx=18, pady=(10, 0))
        tk.Label(
            top_row, text=q[1], font=("Arial", 18, "bold"),
            bg="#fff", anchor="w", fg="#023e8a"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
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
        tk.Label(
            top_row, text=f"por {user_name}{subject_str}{data_str}",
            font=("Arial", 12, "italic"), bg="#fff", fg="#0077b6"
        ).pack(side=tk.LEFT, padx=(8, 0))
        votos = q[4] if len(q) > 4 else 0
        tk.Label(
            top_row, text=f"🟢 {votos}", font=("Arial", 13, "bold"),
            bg="#fff", fg="#38b000"
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Like/Unlike button
        if user and self.question_controller.user_liked_question(user.id, qid):
            btn_icon = "👎"
            btn_cmd = lambda qid=qid: self.toggle_like(qid, user.id, False)
            btn_fg = "#adb5bd"
        else:
            btn_icon = "👍"
            btn_cmd = lambda qid=qid: self.toggle_like(qid, user.id, True)
            btn_fg = "#38b000"
        like_btn = tk.Button(
            top_row, text=btn_icon, font=("Arial", 18, "bold"),
            bg="#fff", fg=btn_fg, bd=0, relief=tk.FLAT, width=2,
            cursor="hand2", command=btn_cmd,
            activebackground="#fff", activeforeground=btn_fg, highlightthickness=0
        )
        like_btn.pack(side=tk.LEFT, padx=(8, 0))

        # Description
        tk.Label(
            q_frame, text=q[2], font=("Arial", 16),
            bg="#fff", fg="#495057", anchor="w", wraplength=1500, justify="left"
        ).pack(fill=tk.X, padx=40, pady=(0, 16))

        # Attachment (button only, not in top bar)
        anexo = q[7] if len(q) > 7 else None
        if anexo:
            def abrir_anexo():
                try:
                    if anexo.startswith('http'):
                        webbrowser.open(anexo)
                    else:
                        import os
                        os.startfile(anexo)
                except Exception:
                    tk.messagebox.showerror("Erro", "Não foi possível abrir o anexo.")
            import os
            anexo_label = "Ver Anexo" if anexo.startswith('http') else os.path.basename(anexo)
            tk.Button(
                q_frame, text=f"📎 {anexo_label}", font=("Arial", 13, "bold"),
                bg="#e9ecef", fg="#0077b6", bd=0, relief=tk.FLAT, cursor="hand2",
                command=abrir_anexo, activebackground="#d0e7f7", activeforeground="#023e8a"
            ).pack(anchor="w", padx=40, pady=(0, 12))

        # Answers
        respostas = self.answer_controller.get_answers_by_question_id(qid)
        show_count = self.expanded_questions.get(qid, 3)
        if respostas:
            resp_label = tk.Label(
                q_frame, text="Respostas:", font=("Arial", 15, "bold"),
                bg="#fff", fg="#0077b6"
            )
            resp_label.pack(anchor="w", padx=40)
            for idx, r in enumerate(respostas):
                if idx >= show_count:
                    break
                resp_user = r[4] if len(r) > 4 else "?"
                tk.Label(
                    q_frame, text=f"- {r[2]} (por {resp_user})",
                    font=("Arial", 12), bg="#f1f3f4", fg="#212529",
                    anchor="w", wraplength=650, justify="left"
                ).pack(fill=tk.X, padx=38, pady=(0, 4))
            # Botão para ver mais/ver menos
            btn_frame = tk.Frame(q_frame, bg="#fff")
            btn_frame.pack(anchor="w", padx=38, pady=(0, 10))
            if show_count < len(respostas):
                def ver_mais(qid=qid):
                    self.expanded_questions[qid] = min(show_count + 3, len(respostas))
                    self.render_questions()
                tk.Button(
                    btn_frame, text=f"Ver mais respostas ({min(3, len(respostas)-show_count)})",
                    font=("Arial", 11, "bold"), bg="#0077b6", fg="#fff",
                    bd=0, relief=tk.FLAT, cursor="hand2", command=ver_mais
                ).pack(side=tk.LEFT)
            if show_count > 3:
                def ver_menos(qid=qid):
                    self.expanded_questions[qid] = 3
                    self.render_questions()
                tk.Button(
                    btn_frame, text="Mostrar menos",
                    font=("Arial", 11, "bold"), bg="#adb5bd", fg="#212529",
                    bd=0, relief=tk.FLAT, cursor="hand2", command=ver_menos
                ).pack(side=tk.LEFT, padx=(8, 0))
        else:
            tk.Label(
                q_frame, text="Ainda sem respostas.",
                font=("Arial", 13, "italic"), bg="#fff", fg="#adb5bd"
            ).pack(anchor="w", padx=40)

        # Action buttons
        btns_frame = tk.Frame(q_frame, bg="#fff")
        btns_frame.pack(fill=tk.X, padx=32, pady=(0, 16))
        resp_btn = tk.Button(
            btns_frame, text="💬 Responder", font=("Arial", 12, "bold"),
            bg="#0077b6", fg="#fff", activebackground="#023e8a",
            activeforeground="#fff", bd=0, relief=tk.FLAT, width=13,
            cursor="hand2", command=lambda qid=qid: self.responder(qid)
        )
        resp_btn.pack(side=tk.LEFT, padx=(0, 8))
        resp_btn.bind('<Enter>', lambda e, b=resp_btn: b.config(bg="#023e8a"))
        resp_btn.bind('<Leave>', lambda e, b=resp_btn: b.config(bg="#0077b6"))
        den_btn = tk.Button(
            btns_frame, text="🚩 Denunciar", font=("Arial", 12, "bold"),
            bg="#d90429", fg="#fff", activebackground="#a30015",
            activeforeground="#fff", bd=0, relief=tk.FLAT, width=13,
            cursor="hand2", command=lambda qid=qid: self.denunciar(qid)
        )
        den_btn.pack(side=tk.LEFT)
        den_btn.bind('<Enter>', lambda e, b=den_btn: b.config(bg="#a30015"))
        den_btn.bind('<Leave>', lambda e, b=den_btn: b.config(bg="#d90429"))

    # =========================
    # ACTIONS
    # =========================
    def responder(self, question_id):
        from gui.answer_question_screen import AnswerQuestionScreen
        root = self.parent.winfo_toplevel()
        AnswerQuestionScreen(root, self.show_home, question_id)

    def denunciar(self, question_id):
        from gui.report_screen import ReportScreen
        root = self.parent.winfo_toplevel()
        ReportScreen(root, self.show_home, question_id)

    def votar(self, question_id):
        self.question_controller.add_vote(question_id)
        self.render_questions()

    def toggle_like(self, question_id, user_id, like):
        if like:
            self.question_controller.like_question(user_id, question_id)
        else:
            self.question_controller.unlike_question(user_id, question_id)
        self.render_questions()

    def abrir_nova_duvida(self):
        from gui.post_question_screen import PostQuestionScreen
        root = self.parent.winfo_toplevel()
        PostQuestionScreen(root, self.show_home)

    # =========================
    # NAVIGATION CALLBACKS
    # =========================
    def show_home(self):
        self.render_questions()
