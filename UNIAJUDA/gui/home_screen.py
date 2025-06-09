import tkinter as tk
from tkinter import ttk
from controllers.question_controller import QuestionController
from controllers.report_controller import ReportController
from controllers.answer_controller import AnswerController
from gui.question_screen import QuestionScreen

class HomeScreen:
    def __init__(self, root, show_home):
        self.root = root
        self.show_home = show_home

        # Controllers
        self.question_controller = QuestionController()
        self.report_controller = ReportController()
        self.answer_controller = AnswerController()

        # Janela principal
        self.root.title("UniAjuda - Plataforma de Apoio Acadêmico")
        self.root.state('zoomed')
        self.root.configure(bg="#e9ecef")

        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#ffffff", bd=0, relief=tk.FLAT)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Estilo do Notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            'TNotebook.Tab',
            font=('Arial', 13, 'bold'),
            padding=[20, 10],
            background='#e0e7ef',
            foreground='#0077b6'
        )
        style.map(
            'TNotebook.Tab',
            background=[('selected', '#0077b6')],
            foreground=[('selected', '#fff')]
        )
        style.configure('TNotebook', background='#f8fafc', borderwidth=0)

        # Notebook (abas)
        self.notebook = ttk.Notebook(self.main_frame, style='TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Aba Dúvidas
        self.questions_frame = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.questions_frame, text="Dúvidas")
        QuestionScreen(
            self.questions_frame,
            show_post_callback=None,
            answer_controller=self.answer_controller,
            question_controller=self.question_controller,
            report_controller=self.report_controller
        )

        # Aba Perfil
        self.profile_frame = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.profile_frame, text="Meu Perfil")
        from gui.profile_screen import ProfileScreen
        ProfileScreen(self.profile_frame, logout_callback=self.logout)

    def logout(self):
        self.root.destroy()