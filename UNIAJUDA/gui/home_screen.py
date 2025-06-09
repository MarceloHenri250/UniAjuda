import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from controllers.question_controller import QuestionController
from controllers.report_controller import ReportController
from controllers.answer_controller import AnswerController
from gui.question_screen import QuestionScreen

class HomeScreen:
    def __init__(self, root, show_home):
        self.root = root
        self.show_home = show_home
        self.q_controller = QuestionController()
        self.r_controller = ReportController()
        self.a_controller = AnswerController()

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
        # Renderiza a tela de dúvidas usando QuestionScreen
        QuestionScreen(self.duvidas_frame, show_post_callback=None, a_controller=self.a_controller, q_controller=self.q_controller, r_controller=self.r_controller)

        # Aba Perfil
        self.perfil_frame = tk.Frame(self.notebook, bg="#f8fafc")
        self.notebook.add(self.perfil_frame, text="Meu Perfil")
        from gui.profile_screen import ProfileScreen
        ProfileScreen(self.perfil_frame, logout_callback=self.logout)

    def logout(self):
        if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
            self.root.destroy()