import tkinter as tk
from data.mock_data import AVAILABLE_SESSIONS

BG_COLOR = "#0F1115"
CARD_COLOR = "#1C1F26"
ACCENT_COLOR = "#0A84FF"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#A1A1A6"


class TutorView(tk.Frame):

    def __init__(self, master, user):
        super().__init__(master, bg=BG_COLOR)
        self.master = master  # ✅ IMPORTANTE
        self.user = user
        self.create_widgets()

    def create_widgets(self):

        container = tk.Frame(self, bg=CARD_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        # Título
        tk.Label(
            container,
            text="Panel Tutor",
            font=("Helvetica", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)

        # Bienvenida
        tk.Label(
            container,
            text=f"Bienvenido {self.user.username}",
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(pady=5)

        tk.Label(
            container,
            text="Mis Tutorías Asignadas",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=("Helvetica", 14)
        ).pack(pady=20)

        found_sessions = False

        for session in AVAILABLE_SESSIONS:

            if session.tutor_name == self.user.username:

                found_sessions = True

                tk.Label(
                    container,
                    text=f"{session.subject} | {session.date} | {session.time}",
                    bg=CARD_COLOR,
                    fg="#0A84FF",
                    font=("Helvetica", 12, "bold")
                ).pack(pady=8)

                if session.students:
                    for student in session.students:
                        tk.Label(
                            container,
                            text=f"   • {student['name']} | {student['career']} | {student['email']}",
                            bg=CARD_COLOR,
                            fg=SECONDARY_TEXT
                        ).pack(anchor="w", padx=120)
                else:
                    tk.Label(
                        container,
                        text="   Sin estudiantes inscritos",
                        bg=CARD_COLOR,
                        fg="#777777"
                    ).pack(anchor="w", padx=120)

                tk.Label(container, text="").pack()

        if not found_sessions:
            tk.Label(
                container,
                text="No tienes tutorías asignadas",
                bg=CARD_COLOR,
                fg="#777777"
            ).pack(pady=20)

        # ==============================
        # 🔥 BOTÓN VOLVER
        # ==============================

        back_btn = tk.Button(
            container,
            text="← Volver",
            command=self.go_back,
            bg="#2A2A2E",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#3A3A3C",
            activeforeground="white"
        )
        back_btn.pack(pady=20, ipadx=15, ipady=6)

    # ==============================
    # 🔥 MÉTODO VOLVER
    # ==============================

    def go_back(self):
        self.destroy()
        from views.login_view import LoginView
        LoginView(self.master).pack(fill="both", expand=True)