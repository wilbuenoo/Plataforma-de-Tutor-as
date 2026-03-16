from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame, QListWidget, QLineEdit, QMessageBox,
    QDateEdit, QTableWidget, QTableWidgetItem, QComboBox, QGraphicsOpacityEffect
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QDate, QPropertyAnimation, QTimer

BG_COLOR = "#1e1e1e"
SIDEBAR_COLOR = "#191919"
CARD_COLOR = "#2a2a2a"
HOVER_COLOR = "#323232"
BORDER_COLOR = "#3a3a3a"

ACCENT_COLOR = "#1DB954"
DANGER_COLOR = "#ff453a"
TEXT_COLOR = "#ffffff"

# ===== COMPONENTE DE NOTIFICACIÓN TIPO APPLE =====
class AppleToast(QFrame):
    def __init__(self, parent, message):
        super().__init__(parent)
        self.setFixedSize(300, 50)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(40, 40, 40, 240);
                border: 1px solid {BORDER_COLOR};
                border-radius: 25px;
            }}
            QLabel {{
                color: white;
                background: transparent;
                font-size: 10pt;
                font-weight: bold;
            }}
        """)
        
        layout = QHBoxLayout(self)
        icon = QLabel("✨")
        text = QLabel(message)
        layout.addWidget(icon)
        layout.addWidget(text)
        layout.addStretch()

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(500)
        
        parent_rect = parent.rect()
        self.move((parent_rect.width() - 300) // 2, parent_rect.height() - 80)
        
        self.show_toast()

    def show_toast(self):
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        self.anim.start()
        QTimer.singleShot(2500, self.hide_toast)

    def hide_toast(self):
        self.anim.setDirection(QPropertyAnimation.Direction.Backward)
        self.anim.finished.connect(self.deleteLater)
        self.anim.start()

# ===== CLASE PRINCIPAL DASHBOARD =====
class DashboardView(QWidget):

    def __init__(self, user, login_reference=None):
        super().__init__()
        self.user = user
        self.login_window = login_reference

        # Datos del sistema
        self.system_data = {
            "materias": ["Matemáticas", "Programación", "Física"],
            "disponibilidades": [],  # Publicadas por docentes
            "solicitudes": [],
            "historial": [],
            "estudiantes": {  # Materias y carreras por estudiante
                "Alice": {"Computer Science": ["Programming Abstractions", "Artificial Intelligence"]},
                "Bob": {"Mechanical Engineering": ["Thermodynamics", "Dynamic Systems & Control"]},
                "Charlie": {"Electrical Engineering": ["Circuits I", "Control Systems"]}
            }
        }

        # Datos de carreras y materias de Oxford
        self.oxford_data = {
            "Computer Science": {
                "Semestre 1": ["Intro to Programming", "Data Structures"],
                "Semestre 2": ["Algorithms", "Databases"],
                "Semestre 3": ["AI & ML", "Computer Networks"]
            },
            "Mechanical Engineering": {
                "Semestre 1": ["Statics", "Thermodynamics I"],
                "Semestre 2": ["Dynamics", "Fluid Mechanics"],
                "Semestre 3": ["Heat Transfer", "Mechanical Design"]
            },
            "Electrical Engineering": {
                "Semestre 1": ["Circuit Theory", "Digital Logic"],
                "Semestre 2": ["Signals & Systems", "Electromagnetics"],
                "Semestre 3": ["Control Systems", "Power Electronics"]
            }
        }

        self.setWindowTitle("Plataforma de Tutorías")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet(f"background-color:{BG_COLOR}; color:{TEXT_COLOR};")

        self.init_ui()

    # --------------------- ESTILOS ---------------------
    def style_input(self, w):
        w.setStyleSheet(f"""
            QLineEdit, QComboBox, QDateEdit {{
                background-color:{CARD_COLOR};
                border-radius:6px;
                padding:8px;
                border:1px solid {BORDER_COLOR};
                color: {TEXT_COLOR};
            }}
            QLineEdit:focus, QComboBox:focus {{
                border:1px solid {ACCENT_COLOR};
                background-color:{HOVER_COLOR};
            }}
        """)

    def style_list(self, w):
        w.setStyleSheet(f"""
            QListWidget {{
                background-color:{CARD_COLOR};
                border-radius:8px;
                border:1px solid {BORDER_COLOR};
                padding: 5px;
            }}
            QListWidget::item {{ padding: 10px; border-bottom: 1px solid {BORDER_COLOR}; }}
            QListWidget::item:selected {{ background-color: {ACCENT_COLOR}; color: black; border-radius: 5px; }}
        """)

    def style_action_button(self, btn):
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT_COLOR};
                color: black;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 11pt;
            }}
            QPushButton:hover {{ background-color: #1ed760; }}
            QPushButton:pressed {{ background-color: #169c46; }}
        """)

    # --------------------- UI PRINCIPAL ---------------------
    def init_ui(self):
        root_layout = QHBoxLayout(self)
        root_layout.setContentsMargins(0,0,0,0)
        root_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"background-color:{SIDEBAR_COLOR}; border-right:1px solid {BORDER_COLOR};")
        sidebar_layout = QVBoxLayout(sidebar)

        profile_container = QLabel()
        profile_container.setFixedSize(100, 100)
        profile_container.setText(self.user['username'][0].upper())
        profile_container.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_container.setStyleSheet(f"background-color: {CARD_COLOR}; color: {ACCENT_COLOR}; border-radius: 50px; border: 2px solid {BORDER_COLOR}; font-size: 30pt; font-weight: bold;")
        
        sidebar_layout.addSpacing(20)
        sidebar_layout.addWidget(profile_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        name_label = QLabel(self.user['username'])
        name_label.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        sidebar_layout.addWidget(name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        role_label = QLabel(self.user['role'])
        role_label.setStyleSheet("color: #888;")
        sidebar_layout.addWidget(role_label, alignment=Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addSpacing(30)
        
        content_widget = QWidget()
        self.main_layout = QVBoxLayout(content_widget)
        
        welcome = QLabel(f"Panel de Control")
        welcome.setFont(QFont("Helvetica", 24, QFont.Weight.Bold))
        self.main_layout.addWidget(welcome)

        self.grid_container = QWidget()
        self.grid = QGridLayout(self.grid_container)
        
        # Opciones por rol
        if self.user["role"] == "Administrador":
            options = ["Gestionar Usuarios", "Asignar Roles", "Administrar Materias", "Ver Reportes"]
        elif self.user["role"] == "Docente":
            options = ["Publicar Disponibilidad", "Ver Solicitudes", "Registrar Tutoría", "Historial de Tutorías"]
        else:
            options = ["Buscar Tutorías", "Solicitar Tutoría", "Mis Tutorías", "Historial Académico"]

        row = col = 0
        for option in options:
            btn = QPushButton(option)
            btn.setFixedSize(220, 100)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color:{CARD_COLOR};
                    border-radius:12px;
                    border:1px solid {BORDER_COLOR};
                    color:{TEXT_COLOR};
                    font-size:12pt;
                    font-weight:bold;
                }}
                QPushButton:hover {{ background-color:{HOVER_COLOR}; border:1px solid {ACCENT_COLOR}; }}
            """)
            btn.clicked.connect(lambda checked, text=option: self.show_section(text))
            self.grid.addWidget(btn, row, col)
            col += 1
            if col > 1: col = 0; row += 1

        self.main_layout.addWidget(self.grid_container)
        
        self.section_widget = QFrame()
        self.section_container = QVBoxLayout(self.section_widget)
        self.main_layout.addWidget(self.section_widget)
        self.section_widget.hide() 

        self.main_layout.addStretch()
        sidebar_layout.addStretch()

        # Cambiar rol
        btn_cambiar_rol = QPushButton("⇄ Cambiar Rol")
        btn_cambiar_rol.setStyleSheet(f"background-color:{DANGER_COLOR}; color:white; border-radius:8px; padding:10px; font-weight:bold; margin-bottom:5px;")
        btn_cambiar_rol.clicked.connect(self.regresar_al_login)
        sidebar_layout.addWidget(btn_cambiar_rol)

        # Cerrar sesión
        logout_btn = QPushButton("↩ Cerrar Sesión")
        logout_btn.setStyleSheet(f"background-color:{DANGER_COLOR}; color:white; border-radius:8px; padding:10px; font-weight:bold;")
        logout_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(logout_btn)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content_widget)

    # --------------------- FUNCIONES AUX ---------------------
    def show_message(self, text):
        self.toast = AppleToast(self, text)

    def clear_section(self):
        self.grid_container.hide()
        self.section_widget.show()
        while self.section_container.count():
            item = self.section_container.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def load_table(self, table, data, keys):
        table.setRowCount(0)
        for item in data:
            row = table.rowCount()
            table.insertRow(row)
            for col, key in enumerate(keys):
                table.setItem(row, col, QTableWidgetItem(str(item.get(key, ""))))


    # --------------------- SECCIONES ---------------------
    def show_section(self, section):
        self.clear_section()
        btn_back = QPushButton("← Volver al Menú")
        btn_back.setStyleSheet("color: #1DB954; background: transparent; border: none; text-align: left; font-size: 11pt;")
        btn_back.clicked.connect(lambda: [self.section_widget.hide(), self.grid_container.show()])
        self.section_container.addWidget(btn_back)

        title = QLabel(section)
        title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        self.section_container.addWidget(title)
        self.section_container.addSpacing(10)

        # ---------------- DOCENTE ----------------
        if self.user["role"] == "Docente":

            # ---------------- Publicar Disponibilidad ----------------
            if section == "Publicar Disponibilidad":
                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Estudiante", "Carrera", "Materia", "Fecha"])
                self.section_container.addWidget(table)

                student_input = QComboBox(); self.style_input(student_input)
                student_input.addItems(list(self.system_data["estudiantes"].keys()))

                carrera_input = QComboBox(); self.style_input(carrera_input)
                materia_input = QComboBox(); self.style_input(materia_input)

                fecha_input = QDateEdit()
                fecha_input.setCalendarPopup(True)
                fecha_input.setDate(QDate.currentDate())
                self.style_input(fecha_input)

                def update_carreras():
                    estudiante = student_input.currentText()
                    carrera_input.clear()

                    if estudiante in self.system_data["estudiantes"]:
                        carrera_input.addItems(
                            list(self.system_data["estudiantes"][estudiante].keys())
                        )
                        update_materias()

                def update_materias():
                    estudiante = student_input.currentText()
                    carrera = carrera_input.currentText()
                    materia_input.clear()

                    if estudiante in self.system_data["estudiantes"]:
                        materias = self.system_data["estudiantes"][estudiante].get(carrera, [])
                        materia_input.addItems(materias)

                student_input.currentTextChanged.connect(update_carreras)
                carrera_input.currentTextChanged.connect(update_materias)

                update_carreras()

                btn_add = QPushButton("Publicar Disponibilidad")
                self.style_action_button(btn_add)

                def add_disp():

                    est = student_input.currentText()
                    car = carrera_input.currentText()
                    mat = materia_input.currentText()
                    fec = fecha_input.date().toString("dd/MM/yyyy")

                    if est and mat:

                        self.system_data["disponibilidades"].append({
                            "estudiante": est,
                            "carrera": car,
                            "materia": mat,
                            "fecha": fec
                        })

                        row = table.rowCount()
                        table.insertRow(row)

                        table.setItem(row,0,QTableWidgetItem(est))
                        table.setItem(row,1,QTableWidgetItem(car))
                        table.setItem(row,2,QTableWidgetItem(mat))
                        table.setItem(row,3,QTableWidgetItem(fec))

                        self.show_message("Disponibilidad publicada")

                    else:
                        self.show_message("Completa los campos")

                btn_add.clicked.connect(add_disp)

                self.section_container.addWidget(QLabel("Estudiante"))
                self.section_container.addWidget(student_input)

                self.section_container.addWidget(QLabel("Carrera"))
                self.section_container.addWidget(carrera_input)

                self.section_container.addWidget(QLabel("Materia"))
                self.section_container.addWidget(materia_input)

                self.section_container.addWidget(QLabel("Fecha"))
                self.section_container.addWidget(fecha_input)

                self.section_container.addWidget(btn_add)

            # ---------------- Ver Solicitudes ----------------
            elif section == "Ver Solicitudes":

                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Estudiante","Carrera","Materia","Fecha"])
                self.section_container.addWidget(table)

                for s in self.system_data["solicitudes"]:

                    row = table.rowCount()
                    table.insertRow(row)

                    table.setItem(row,0,QTableWidgetItem(s.get("estudiante","")))
                    table.setItem(row,1,QTableWidgetItem(s.get("carrera","")))
                    table.setItem(row,2,QTableWidgetItem(s.get("materia","")))
                    table.setItem(row,3,QTableWidgetItem(s.get("fecha","")))

            # ---------------- Registrar Tutoría ----------------
            elif section == "Registrar Tutoría":

                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Estudiante","Carrera","Materia","Fecha"])
                self.section_container.addWidget(table)

                student_input = QComboBox()
                self.style_input(student_input)
                student_input.addItems(list(self.system_data["estudiantes"].keys()))

                carrera_input = QComboBox()
                self.style_input(carrera_input)

                materia_input = QComboBox()
                self.style_input(materia_input)

                fecha_input = QDateEdit()
                fecha_input.setCalendarPopup(True)
                fecha_input.setDate(QDate.currentDate())
                self.style_input(fecha_input)

                def update_carreras():

                    estudiante = student_input.currentText()
                    carrera_input.clear()

                    if estudiante in self.system_data["estudiantes"]:
                        carrera_input.addItems(
                            list(self.system_data["estudiantes"][estudiante].keys())
                        )
                        update_materias()

                def update_materias():

                    estudiante = student_input.currentText()
                    carrera = carrera_input.currentText()

                    materia_input.clear()

                    if estudiante in self.system_data["estudiantes"]:
                        materias = self.system_data["estudiantes"][estudiante].get(carrera, [])
                        materia_input.addItems(materias)

                student_input.currentTextChanged.connect(update_carreras)
                carrera_input.currentTextChanged.connect(update_materias)

                update_carreras()

                btn_add = QPushButton("Registrar Tutoría")
                self.style_action_button(btn_add)

                def add_tutoria():

                    est = student_input.currentText()
                    car = carrera_input.currentText()
                    mat = materia_input.currentText()
                    fec = fecha_input.date().toString("dd/MM/yyyy")

                    if est and car and mat:

                        self.system_data["historial"].append({
                            "estudiante": est,
                            "carrera": car,
                            "materia": mat,
                            "fecha": fec
                        })

                        row = table.rowCount()
                        table.insertRow(row)

                        table.setItem(row,0,QTableWidgetItem(est))
                        table.setItem(row,1,QTableWidgetItem(car))
                        table.setItem(row,2,QTableWidgetItem(mat))
                        table.setItem(row,3,QTableWidgetItem(fec))

                        self.show_message("Tutoría registrada")

                    else:
                        self.show_message("Completa todos los campos")

                btn_add.clicked.connect(add_tutoria)

                self.section_container.addWidget(QLabel("Estudiante"))
                self.section_container.addWidget(student_input)

                self.section_container.addWidget(QLabel("Carrera"))
                self.section_container.addWidget(carrera_input)

                self.section_container.addWidget(QLabel("Materia"))
                self.section_container.addWidget(materia_input)

                self.section_container.addWidget(QLabel("Fecha"))
                self.section_container.addWidget(fecha_input)

                self.section_container.addWidget(btn_add)


            # ---------------- Historial de Tutorías ----------------
            elif section == "Historial de Tutorías":

                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Estudiante","Carrera","Materia","Fecha"])
                self.section_container.addWidget(table)

                self.load_table(
                    table,
                    self.system_data["historial"],
                    ["estudiante","carrera","materia","fecha"]
                )


            # ---------------- ESTUDIANTE ----------------
            if self.user["role"] == "Estudiante":

            # ---------------- Buscar Tutorías ----------------
                if section == "Buscar Tutorías":
                    table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Docente", "Carrera", "Materia", "Fecha"])
                self.section_container.addWidget(table)
                for d in self.system_data["disponibilidades"]:
                    row = table.rowCount()
                    table.insertRow(row)
                    table.setItem(row, 0, QTableWidgetItem(d.get("estudiante","")))
                    table.setItem(row, 1, QTableWidgetItem(d.get("carrera","")))
                    table.setItem(row, 2, QTableWidgetItem(d.get("materia","")))
                    table.setItem(row, 3, QTableWidgetItem(d.get("fecha","")))

            # ---------------- Solicitar Tutoría ----------------
            elif section == "Solicitar Tutoría":
                student_name = self.user['username']
                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Carrera", "Materia", "Fecha Solicitud", "Docente"])
                self.section_container.addWidget(table)

                carrera_input = QComboBox(); self.style_input(carrera_input)
                materia_input = QComboBox(); self.style_input(materia_input)
                fecha_input = QDateEdit(); fecha_input.setCalendarPopup(True); fecha_input.setDate(QDate.currentDate()); self.style_input(fecha_input)

                if student_name in self.system_data["estudiantes"]:
                    carreras = list(self.system_data["estudiantes"][student_name].keys())
                    carrera_input.addItems(carreras)
                    materia_input.addItems(self.system_data["estudiantes"][student_name][carreras[0]])

                def update_materias():
                    carrera = carrera_input.currentText()
                    materia_input.clear()
                    materias = self.system_data["estudiantes"][student_name].get(carrera, [])
                    materia_input.addItems(materias)

                carrera_input.currentTextChanged.connect(update_materias)

                btn_add = QPushButton("Solicitar Tutoría"); self.style_action_button(btn_add)
                def add_solicitud():
                    car = carrera_input.currentText()
                    mat = materia_input.currentText()
                    fec = fecha_input.date().toString("dd/MM/yyyy")
                    self.system_data["solicitudes"].append({"estudiante": student_name, "carrera": car, "materia": mat, "fecha": fec})
                    row = table.rowCount()
                    table.insertRow(row)
                    table.setItem(row, 0, QTableWidgetItem(car))
                    table.setItem(row, 1, QTableWidgetItem(mat))
                    table.setItem(row, 2, QTableWidgetItem(fec))
                    table.setItem(row, 3, QTableWidgetItem("Docente"))
                    self.show_message(f"Tutoría solicitada: {mat}")
                btn_add.clicked.connect(add_solicitud)

                self.section_container.addWidget(QLabel("Carrera:")); self.section_container.addWidget(carrera_input)
                self.section_container.addWidget(QLabel("Materia:")); self.section_container.addWidget(materia_input)
                self.section_container.addWidget(QLabel("Fecha:")); self.section_container.addWidget(fecha_input)
                self.section_container.addWidget(btn_add)

            # ---------------- Mis Tutorías ----------------
            elif section == "Mis Tutorías":
                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Carrera", "Materia", "Fecha", "Estado"])
                self.section_container.addWidget(table)
                for s in self.system_data["solicitudes"]:
                    if s.get("estudiante") == self.user['username']:
                        row = table.rowCount()
                        table.insertRow(row)
                        table.setItem(row, 0, QTableWidgetItem(s.get("carrera","")))
                        table.setItem(row, 1, QTableWidgetItem(s.get("materia","")))
                        table.setItem(row, 2, QTableWidgetItem(s.get("fecha","")))
                        table.setItem(row, 3, QTableWidgetItem("Pendiente"))

            # ---------------- Historial Académico ----------------
            elif section == "Historial Académico":
                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Carrera", "Materia", "Fecha", "Docente"])
                self.section_container.addWidget(table)
                for h in self.system_data["historial"]:
                    if h.get("estudiante") == self.user['username']:
                        row = table.rowCount()
                        table.insertRow(row)
                        table.setItem(row, 0, QTableWidgetItem(h.get("carrera","")))
                        table.setItem(row, 1, QTableWidgetItem(h.get("materia","")))
                        table.setItem(row, 2, QTableWidgetItem(h.get("fecha","")))
                        table.setItem(row, 3, QTableWidgetItem("Docente"))

        self.section_container.addStretch()

                # ---------------- ADMINISTRADOR ----------------
        if self.user["role"] == "Administrador":

            # Base de usuarios del sistema
            if "usuarios" not in self.system_data:
                self.system_data["usuarios"] = [
                    {"username": "Alice", "role": "Estudiante"},
                    {"username": "Bob", "role": "Docente"},
                    {"username": "Charlie", "role": "Estudiante"}
                ]

            if "reportes" not in self.system_data:
                self.system_data["reportes"] = []

            # ---------------- Gestionar Usuarios ----------------
            if section == "Gestionar Usuarios":

                table = QTableWidget()
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels(["Usuario", "Rol"])
                self.section_container.addWidget(table)

                def load_users():
                    table.setRowCount(0)
                    for u in self.system_data["usuarios"]:
                        row = table.rowCount()
                        table.insertRow(row)
                        table.setItem(row,0,QTableWidgetItem(u["username"]))
                        table.setItem(row,1,QTableWidgetItem(u["role"]))

                load_users()

                username_input = QLineEdit()
                self.style_input(username_input)

                role_input = QComboBox()
                role_input.addItems(["Estudiante","Docente","Administrador"])
                self.style_input(role_input)

                btn_add = QPushButton("Crear Usuario")
                self.style_action_button(btn_add)

                def add_user():
                    name = username_input.text()
                    role = role_input.currentText()

                    if name:
                        self.system_data["usuarios"].append({
                            "username": name,
                            "role": role
                        })
                        load_users()
                        username_input.clear()
                        self.show_message(f"Usuario {name} creado")
                    else:
                        self.show_message("Ingresa un nombre de usuario")

                btn_add.clicked.connect(add_user)

                self.section_container.addWidget(QLabel("Usuario"))
                self.section_container.addWidget(username_input)

                self.section_container.addWidget(QLabel("Rol"))
                self.section_container.addWidget(role_input)

                self.section_container.addWidget(btn_add)

            # ---------------- Asignar Roles ----------------
            elif section == "Asignar Roles":

                table = QTableWidget()
                table.setColumnCount(2)
                table.setHorizontalHeaderLabels(["Usuario","Rol"])
                self.section_container.addWidget(table)

                def load_users():
                    table.setRowCount(0)
                    for u in self.system_data["usuarios"]:
                        row = table.rowCount()
                        table.insertRow(row)
                        table.setItem(row,0,QTableWidgetItem(u["username"]))
                        table.setItem(row,1,QTableWidgetItem(u["role"]))

                load_users()

                user_select = QComboBox()
                self.style_input(user_select)

                role_select = QComboBox()
                role_select.addItems(["Estudiante","Docente","Administrador"])
                self.style_input(role_select)

                def refresh_users():
                    user_select.clear()
                    for u in self.system_data["usuarios"]:
                        user_select.addItem(u["username"])

                refresh_users()

                btn_change = QPushButton("Cambiar Rol")
                self.style_action_button(btn_change)

                def change_role():
                    user = user_select.currentText()
                    role = role_select.currentText()

                    for u in self.system_data["usuarios"]:
                        if u["username"] == user:
                            u["role"] = role

                    load_users()
                    self.show_message(f"{user} ahora es {role}")

                btn_change.clicked.connect(change_role)

                self.section_container.addWidget(QLabel("Usuario"))
                self.section_container.addWidget(user_select)

                self.section_container.addWidget(QLabel("Nuevo Rol"))
                self.section_container.addWidget(role_select)

                self.section_container.addWidget(btn_change)

            # ---------------- Administrar Materias ----------------
            elif section == "Administrar Materias":

                table = QTableWidget()
                table.setColumnCount(3)
                table.setHorizontalHeaderLabels(["Carrera","Semestre","Materia"])
                self.section_container.addWidget(table)

                def load_subjects():
                    table.setRowCount(0)
                    for carrera in self.oxford_data:
                        for semestre in self.oxford_data[carrera]:
                            for materia in self.oxford_data[carrera][semestre]:
                                row = table.rowCount()
                                table.insertRow(row)
                                table.setItem(row,0,QTableWidgetItem(carrera))
                                table.setItem(row,1,QTableWidgetItem(semestre))
                                table.setItem(row,2,QTableWidgetItem(materia))

                load_subjects()

                carrera_input = QComboBox()
                carrera_input.addItems(list(self.oxford_data.keys()))
                self.style_input(carrera_input)

                semestre_input = QComboBox()
                semestre_input.addItems(["Semestre 1","Semestre 2","Semestre 3"])
                self.style_input(semestre_input)

                materia_input = QLineEdit()
                self.style_input(materia_input)

                btn_add = QPushButton("Agregar Materia")
                self.style_action_button(btn_add)

                def add_subject():

                    carrera = carrera_input.currentText()
                    semestre = semestre_input.currentText()
                    materia = materia_input.text()

                    if materia:

                        if carrera not in self.oxford_data:
                            self.oxford_data[carrera] = {}

                        if semestre not in self.oxford_data[carrera]:
                            self.oxford_data[carrera][semestre] = []

                        self.oxford_data[carrera][semestre].append(materia)

                        load_subjects()

                        materia_input.clear()

                        self.show_message("Materia agregada")

                btn_add.clicked.connect(add_subject)

                self.section_container.addWidget(QLabel("Carrera"))
                self.section_container.addWidget(carrera_input)

                self.section_container.addWidget(QLabel("Semestre"))
                self.section_container.addWidget(semestre_input)

                self.section_container.addWidget(QLabel("Materia"))
                self.section_container.addWidget(materia_input)

                self.section_container.addWidget(btn_add)

            # ---------------- Ver Reportes ----------------
            elif section == "Ver Reportes":

                table = QTableWidget()
                table.setColumnCount(3)
                table.setHorizontalHeaderLabels(["Usuario","Rol","Comentario"])
                self.section_container.addWidget(table)

                for r in self.system_data["reportes"]:
                    row = table.rowCount()
                    table.insertRow(row)
                    table.setItem(row,0,QTableWidgetItem(r.get("usuario","")))
                    table.setItem(row,1,QTableWidgetItem(r.get("rol","")))
                    table.setItem(row,2,QTableWidgetItem(r.get("comentario","")))


    def regresar_al_login(self):
        if self.login_window:
            self.hide()
            self.login_window.show()
        else:
            QMessageBox.information(self, "Login", "Aquí debería reabrirse tu pantalla de login.")


# --------------------- EJECUCIÓN ---------------------
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    user_test = {"username": "Alice", "role": "Estudiante"}  # Cambia a "Docente" para probar rol docente
    window = DashboardView(user_test)
    window.show()
    sys.exit(app.exec())