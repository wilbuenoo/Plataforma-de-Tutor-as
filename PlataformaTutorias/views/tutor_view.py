import tkinter as tk

class TutorView(tk.Frame):

    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Panel Tutor", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self, text=f"Bienvenido {self.user.username}").pack()

        tk.Button(self, text="Ver Tutorías Asignadas").pack(pady=10)
        tk.Button(self, text="Iniciar Sesión (Streamly)").pack(pady=10)