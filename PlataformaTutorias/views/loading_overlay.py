from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class LoadingOverlay(QWidget):

    def __init__(self, parent=None, message="Cargando..."):
        super().__init__(parent)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
        QWidget{
            background-color: rgba(0,0,0,170);
        }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel(message)
        self.label.setFont(QFont("Segoe UI", 14))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setStyleSheet("""
        QLabel{
            background-color:#181818;
            padding:20px 40px;
            border-radius:15px;
            color:white;
        }
        """)

        layout.addWidget(self.label)

        self.setLayout(layout)

        self.hide()

    def show_loading(self):

        if self.parent():
            self.setGeometry(self.parent().rect())

        self.show()

    def hide_loading(self):
        self.hide()
