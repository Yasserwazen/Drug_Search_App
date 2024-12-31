from DrugSearchApp import DrugSearchApp
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font
class LoginWindow:
    def __init__(self, db_manager):
        self.root = tk.Tk()
        self.root.title("Drug Search System - Login")
        self.root.geometry("400x500")
        self.db_manager = db_manager

        # Colors and fonts
        self.colors = {
            'primary': '#1a237e',
            'secondary': '#303f9f',
            'background': '#fafafa',
            'card': '#ffffff',
            'text': '#263238',
            'accent': '#448aff'
        }

        self.fonts = {
            'header': Font(family="Segoe UI", size=24, weight="bold"),
            'normal': Font(family="Segoe UI", size=12),
            'small': Font(family="Segoe UI", size=10)
        }

        self.setup_login_gui()

    def setup_login_gui(self):
        self.root.configure(bg=self.colors['background'])

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], pady=20)
        header_frame.pack(fill="x", pady=(0, 30))

        header_label = tk.Label(
            header_frame,
            text="Drug Search System",
            font=self.fonts['header'],
            bg=self.colors['primary'],
            fg="white"
        )
        header_label.pack()

        # Login form
        login_frame = tk.Frame(main_frame, bg=self.colors['card'], padx=20, pady=20)
        login_frame.pack(fill="x", pady=20)

        # Username
        tk.Label(
            login_frame,
            text="Username:",
            font=self.fonts['normal'],
            bg=self.colors['card']
        ).pack(anchor="w", pady=(0, 5))

        self.username_entry = ttk.Entry(login_frame, font=self.fonts['normal'])
        self.username_entry.pack(fill="x", pady=(0, 15))

        # Password
        tk.Label(
            login_frame,
            text="Password:",
            font=self.fonts['normal'],
            bg=self.colors['card']
        ).pack(anchor="w", pady=(0, 5))

        self.password_entry = ttk.Entry(login_frame, font=self.fonts['normal'], show="*")
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Login button
        ttk.Button(
            login_frame,
            text="Login",
            command=self.login
        ).pack(fill="x", pady=(0, 10))

        # Register button
        ttk.Button(
            login_frame,
            text="Register",
            command=self.show_register
        ).pack(fill="x")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_id = self.db_manager.verify_user(username, password)
        if user_id:
            self.root.destroy()
            app = DrugSearchApp(tk.Tk(), self.db_manager, user_id, username)
            app.root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show_register(self):
        register_window = tk.Toplevel(self.root)
        register_window.title("Register")
        register_window.geometry("300x300")
        register_window.configure(bg=self.colors['background'])

        frame = tk.Frame(register_window, bg=self.colors['card'], padx=20, pady=20)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="Username:",
            font=self.fonts['normal'],
            bg=self.colors['card']
        ).pack(anchor="w", pady=(0, 5))

        username_entry = ttk.Entry(frame, font=self.fonts['normal'])
        username_entry.pack(fill="x", pady=(0, 15))

        tk.Label(
            frame,
            text="Password:",
            font=self.fonts['normal'],
            bg=self.colors['card']
        ).pack(anchor="w", pady=(0, 5))

        password_entry = ttk.Entry(frame, font=self.fonts['normal'], show="*")
        password_entry.pack(fill="x", pady=(0, 15))

        def register():
            username = username_entry.get()
            password = password_entry.get()

            if len(username) < 3 or len(password) < 4:
                messagebox.showerror(
                    "Error",
                    "Username must be at least 3 characters and password at least 4 characters"
                )
                return

            if self.db_manager.add_user(username, password):
                messagebox.showinfo("Success", "Registration successful! You can now login.")
                register_window.destroy()
            else:
                messagebox.showerror("Error", "Username already exists")

        ttk.Button(
            frame,
            text="Register",
            command=register
        ).pack(fill="x", pady=(10, 0))
