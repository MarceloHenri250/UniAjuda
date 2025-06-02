import tkinter as tk
from tkinter import ttk
from controllers.question_controller import QuestionController
from controllers.report_controller import ReportController
from controllers.answer_controller import AnswerController

class QuestionScreen:
    def __init__(self, parent, show_post_callback, a_controller=None, q_controller=None, r_controller=None):
        # --- Controladores e Estado ---
        self.parent = parent
        self.show_post = show_post_callback
        self.q_controller = q_controller or QuestionController()
        self.r_controller = r_controller or ReportController()
        self.a_controller = a_controller or AnswerController()
        self.expanded_questions = {}
        self.search_var = tk.StringVar()
        self.filter_var = tk.StringVar()
        self.filter_var.set("")
        self.build_ui()

    # =========================
    # CONSTRUÇÃO DA INTERFACE
    # =========================
    def build_ui(self):
        self.frame = tk.Frame(self.parent, bg="#f8fafc")
        self.frame.pack(fill=tk.BOTH, expand=True)
        tk.Frame(self.frame, height=30, bg="#f8fafc").pack(fill=tk.X)

        content_container = tk.Frame(self.frame, bg="#f8fafc")
        content_container.pack(expand=True)

        tk.Label(
            content_container, text="Dúvidas Recentes",
            font=("Arial", 26, "bold"), bg="#f8fafc", fg="#0077b6"
        ).pack(pady=(0, 18), anchor="center")

        self._build_topbar(content_container)
        self._build_questions_area(content_container)

        tk.Frame(self.frame, height=30, bg="#f8fafc").pack(fill=tk.X, side=tk.BOTTOM)

    # --- Topbar (Busca & Filtro) ---
    def _build_topbar(self, parent):
        topbar_card = tk.Frame(
            parent, bg="#fff", bd=2, relief=tk.RIDGE,
            highlightbackground="#e0e7ef", highlightthickness=2
        )
        topbar_card.pack(pady=(0, 30), ipadx=12, ipady=10)
        topbar = tk.Frame(topbar_card, bg="#fff")
        topbar.pack(padx=18, pady=6)

        search_frame = tk.Frame(topbar, bg="#fff")
        search_frame.pack(side=tk.LEFT)

        # Campo de Busca
        search_icon = tk.Label(search_frame, text="🔍", font=("Arial", 13), bg="#fff", fg="#0077b6")
        search_icon.pack(side=tk.LEFT, padx=(0, 2))

        search_entry = tk.Entry(
            search_frame, textvariable=self.search_var, font=("Arial", 12), width=28,
            relief=tk.GROOVE, bd=2, highlightthickness=2, highlightcolor="#0077b6"
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 8))
        search_entry.insert(0, "Buscar por título ou descrição...")

        search_entry.bind('<FocusIn>', lambda e: self._on_entry_click(search_entry, "Buscar por título ou descrição..."))
        search_entry.bind('<FocusOut>', lambda e: self._on_focusout(search_entry, "Buscar por título ou descrição..."))
        search_entry.config(
            fg="#adb5bd", relief=tk.GROOVE, bd=2,
            highlightbackground="#e0e7ef", highlightcolor="#0077b6", borderwidth=2
        )

        # Campo de Filtro
        disc_icon = tk.Label(search_frame, text="📚", font=("Arial", 13), bg="#fff", fg="#0077b6")
        disc_icon.pack(side=tk.LEFT, padx=(6, 2))

        filter_entry = tk.Entry(
            search_frame, textvariable=self.filter_var, font=("Arial", 12), width=16,
            relief=tk.GROOVE, bd=2, highlightthickness=2, highlightcolor="#0077b6"
        )
        filter_entry.pack(side=tk.LEFT, padx=(0, 8))
        filter_entry.insert(0, "Filtrar por disciplina...")

        filter_entry.bind('<FocusIn>', lambda e: self._on_entry_click(filter_entry, "Filtrar por disciplina..."))
        filter_entry.bind('<FocusOut>', lambda e: self._on_focusout(filter_entry, "Filtrar por disciplina..."))
        filter_entry.config(
            fg="#adb5bd", relief=tk.GROOVE, bd=2,
            highlightbackground="#e0e7ef", highlightcolor="#0077b6", borderwidth=2
        )

        filter_btn = tk.Button(
            search_frame, text="Filtrar", font=("Arial", 11, "bold"),
            bg="#0077b6", fg="#fff", bd=0, relief=tk.FLAT,
            activebackground="#023e8a", activeforeground="#fff",
            cursor="hand2", command=self.render_questions
        )
        filter_btn.pack(side=tk.LEFT, padx=(8, 0))
        filter_btn.bind('<Enter>', lambda e: filter_btn.config(bg="#023e8a"))
        filter_btn.bind('<Leave>', lambda e: filter_btn.config(bg="#0077b6"))

        # Botão Nova Dúvida
        self.create_btn = tk.Button(
            topbar,
            text="+ Nova Dúvida",
            font=("Arial", 15, "bold"),
            bg="#38b000",
            fg="#fff",
            activebackground="#007f00",
            activeforeground="#fff",
            bd=0,
            relief=tk.FLAT,
            width=16,
            height=2,
            cursor="hand2",
            command=self.abrir_nova_duvida
        )
        self.create_btn.pack(side=tk.LEFT, padx=(32, 0))

    # --- Manipuladores de Placeholder ---
    def _on_entry_click(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="#212529")

    def _on_focusout(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#adb5bd")

    # --- Área da Lista de Dúvidas ---
    def _build_questions_area(self, parent):
        center_frame = tk.Frame(parent, bg="#f8fafc")
        center_frame.pack(fill=tk.BOTH, expand=True)

        self.questions_canvas = tk.Canvas(
            center_frame, bg="#f8fafc", highlightthickness=0, width=900, height=520
        )
        self.questions_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.questions_scrollbar = tk.Scrollbar(
            center_frame, orient="vertical", command=self.questions_canvas.yview
        )
        self.questions_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.questions_canvas.configure(yscrollcommand=self.questions_scrollbar.set)

        self.questions_frame = tk.Frame(self.questions_canvas, bg="#f8fafc")
        self.questions_canvas.create_window((0, 0), window=self.questions_frame, anchor="nw")
        self.questions_frame.bind(
            "<Configure>",
            lambda e: self.questions_canvas.configure(scrollregion=self.questions_canvas.bbox("all"))
        )
        self.questions_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self.questions_canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        self.render_questions()

    # =========================
    # RENDERIZAÇÃO DAS DÚVIDAS
    # =========================
    def render_questions(self):
        from controllers.user_controller import UserController
        import datetime

        user = UserController.get_logged_user()
        for widget in self.questions_frame.winfo_children():
            widget.destroy()

        questions = self.q_controller.get_all_questions_full()
        search = self.search_var.get().strip().lower()
        if search == "buscar por título ou descrição...":
            search = ""
        disciplina = self.filter_var.get().strip().lower()
        if disciplina == "filtrar por disciplina...":
            disciplina = ""

        filtered = [
            q for q in questions
            if (not search or search in q[1].lower() or search in q[2].lower())
            and (not disciplina or (len(q) > 3 and disciplina in (q[3] or '').lower()))
        ]

        if not filtered:
            tk.Label(
                self.questions_frame, text="Nenhuma dúvida encontrada.",
                font=("Arial", 13), bg="#f1f3f4", fg="#6c757d"
            ).pack(pady=30)
            return

        for q in filtered:
            self._render_question(q, user)

    # --- Renderiza um Cartão de Dúvida ---
    def _render_question(self, q, user):
        import datetime

        qid = q[0]
        q_frame = tk.Frame(
            self.questions_frame, bg="#fff", bd=0,
            highlightbackground="#adb5bd", highlightthickness=2, relief=tk.RIDGE
        )
        q_frame.pack(fill=tk.X, pady=16, padx=10, ipady=6)
        shadow = tk.Frame(self.questions_frame, bg="#e0e0e0", height=4)
        shadow.pack(fill=tk.X, padx=18, pady=(0, 0))

        votos = q[4] if len(q) > 4 else 0
        user_name = q[6] if len(q) > 6 else "?"
        disciplina_str = f" | Disciplina: {q[3]}" if len(q) > 3 and q[3] else ""
        data_str = ""
        if len(q) > 7 and q[7]:
            try:
                data_str = f" | {datetime.datetime.strptime(q[7], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')}"
            except Exception:
                data_str = f" | {q[7]}"
        else:
            data_str = " | Hoje"

        # --- Linha Superior: Título, Usuário, Votos, Botão Curtir ---
        top_row = tk.Frame(q_frame, bg="#fff")
        top_row.pack(fill=tk.X, padx=18, pady=(10, 0))
        tk.Label(
            top_row, text=q[1], font=("Arial", 17, "bold"),
            bg="#fff", anchor="w"
        ).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(
            top_row, text=f"por {user_name}{disciplina_str}{data_str}",
            font=("Arial", 12, "italic"), bg="#fff", fg="#0077b6"
        ).pack(side=tk.LEFT, padx=(8, 0))
        tk.Label(
            top_row, text=f"🟢 {votos}", font=("Arial", 13, "bold"),
            bg="#fff", fg="#38b000"
        ).pack(side=tk.LEFT, padx=(8, 0))

        # Botão Curtir/Descurtir
        if user and self.q_controller.user_liked_question(user.id, qid):
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

        # --- Descrição ---
        tk.Label(
            q_frame, text=q[2], font=("Arial", 13),
            bg="#fff", fg="#495057", anchor="w", wraplength=700, justify="left"
        ).pack(fill=tk.X, padx=18, pady=(0, 10))

        # --- Seção de Respostas ---
        respostas = self.a_controller.get_answers_by_question_id(qid)
        show_all = self.expanded_questions.get(qid, False)
        max_to_show = 2 if respostas and len(respostas) > 2 and not show_all else len(respostas) if respostas else 0

        if respostas:
            resp_label = tk.Label(
                q_frame, text="Respostas:", font=("Arial", 13, "bold"),
                bg="#fff", fg="#0077b6"
            )
            resp_label.pack(anchor="w", padx=28)
            for idx, r in enumerate(respostas):
                if idx >= max_to_show:
                    break
                resp_user = r[4] if len(r) > 4 else "?"
                tk.Label(
                    q_frame, text=f"- {r[2]} (por {resp_user})",
                    font=("Arial", 12), bg="#f1f3f4", fg="#212529",
                    anchor="w", wraplength=650, justify="left"
                ).pack(fill=tk.X, padx=38, pady=(0, 4))
            if len(respostas) > 2 and not show_all:
                def expand_resps(qid=qid):
                    self.expanded_questions[qid] = True
                    self.render_questions()
                tk.Button(
                    q_frame, text=f"Ver mais respostas ({len(respostas)-2})",
                    font=("Arial", 11, "bold"), bg="#0077b6", fg="#fff",
                    bd=0, relief=tk.FLAT, cursor="hand2", command=expand_resps
                ).pack(anchor="w", padx=38, pady=(0, 8))
        else:
            tk.Label(
                q_frame, text="Ainda sem respostas.",
                font=("Arial", 11, "italic"), bg="#fff", fg="#adb5bd"
            ).pack(anchor="w", padx=28)

        # --- Botões de Ação (Responder, Denunciar) ---
        btns_frame = tk.Frame(q_frame, bg="#fff")
        btns_frame.pack(fill=tk.X, padx=18, pady=(0, 10))

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
    # AÇÕES
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
        self.q_controller.add_vote(question_id)
        self.render_questions()

    def toggle_like(self, question_id, user_id, like):
        if like:
            self.q_controller.like_question(user_id, question_id)
        else:
            self.q_controller.unlike_question(user_id, question_id)
        self.render_questions()

    def abrir_nova_duvida(self):
        from gui.post_question_screen import PostQuestionScreen
        root = self.parent.winfo_toplevel()
        PostQuestionScreen(root, self.show_home)

    # =========================
    # CALLBACKS DE NAVEGAÇÃO
    # =========================
    def show_home(self):
        # Callback para retornar à lista de dúvidas
        self.render_questions()
