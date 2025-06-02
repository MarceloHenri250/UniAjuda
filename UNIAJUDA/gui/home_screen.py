import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.question_controller import QuestionController
from controllers.report_controller import ReportController
from controllers.answer_controller import AnswerController

class HomeScreen:
    def __init__(self, root, show_home):
        self.root = root
        self.show_home = show_home
        self.q_controller = QuestionController()
        self.r_controller = ReportController()
        self.a_controller = AnswerController()
        self.expanded_questions = {}  # id da pergunta: True/False

        # Configurações da janela principal
        self.root.title("UniAjuda - Plataforma de Apoio Acadêmico")
        self.root.state('zoomed')
        self.root.configure(bg="#e9ecef")

        # Frame principal ocupa toda a janela
        self.main_frame = tk.Frame(self.root, bg="#ffffff", bd=0, relief=tk.FLAT)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Notebook (abas)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook.Tab', font=('Arial', 13, 'bold'), padding=[20, 10], background='#e0e7ef', foreground='#0077b6')
        style.map('TNotebook.Tab', background=[('selected', '#0077b6')], foreground=[('selected', '#fff')])
        style.configure('TNotebook', background='#f8fafc', borderwidth=0)

        self.notebook = ttk.Notebook(self.main_frame, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Aba Dúvidas
        self.duvidas_frame = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.duvidas_frame, text="Dúvidas")

        # Aba Perfil
        self.perfil_frame = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.perfil_frame, text="Meu Perfil")

        # Conteúdo da aba Dúvidas
        # Centraliza o título
        tk.Label(self.duvidas_frame, text="Dúvidas Recentes", font=("Arial", 26, "bold"), bg="#f8fafc", fg="#0077b6").pack(pady=(40, 18), anchor="center")

        # Centraliza a barra de pesquisa
        search_frame = tk.Frame(self.duvidas_frame, bg="#f8fafc")
        search_frame.pack(fill=None, expand=False, pady=(0, 18))
        search_frame.place(relx=0.5, anchor="n", y=90)
        self.search_var = tk.StringVar()
        # Ícone de busca
        search_icon = tk.Label(search_frame, text="🔍", font=("Arial", 13), bg="#f8fafc", fg="#0077b6")
        search_icon.pack(side=tk.LEFT, padx=(0, 2))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 12), width=32, relief=tk.GROOVE, bd=2, highlightthickness=2, highlightcolor="#0077b6")
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.insert(0, "Buscar por título ou descrição...")
        def on_entry_click(event):
            if search_entry.get() == "Buscar por título ou descrição...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="#212529")
        def on_focusout(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Buscar por título ou descrição...")
                search_entry.config(fg="#adb5bd")
        search_entry.bind('<FocusIn>', on_entry_click)
        search_entry.bind('<FocusOut>', on_focusout)
        search_entry.config(fg="#adb5bd", relief=tk.GROOVE, bd=2, highlightbackground="#e0e7ef", highlightcolor="#0077b6", borderwidth=2)
        self.filter_var = tk.StringVar()
        self.filter_var.set("")
        # Ícone disciplina
        disc_icon = tk.Label(search_frame, text="📚", font=("Arial", 13), bg="#f8fafc", fg="#0077b6")
        disc_icon.pack(side=tk.LEFT, padx=(10, 2))
        self.filter_entry = tk.Entry(search_frame, textvariable=self.filter_var, font=("Arial", 12), width=18, relief=tk.GROOVE, bd=2, highlightthickness=2, highlightcolor="#0077b6")
        self.filter_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.filter_entry.insert(0, "Filtrar por disciplina...")
        def on_disc_entry_click(event):
            if self.filter_entry.get() == "Filtrar por disciplina...":
                self.filter_entry.delete(0, tk.END)
                self.filter_entry.config(fg="#212529")
        def on_disc_focusout(event):
            if self.filter_entry.get() == "":
                self.filter_entry.insert(0, "Filtrar por disciplina...")
                self.filter_entry.config(fg="#adb5bd")
        self.filter_entry.bind('<FocusIn>', on_disc_entry_click)
        self.filter_entry.bind('<FocusOut>', on_disc_focusout)
        self.filter_entry.config(fg="#adb5bd", relief=tk.GROOVE, bd=2, highlightbackground="#e0e7ef", highlightcolor="#0077b6", borderwidth=2)
        # Botão filtrar
        filter_btn = tk.Button(search_frame, text="Filtrar", font=("Arial", 11, "bold"), bg="#0077b6", fg="#fff", bd=0, relief=tk.FLAT, activebackground="#023e8a", activeforeground="#fff", cursor="hand2", command=self.render_questions)
        filter_btn.pack(side=tk.LEFT, padx=(10, 0))
        filter_btn.bind('<Enter>', lambda e: filter_btn.config(bg="#023e8a"))
        filter_btn.bind('<Leave>', lambda e: filter_btn.config(bg="#0077b6"))

        # Frame horizontal para lista de dúvidas + botão nova dúvida
        content_frame = tk.Frame(self.duvidas_frame, bg="#f8fafc")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 30))
        # Canvas de dúvidas (centralizado)
        self.questions_canvas = tk.Canvas(content_frame, bg="#f8fafc", highlightthickness=0, width=700)
        self.questions_scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=self.questions_canvas.yview)
        self.questions_canvas.configure(yscrollcommand=self.questions_scrollbar.set)
        self.questions_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(80,0))
        self.questions_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.questions_frame = tk.Frame(self.questions_canvas, bg="#f8fafc")
        self.questions_canvas.create_window((0, 0), window=self.questions_frame, anchor="nw")
        self.questions_frame.bind("<Configure>", lambda e: self.questions_canvas.configure(scrollregion=self.questions_canvas.bbox("all")))
        self.questions_canvas.bind_all("<MouseWheel>", lambda e: self.questions_canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        # Botão nova dúvida (fixo topo direito)
        btn_frame = tk.Frame(content_frame, bg="#f8fafc")
        btn_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(40, 0), anchor="n")
        self.create_btn = tk.Button(
            btn_frame,
            text="+ Nova Dúvida",
            font=("Arial", 15, "bold"),
            bg="#38b000",
            fg="#fff",
            activebackground="#007f00",
            activeforeground="#fff",
            bd=0,
            relief=tk.FLAT,
            width=18,
            height=2,
            cursor="hand2",
            command=self.show_post
        )
        self.create_btn.pack(pady=(10, 0), anchor="n")
        self.render_questions()

        # Conteúdo da aba Perfil
        self.render_profile()

    def show_post(self):
        from gui.post_question_screen import PostQuestionScreen
        PostQuestionScreen(self.root, self.show_home)

    def render_profile(self):
        from controllers.user_controller import UserController
        user = UserController.get_logged_user()
        for widget in self.perfil_frame.winfo_children():
            widget.destroy()
        tk.Label(self.perfil_frame, text="Meu Perfil", font=("Arial", 24, "bold"), bg="#f8fafc", fg="#0077b6").pack(pady=(25, 12))
        if user:
            tk.Label(self.perfil_frame, text=f"Nome: {user.nome}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
            tk.Label(self.perfil_frame, text=f"Matrícula: {user.matricula}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
            tk.Label(self.perfil_frame, text=f"Curso: {user.curso}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
            tk.Label(self.perfil_frame, text=f"E-mail: {user.email}", font=("Arial", 13), bg="#f8fafc").pack(anchor="w", padx=30)
        else:
            tk.Label(self.perfil_frame, text="Usuário não identificado.", font=("Arial", 13), bg="#f8fafc", fg="#d90429").pack(anchor="w", padx=30)
            return
        # Minhas Perguntas
        tk.Label(self.perfil_frame, text="Minhas Perguntas:", font=("Arial", 13, "bold"), bg="#f8fafc", fg="#0077b6").pack(anchor="w", padx=30, pady=(20, 0))
        questions = self.q_controller.get_user_questions(user.id)
        if questions:
            for q in questions:
                tk.Label(self.perfil_frame, text=f"- {q[1]} (Disciplina: {q[3]})", font=("Arial", 12), bg="#f1f3f4", fg="#212529", anchor="w", wraplength=600, justify="left").pack(fill=tk.X, padx=40, pady=(0, 2))
        else:
            tk.Label(self.perfil_frame, text="Nenhuma pergunta cadastrada.", font=("Arial", 11, "italic"), bg="#f8fafc", fg="#adb5bd").pack(anchor="w", padx=40)
        # Minhas Respostas
        tk.Label(self.perfil_frame, text="Minhas Respostas:", font=("Arial", 13, "bold"), bg="#f8fafc", fg="#0077b6").pack(anchor="w", padx=30, pady=(20, 0))
        answers = self.a_controller.get_user_answers(user.id)
        if answers:
            for a in answers:
                tk.Label(self.perfil_frame, text=f"- {a[2]} (Pergunta ID: {a[1]})", font=("Arial", 12), bg="#f1f3f4", fg="#212529", anchor="w", wraplength=600, justify="left").pack(fill=tk.X, padx=40, pady=(0, 2))
        else:
            tk.Label(self.perfil_frame, text="Nenhuma resposta cadastrada.", font=("Arial", 11, "italic"), bg="#f8fafc", fg="#adb5bd").pack(anchor="w", padx=40)
        # Botão de sair
        tk.Button(self.perfil_frame, text="Sair", font=("Arial", 12, "bold"), bg="#adb5bd", fg="#212529", activebackground="#6c757d", activeforeground="#fff", bd=0, relief=tk.FLAT, width=12, height=1, cursor="hand2", command=self.logout).pack(pady=(30, 0))

    def render_questions(self):
        from controllers.user_controller import UserController
        import datetime
        user = UserController.get_logged_user()
        # Limpa o frame
        for widget in self.questions_frame.winfo_children():
            widget.destroy()
        # Busca e filtra dúvidas
        questions = self.q_controller.get_all_questions_full()
        search = self.search_var.get().strip().lower()
        if search == "buscar por título ou descrição...":
            search = ""
        disciplina = self.filter_var.get().strip().lower()
        if disciplina == "filtrar por disciplina...":
            disciplina = ""
        filtered = []
        for q in questions:
            if (not search or search in q[1].lower() or search in q[2].lower()) and (not disciplina or (len(q) > 3 and disciplina in (q[3] or '').lower())):
                filtered.append(q)
        if not filtered:
            tk.Label(self.questions_frame, text="Nenhuma dúvida encontrada.", font=("Arial", 13), bg="#f1f3f4", fg="#6c757d").pack(pady=30)
            return
        for q in filtered:
            qid = q[0]
            q_frame = tk.Frame(self.questions_frame, bg="#fff", bd=0, highlightbackground="#adb5bd", highlightthickness=2)
            q_frame.pack(fill=tk.X, pady=16, padx=10, ipady=6)
            q_frame.configure(relief=tk.RIDGE)
            # Sombra fake
            shadow = tk.Frame(self.questions_frame, bg="#e0e0e0", height=4)
            shadow.pack(fill=tk.X, padx=18, pady=(0, 0))
            votos = q[4] if len(q) > 4 else 0
            user_name = q[6] if len(q) > 6 else "?"
            # Suporte a data e disciplina
            disciplina_str = f" | Disciplina: {q[3]}" if len(q) > 3 and q[3] else ""
            # Suporte a data (se existir na query, senão exibe 'Hoje')
            data_str = ""
            if len(q) > 7 and q[7]:
                try:
                    data_str = f" | {datetime.datetime.strptime(q[7], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')}"
                except Exception:
                    data_str = f" | {q[7]}"
            else:
                data_str = " | Hoje"
            top_row = tk.Frame(q_frame, bg="#fff")
            top_row.pack(fill=tk.X, padx=18, pady=(10, 0))
            tk.Label(top_row, text=q[1], font=("Arial", 17, "bold"), bg="#fff", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
            tk.Label(top_row, text=f"por {user_name}{disciplina_str}{data_str}", font=("Arial", 12, "italic"), bg="#fff", fg="#0077b6").pack(side=tk.LEFT, padx=(8, 0))
            tk.Label(top_row, text=f"🟢 {votos}", font=("Arial", 13, "bold"), bg="#fff", fg="#38b000").pack(side=tk.LEFT, padx=(8, 0))
            # Botão Curtir/Descurtir com ícone estilizado
            if user and self.q_controller.user_liked_question(user.id, qid):
                btn_icon = "👎"
                btn_cmd = lambda qid=qid: self.toggle_like(qid, user.id, False)
                btn_fg = "#adb5bd"
            else:
                btn_icon = "👍"
                btn_cmd = lambda qid=qid: self.toggle_like(qid, user.id, True)
                btn_fg = "#38b000"
            like_btn = tk.Button(top_row, text=btn_icon, font=("Arial", 18, "bold"), bg="#fff", fg=btn_fg, bd=0, relief=tk.FLAT, width=2, cursor="hand2", command=btn_cmd, activebackground="#fff", activeforeground=btn_fg, highlightthickness=0)
            like_btn.pack(side=tk.LEFT, padx=(8, 0))
            # Descrição
            tk.Label(q_frame, text=q[2], font=("Arial", 13), bg="#fff", fg="#495057", anchor="w", wraplength=700, justify="left").pack(fill=tk.X, padx=18, pady=(0, 10))
            # Exibe as respostas da dúvida (máximo 2, com opção de ver mais)
            respostas = self.a_controller.get_answers_by_question_id(qid)
            show_all = self.expanded_questions.get(qid, False)
            max_to_show = 2 if respostas and len(respostas) > 2 and not show_all else len(respostas) if respostas else 0
            if respostas:
                resp_label = tk.Label(q_frame, text="Respostas:", font=("Arial", 13, "bold"), bg="#fff", fg="#0077b6")
                resp_label.pack(anchor="w", padx=28)
                for idx, r in enumerate(respostas):
                    if idx >= max_to_show:
                        break
                    resp_user = r[4] if len(r) > 4 else "?"
                    tk.Label(q_frame, text=f"- {r[2]} (por {resp_user})", font=("Arial", 12), bg="#f1f3f4", fg="#212529", anchor="w", wraplength=650, justify="left").pack(fill=tk.X, padx=38, pady=(0, 4))
                if len(respostas) > 2 and not show_all:
                    def expand_resps(qid=qid):
                        self.expanded_questions[qid] = True
                        self.render_questions()
                    tk.Button(q_frame, text=f"Ver mais respostas ({len(respostas)-2})", font=("Arial", 11, "bold"), bg="#0077b6", fg="#fff", bd=0, relief=tk.FLAT, cursor="hand2", command=expand_resps).pack(anchor="w", padx=38, pady=(0, 8))
            else:
                tk.Label(q_frame, text="Ainda sem respostas.", font=("Arial", 11, "italic"), bg="#fff", fg="#adb5bd").pack(anchor="w", padx=28)
            btns_frame = tk.Frame(q_frame, bg="#fff")
            btns_frame.pack(fill=tk.X, padx=18, pady=(0, 10))
            # Botão Responder com ícone
            resp_btn = tk.Button(
                btns_frame, text="💬 Responder", font=("Arial", 12, "bold"), bg="#0077b6", fg="#fff",
                activebackground="#023e8a", activeforeground="#fff", bd=0, relief=tk.FLAT, width=13, cursor="hand2",
                command=lambda qid=qid: self.responder(qid)
            )
            resp_btn.pack(side=tk.LEFT, padx=(0, 8))
            resp_btn.bind('<Enter>', lambda e, b=resp_btn: b.config(bg="#023e8a"))
            resp_btn.bind('<Leave>', lambda e, b=resp_btn: b.config(bg="#0077b6"))
            # Botão Denunciar com ícone
            den_btn = tk.Button(
                btns_frame, text="🚩 Denunciar", font=("Arial", 12, "bold"), bg="#d90429", fg="#fff",
                activebackground="#a30015", activeforeground="#fff", bd=0, relief=tk.FLAT, width=13, cursor="hand2",
                command=lambda qid=qid: self.denunciar(qid)
            )
            den_btn.pack(side=tk.LEFT)
            den_btn.bind('<Enter>', lambda e, b=den_btn: b.config(bg="#a30015"))
            den_btn.bind('<Leave>', lambda e, b=den_btn: b.config(bg="#d90429"))

    def responder(self, question_id):
        from gui.answer_question_screen import AnswerQuestionScreen
        AnswerQuestionScreen(self.root, self.show_home, question_id)

    def denunciar(self, question_id):
        from gui.report_screen import ReportScreen
        ReportScreen(self.root, self.show_home, question_id)

    def votar(self, question_id):
        self.q_controller.add_vote(question_id)
        self.render_questions()

    def toggle_like(self, question_id, user_id, like):
        if like:
            self.q_controller.like_question(user_id, question_id)
        else:
            self.q_controller.unlike_question(user_id, question_id)
        self.render_questions()

    def logout(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
            self.root.destroy()