import tkinter as tk
from tkinter import messagebox
from models.user import User
from views.admin_view import AdminView
from views.tutor_view import TutorView
from views.student_view import StudentView

class LoginView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="PLATAFORMA DE TUTORÍAS", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Label(self, text="Usuario").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Rol").pack()

        self.role_var = tk.StringVar()
        self.role_var.set("estudiante")

        tk.Radiobutton(self, text="Administrador", variable=self.role_var, value="admin").pack()
        tk.Radiobutton(self, text="Tutor", variable=self.role_var, value="tutor").pack()
        tk.Radiobutton(self, text="Estudiante", variable=self.role_var, value="estudiante").pack()

        tk.Button(self, text="Ingresar", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        role = self.role_var.get()

        if not username:
            messagebox.showerror("Error", "Debe ingresar un usuario")
            return

        user = User(username, role)
        self.redirect(user)

    def redirect(self, user):
        self.destroy()

        if user.role == "admin":
            view = AdminView(self.master, user)
        elif user.role == "tutor":
            view = TutorView(self.master, user)
        else:
            view = StudentView(self.master, user)

        view.pack(fill="both", expand=True)