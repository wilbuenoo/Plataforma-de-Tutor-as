from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation
from PyQt6.QtGui import QPixmap


class SplashScreen(QWidget):

    def __init__(self, open_login_callback):
        super().__init__()

        self.open_login_callback = open_login_callback

        self.setFixedSize(900, 600)

        # Pantalla verde
        self.setStyleSheet("background-color:#16a34a;")

        # ===== LOGO =====
        self.logo = QLabel(self)

        pixmap = QPixmap("assets/Logo.png")

        self.logo.setPixmap(
            pixmap.scaled(
                260,
                260,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        self.logo.resize(260, 260)
        self.logo.move(320, 170)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== EFECTO FADE =====
        self.opacity = QGraphicsOpacityEffect()
        self.logo.setGraphicsEffect(self.opacity)

        self.fade = QPropertyAnimation(self.opacity, b"opacity")
        self.fade.setDuration(1200)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)

        # ===== EFECTO ZOOM =====
        self.zoom = QPropertyAnimation(self.logo, b"geometry")
        self.zoom.setDuration(1200)

        start_rect = self.logo.geometry().adjusted(60, 60, -60, -60)
        end_rect = self.logo.geometry()

        self.zoom.setStartValue(start_rect)
        self.zoom.setEndValue(end_rect)

        self.fade.start()
        self.zoom.start()

        # ===== ESPERA 3 SEGUNDOS =====
        QTimer.singleShot(3000, self.finish)

    def finish(self):

        self.close()
        self.open_login_callback()