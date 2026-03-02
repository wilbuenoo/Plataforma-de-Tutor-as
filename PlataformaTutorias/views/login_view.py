import tkinter as tk
from tkinter import messagebox
from models.user import User

# 🎨 PALETA APPLE DARK
BG_COLOR = "#0E0E10"
CARD_COLOR = "#1A1A1D"
INPUT_COLOR = "#2A2A2E"
ACCENT_COLOR = "#0A84FF"
ACCENT_HOVER = "#339CFF"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#8E8E93"


class LoginView(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg=BG_COLOR)
        self.master = master
        self.create_widgets()

    def create_widgets(self):

        # ===== CARD CENTRAL =====
        container = tk.Frame(self, bg=CARD_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center", width=420, height=480)

        # Título
        tk.Label(
            container,
            text="Plataforma de Tutorías",
            font=("Helvetica", 22, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(40, 25))

        # Usuario label
        tk.Label(container, text="Usuario",
                 bg=CARD_COLOR,
                 fg=SECONDARY_TEXT,
                 font=("Helvetica", 10)).pack()

        # Input moderno
        self.username_entry = tk.Entry(
            container,
            font=("Helvetica", 13),
            bg=INPUT_COLOR,
            fg=TEXT_COLOR,
            insertbackground="white",
            relief="flat",
            highlightthickness=0
        )
        self.username_entry.pack(pady=12, ipady=10, ipadx=12)

        # Rol label
        tk.Label(container, text="Rol",
                 bg=CARD_COLOR,
                 fg=SECONDARY_TEXT,
                 font=("Helvetica", 10)).pack(pady=(15, 5))

        self.role_var = tk.StringVar()
        self.role_var.set("estudiante")

        roles = [("Administrador", "admin"),
                 ("Tutor", "tutor"),
                 ("Estudiante", "estudiante")]

        for text, value in roles:
            tk.Radiobutton(
                container,
                text=text,
                variable=self.role_var,
                value=value,
                bg=CARD_COLOR,
                fg=TEXT_COLOR,
                selectcolor=INPUT_COLOR,
                activebackground=CARD_COLOR,
                activeforeground=TEXT_COLOR,
                font=("Helvetica", 11),
                cursor="hand2"
            ).pack(anchor="w", padx=110, pady=2)

        # ===== BOTÓN APPLE =====
        login_btn = tk.Button(
            container,
            text="Ingresar",
            command=self.login,
            bg=ACCENT_COLOR,
            fg="white",
            font=("Helvetica", 12, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground=ACCENT_HOVER,
            activeforeground="white"
        )
        login_btn.pack(pady=40, ipadx=30, ipady=10)

        # Hover effect
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg=ACCENT_HOVER))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg=ACCENT_COLOR))

    # ==============================
    # LÓGICA LOGIN
    # ==============================

    def login(self):
        username = self.username_entry.get()
        role = self.role_var.get()

        if not username:
            messagebox.showerror("Error", "Debe ingresar un usuario")
            return

        user = User(username, role)
        self.redirect(user)

    # ==============================
    # REDIRECCIÓN SIN CIRCULAR IMPORT
    # ==============================

    def redirect(self, user):
        self.destroy()

        if user.role == "admin":
            from views.admin_view import AdminView
            view = AdminView(self.master, user)

        elif user.role == "tutor":
            from views.tutor_view import TutorView
            view = TutorView(self.master, user)

        else:
            from views.student_view import StudentView
            view = StudentView(self.master, user)

        view.pack(fill="both", expand=True)