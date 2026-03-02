import tkinter as tk
from tkinter import Toplevel, Entry, Button, Label, messagebox
from data.mock_data import AVAILABLE_SESSIONS

BG_COLOR = "#0F1115"
CARD_COLOR = "#1C1F26"
ACCENT_COLOR = "#0A84FF"
TEXT_COLOR = "#FFFFFF"
SECONDARY_TEXT = "#A1A1A6"


class AdminView(tk.Frame):

    def __init__(self, master, user):
        super().__init__(master, bg=BG_COLOR)
        self.master = master
        self.user = user
        self.create_widgets()

    def create_widgets(self):

        container = tk.Frame(self, bg=CARD_COLOR)
        container.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        tk.Label(
            container,
            text="Panel Administrador",
            font=("Helvetica", 18, "bold"),
            bg=CARD_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=20)

        tk.Label(
            container,
            text=f"Bienvenido {self.user.username}",
            bg=CARD_COLOR,
            fg=SECONDARY_TEXT
        ).pack(pady=10)

        Button(container, text="Gestionar Tutores",
               bg=ACCENT_COLOR, fg="white",
               command=self.manage_tutors).pack(pady=10, ipadx=15, ipady=6)

        Button(container, text="Gestionar Estudiantes",
               bg=ACCENT_COLOR, fg="white",
               command=self.manage_students).pack(pady=10, ipadx=15, ipady=6)

        Button(container, text="Ver Reportes",
               bg=ACCENT_COLOR, fg="white",
               command=self.show_reports).pack(pady=10, ipadx=15, ipady=6)

        # ===== BOTÓN VOLVER =====
        back_btn = Button(
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
        back_btn.pack(pady=25, ipadx=15, ipady=6)

    # ==============================
    # MÉTODO VOLVER (SIN IMPORT ARRIBA)
    # ==============================

    def go_back(self):
        self.destroy()
        from views.login_view import LoginView
        LoginView(self.master).pack(fill="both", expand=True)

    # ====================================
    # GESTIÓN DE TUTORES
    # ====================================

    def manage_tutors(self):

        window = Toplevel(self)
        window.title("Gestionar Tutores")
        window.geometry("500x400")
        window.configure(bg=BG_COLOR)

        Label(window, text="Tutores Actuales",
              bg=BG_COLOR, fg=TEXT_COLOR,
              font=("Helvetica", 14)).pack(pady=10)

        tutors = list(set(session.tutor_name for session in AVAILABLE_SESSIONS))

        for tutor in tutors:
            Label(window, text=tutor,
                  bg=BG_COLOR, fg=SECONDARY_TEXT).pack()

        Label(window, text="Agregar Nuevo Tutor",
              bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=10)

        tutor_entry = Entry(window)
        tutor_entry.pack()

        def add_tutor():
            new_tutor = tutor_entry.get()
            if not new_tutor:
                return

            from models.tutoring_session import TutoringSession
            AVAILABLE_SESSIONS.append(
                TutoringSession(new_tutor, "Nueva Materia", "Pendiente", "Pendiente")
            )

            messagebox.showinfo("Éxito", "Tutor agregado")
            window.destroy()

        Button(window, text="Agregar",
               bg=ACCENT_COLOR, fg="white",
               command=add_tutor).pack(pady=10)

    # ====================================
    # GESTIÓN DE ESTUDIANTES
    # ====================================

    def manage_students(self):

        window = Toplevel(self)
        window.title("Gestionar Estudiantes")
        window.geometry("600x500")
        window.configure(bg=BG_COLOR)

        Label(window, text="Estudiantes Inscritos",
              bg=BG_COLOR, fg=TEXT_COLOR,
              font=("Helvetica", 14)).pack(pady=10)

        for session in AVAILABLE_SESSIONS:

            Label(window,
                  text=f"{session.subject} - {session.tutor_name}",
                  bg=BG_COLOR,
                  fg="#0A84FF").pack(pady=5)

            if session.students:
                for student in session.students:

                    frame = tk.Frame(window, bg=BG_COLOR)
                    frame.pack(fill="x")

                    Label(frame,
                          text=student["name"],
                          bg=BG_COLOR,
                          fg=SECONDARY_TEXT).pack(side="left", padx=10)

                    def remove_student(s=session, st=student):
                        s.students.remove(st)
                        window.destroy()
                        self.manage_students()

                    Button(frame,
                           text="Eliminar",
                           bg="red",
                           fg="white",
                           command=remove_student).pack(side="right", padx=10)
            else:
                Label(window,
                      text="Sin inscritos",
                      bg=BG_COLOR,
                      fg="#777777").pack()

    # ====================================
    # REPORTES
    # ====================================

    def show_reports(self):

        window = Toplevel(self)
        window.title("Reportes")
        window.geometry("600x400")
        window.configure(bg=BG_COLOR)

        total_sessions = len(AVAILABLE_SESSIONS)
        total_students = sum(len(s.students) for s in AVAILABLE_SESSIONS)

        Label(window,
              text="Reportes del Sistema",
              bg=BG_COLOR,
              fg=TEXT_COLOR,
              font=("Helvetica", 16)).pack(pady=20)

        Label(window,
              text=f"Total Tutorías: {total_sessions}",
              bg=BG_COLOR,
              fg=SECONDARY_TEXT).pack(pady=5)

        Label(window,
              text=f"Total Inscripciones: {total_students}",
              bg=BG_COLOR,
              fg=SECONDARY_TEXT).pack(pady=5)

        for session in AVAILABLE_SESSIONS:
            Label(window,
                  text=f"{session.subject} | {session.tutor_name} | {len(session.students)} inscritos",
                  bg=BG_COLOR,
                  fg="#0A84FF").pack()