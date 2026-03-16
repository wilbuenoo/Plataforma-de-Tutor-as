import sys
from PyQt6.QtWidgets import QApplication
from views.login_view import LoginView
from views.splash_screen import SplashScreen


def main():

    app = QApplication(sys.argv)

    login_window = LoginView()

    def open_login():
        login_window.show()

    splash = SplashScreen(open_login)
    splash.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()