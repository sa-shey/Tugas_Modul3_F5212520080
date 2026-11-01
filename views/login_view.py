import tkinter as tk

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Sistem Perpustakaan")
        self.geometry("360x320")
        self.resizable(False, False)

        self.frame = tk.Frame(self)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        tk.Label(self.frame, text="LOGIN SISTEM", font=("Arial", 18, "bold")).pack(pady=(20, 15))

        self.entry_username = tk.Entry(self.frame)
        self.entry_username.pack(pady=10, padx=20, fill="x")
        self.entry_username.insert(0, "Username")

        self.entry_password = tk.Entry(self.frame, show="*")
        self.entry_password.pack(pady=10, padx=20, fill="x")
        self.entry_password.insert(0, "Password")

        self.btn_login = tk.Button(self.frame, text="Masuk", bg="blue", fg="white")
        self.btn_login.pack(pady=20, padx=20, fill="x")