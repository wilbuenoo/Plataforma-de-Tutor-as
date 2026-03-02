import tkinter as tk
from views.login_view import LoginView

def main():
    root = tk.Tk()
    root.title("Plataforma de Tutorías")
    root.geometry("900x600")
    root.resizable(False, False)
    root.configure(bg="#0F1115")

    app = LoginView(root)
    app.pack(fill="both", expand=True)

    root.mainloop()

if __name__ == "__main__":
    main()