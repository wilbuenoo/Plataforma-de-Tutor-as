import tkinter as tk
from tkinter import Toplevel, Label, Entry, Button, messagebox
from data.mock_data import AVAILABLE_SESSIONS

BG_COLOR = "#0F1115"
CARD_COLOR = "#1C1F26"
ACCENT_COLOR = "#0A84FF"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#A1A1A6"


class StudentView(tk.Frame):

    def __init__(self, master, user):
        super().__init__(master, bg=BG_COLOR)
        self.master = master  # ✅ IMPORTANTE
        self.user = user
        self.create_widgets()

    def create_widgets(self):

        container = tk.Frame(self, bg=CARD_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center", width=650, height=500)

        # Título
        tk.Label(
            container,
            text="Panel Estudiante",
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

        # Subtítulo
        tk.Label(
            container,
            text="Tutorías Disponibles",
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            font=("Helvetica", 14)
        ).pack(pady=15)

        # Listado de tutorías
        for session in AVAILABLE_SESSIONS:
            btn = tk.Button(
                container,
                text=f"{session.subject} | {session.tutor_name} | {session.date} {session.time}",
                bg=ACCENT_COLOR,
                fg="white",
                font=("Helvetica", 11),
                relief="flat",
                cursor="hand2",
                command=lambda s=session: self.open_enrollment_form(s)
            )
            btn.pack(pady=6, ipadx=10, ipady=6)

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

    # ===============================
    # FORMULARIO DE INSCRIPCIÓN
    # ===============================

    def open_enrollment_form(self, session):

        form = Toplevel(self)
        form.title("Datos del Estudiante")
        form.geometry("400x400")
        form.configure(bg=CARD_COLOR)
        form.resizable(False, False)

        tk.Label(form, text="Completa tus datos",
                 bg=CARD_COLOR,
                 fg=TEXT_COLOR,
                 font=("Helvetica", 14, "bold")).pack(pady=15)

        tk.Label(form, text="Correo",
                 bg=CARD_COLOR,
                 fg=SECONDARY_TEXT).pack()
        email_entry = Entry(form, bg="#2C2F36", fg="white", relief="flat")
        email_entry.pack(pady=5, ipady=5, ipadx=5)

        tk.Label(form, text="Carrera",
                 bg=CARD_COLOR,
                 fg=SECONDARY_TEXT).pack()
        career_entry = Entry(form, bg="#2C2F36", fg="white", relief="flat")
        career_entry.pack(pady=5, ipady=5, ipadx=5)

        tk.Label(form, text="Código Estudiantil",
                 bg=CARD_COLOR,
                 fg=SECONDARY_TEXT).pack()
        code_entry = Entry(form, bg="#2C2F36", fg="white", relief="flat")
        code_entry.pack(pady=5, ipady=5, ipadx=5)

        tk.Label(form, text="Motivo de la tutoría",
                 bg=CARD_COLOR,
                 fg=SECONDARY_TEXT).pack()
        reason_entry = Entry(form, bg="#2C2F36", fg="white", relief="flat")
        reason_entry.pack(pady=5, ipady=5, ipadx=5)

        def confirm():

            if not email_entry.get() or not career_entry.get():
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            student_data = {
                "name": self.user.username,
                "email": email_entry.get(),
                "career": career_entry.get(),
                "code": code_entry.get(),
                "reason": reason_entry.get()
            }

            session.enroll_student(student_data)

            form.destroy()

            messagebox.showinfo(
                "Inscripción Exitosa",
                f"Te inscribiste a {session.subject} con {session.tutor_name}"
            )

        tk.Button(
            form,
            text="Confirmar Inscripción",
            command=confirm,
            bg=ACCENT_COLOR,
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            cursor="hand2"
        ).pack(pady=20, ipadx=10, ipady=6)