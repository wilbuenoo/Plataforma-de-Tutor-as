import tkinter as tk

class AdminView(tk.Frame):

    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Panel Administrador", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Label(self, text=f"Bienvenido {self.user.username}").pack()

        tk.Button(self, text="Gestionar Tutores").pack(pady=10)
        tk.Button(self, text="Gestionar Estudiantes").pack(pady=10)
        tk.Button(self, text="Ver Reportes").pack(pady=10)