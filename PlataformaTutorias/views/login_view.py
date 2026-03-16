from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QComboBox, QFrame
)

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap, QPainter, QLinearGradient, QColor, QIcon

from services.auth_service import AuthService
from views.dashboard_view import DashboardView
from views.loading_overlay import LoadingOverlay


class LoginView(QWidget):

    def __init__(self):
        super().__init__()

        self.auth_service = AuthService()

        self.setWindowTitle("Plataforma Tutorías")
        self.resize(900, 600)

        # ⭐ ICONO DEL PROGRAMA
        self.setWindowIcon(QIcon("assets/Logo.ico"))

        self.setFont(QFont("Segoe UI", 11))

        # ===== FONDO DE LA UNIVERSIDAD =====
        self.background = QPixmap("assets/Uni.jpg")

        # ===== ESTILOS =====
        self.setStyleSheet("""

        QLabel{
            color:white;
        }

        QLineEdit,QComboBox{
            background-color:#282828;
            border-radius:10px;
            padding:12px;
            color:white;
            font-size:14px;
        }

        QPushButton{
            background-color:#1DB954;
            border-radius:20px;
            padding:14px;
            font-weight:600;
            font-size:14px;
        }

        QPushButton:hover{
            background-color:#1ed760;
        }

        QFrame{
            background-color: rgba(0,0,0,0.85);
            border-radius:20px;
        }

        """)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setFixedWidth(380)

        card_layout = QVBoxLayout()
        card_layout.setSpacing(15)

        # ===== LOGO =====
        logo = QLabel()

        pixmap_logo = QPixmap("assets/Logo.png")

        logo.setPixmap(
            pixmap_logo.scaled(
                130,
                130,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Plataforma de Tutorías")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size:24px;font-weight:600")

        subtitle = QLabel("Iniciar sesión")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color:#b3b3b3")

        self.username = QLineEdit()
        self.username.setPlaceholderText("Usuario")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        self.role = QComboBox()
        self.role.addItems([
            "Administrador",
            "Docente",
            "Estudiante"
        ])

        login_btn = QPushButton("Entrar")
        login_btn.clicked.connect(self.login)

        self.message = QLabel("")
        self.message.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(logo)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(self.username)
        card_layout.addWidget(self.password)
        card_layout.addWidget(self.role)
        card_layout.addSpacing(10)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(self.message)

        card.setLayout(card_layout)

        main_layout.addWidget(card)

        self.setLayout(main_layout)

        self.loading = LoadingOverlay(self, "Ingresando...")

    # ===== PINTAR FONDO DINÁMICO =====
    def paintEvent(self, event):

        painter = QPainter(self)

        if not self.background.isNull():
            scaled = self.background.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)

        # ===== DEGRADADO OSCURO =====
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(0, 0, 0, 120))
        gradient.setColorAt(1, QColor(0, 0, 0, 200))

        painter.fillRect(self.rect(), gradient)

    # ===== LOGIN CORREGIDO PARA CAMBIAR ROL =====
    def login(self):

        user = self.username.text()
        password = self.password.text()
        role = self.role.currentText()

        self.loading.show_loading()

        def process_login():

            result = self.auth_service.login(user, password, role)

            self.loading.hide_loading()

            if result:
                # ✅ PASAR LOGIN COMO REFERENCIA
                self.dashboard = DashboardView(result, login_reference=self)

                # 🔥 OCULTAR LOGIN, NO CERRAR
                self.hide()
                self.dashboard.show()

            else:
                self.message.setText("Credenciales incorrectas")

        QTimer.singleShot(1200, process_login)