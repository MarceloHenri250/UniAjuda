import tkinter as tk
from controllers.question_controller import QuestionController
from controllers.user_controller import UserController

class MyQuestionsScreen:
    def __init__(self, root, show_profile_callback):
        self.root = root
        self.show_profile = show_profile_callback
        self.question_controller = QuestionController()
        self.user = UserController.get_logged_user()
        self.search_var = tk.StringVar()
        self._build_ui()

    def _build_ui(self):
        self.root.configure(bg="#f8fafc")
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Minhas Perguntas", font=("Arial", 28, "bold"), bg="#f8fafc", fg="#0077b6").pack(pady=(32, 18))
        search_frame = tk.Frame(self.root, bg="#f8fafc")
        search_frame.pack(pady=(0, 10))
        tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 13), width=36).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(search_frame, text="Buscar", font=("Arial", 12, "bold"), bg="#0077b6", fg="#fff", bd=0, relief=tk.FLAT, cursor="hand2", command=self._render_questions).pack(side=tk.LEFT)
        self.questions_frame = tk.Frame(self.root, bg="#f8fafc")
        self.questions_frame.pack(fill=tk.BOTH, expand=True, padx=60, pady=(0, 18))
        self._render_questions()
        tk.Button(self.root, text="Voltar", font=("Arial", 12, "bold"), bg="#adb5bd", fg="#212529", activebackground="#6c757d", activeforeground="#fff", bd=0, relief=tk.FLAT, width=14, cursor="hand2", command=self.show_profile).pack(pady=(0, 18))

    def _render_questions(self):
        for widget in self.questions_frame.winfo_children():
            widget.destroy()
        questions = self.question_controller.get_user_questions(self.user.id)
        search = self.search_var.get().strip().lower()
        filtered = [q for q in questions if not search or search in q[1].lower() or search in (q[3] or '').lower()]
        if not filtered:
            tk.Label(self.questions_frame, text="Nenhuma dúvida encontrada.", font=("Arial", 13), bg="#f8fafc", fg="#adb5bd").pack(pady=30)
            return
        for q in filtered:
            self._render_question_card(q)

    def _render_question_card(self, q):
        import datetime
        import os
        card = tk.Frame(self.questions_frame, bg="#fff", bd=0, relief=tk.FLAT, highlightbackground="#e0e7ef", highlightthickness=1)
        card.pack(fill=tk.X, pady=10, padx=0)
        card.pack_propagate(True)
        tk.Label(card, text=q[1], font=("Arial", 16, "bold"), bg="#fff", fg="#023e8a", anchor="w").pack(anchor="w", padx=18, pady=(10, 0))
        subject_str = f"Disciplina: {q[3]}" if q[3] else ""
        data_str = ""
        if len(q) > 7 and q[7]:
            try:
                data_str = f" | {datetime.datetime.strptime(q[7], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')}"
            except Exception:
                data_str = ""
        tk.Label(card, text=f"{subject_str}{data_str}", font=("Arial", 12, "italic"), bg="#fff", fg="#0077b6").pack(anchor="w", padx=18)
        tk.Label(card, text=q[2], font=("Arial", 13), bg="#fff", fg="#495057", anchor="w", wraplength=900, justify="left").pack(fill=tk.X, padx=18, pady=(0, 8))
        card.bind('<Double-1>', lambda e, qid=q[0]: self._open_question(qid))
        for child in card.winfo_children():
            child.bind('<Double-1>', lambda e, qid=q[0]: self._open_question(qid))

    def _open_question(self, question_id):
        # Reutiliza o modal de detalhes já implementado no ProfileScreen
        from gui.profile_screen import ProfileScreen
        ProfileScreen._open_question(self, question_id)
