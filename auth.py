import tkinter as tk
from tkinter import ttk, messagebox


class AuthFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create authentication UI"""
        # Center container
        center_frame = tk.Frame(self, bg="#0f172a")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Card
        card = tk.Frame(center_frame, bg="#1e293b", highlightthickness=0)
        card.pack(padx=40, pady=40)
        
        # Inner padding
        inner = tk.Frame(card, bg="#1e293b")
        inner.pack(padx=50, pady=50)
        
        # Logo/Title
        tk.Label(inner,
                text="📚 Attendify Pro",
                bg="#1e293b",
                fg="#3b82f6",
                font=("Segoe UI", 32, "bold")).pack(pady=(0, 10))
        
        tk.Label(inner,
                text="Smart Attendance Tracking",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 12)).pack(pady=(0, 40))
        
        # Username
        tk.Label(inner,
                text="Username",
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ttk.Entry(inner, style="Modern.TEntry", width=35, font=("Segoe UI", 11))
        self.username_entry.pack(pady=(0, 20))
        
        # Password
        tk.Label(inner,
                text="Password",
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        
        self.password_entry = ttk.Entry(inner, style="Modern.TEntry", show="●", width=35, font=("Segoe UI", 11))
        self.password_entry.pack(pady=(0, 30))
        
        # Buttons
        btn_frame = tk.Frame(inner, bg="#1e293b")
        btn_frame.pack(fill="x")
        
        login_btn = ttk.Button(btn_frame,
                              text="Login",
                              style="Primary.TButton",
                              command=self.login)
        login_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        signup_btn = ttk.Button(btn_frame,
                               text="Sign Up",
                               style="Secondary.TButton",
                               command=self.signup)
        signup_btn.pack(side="right", expand=True, fill="x")
        
        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Focus username
        self.username_entry.focus()
    
    def login(self):
        """Handle login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        success, user_id = self.app.db.authenticate_user(username, password)
        
        if success:
            self.app.login_success(user_id, username)
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)
    
    def signup(self):
        """Handle signup"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "Password must be at least 4 characters")
            return
        
        success, result = self.app.db.create_user(username, password)
        
        if success:
            messagebox.showinfo("Success", "Account created successfully! Please login.")
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", result)