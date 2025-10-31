import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from datetime import datetime
from database import Database
from auth import AuthFrame
from dashboard import DashboardFrame
from timetable import TimetableFrame
from statistics import StatisticsFrame


class AttendifyPro(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Attendify Pro - Smart Attendance Tracker")
        self.geometry("1200x750")
        self.configure(bg="#0f172a")

        # Center window on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (750 // 2)
        self.geometry(f"1200x750+{x}+{y}")

        # Initialize database
        self.db = Database()
        self.current_user = None
        # Ensure DB closes cleanly on window exit
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        # Configure styles
        self.setup_styles()

        # Container for frames
        self.container = tk.Frame(self, bg="#0f172a")
        self.container.pack(fill="both", expand=True)

        # Store frames
        self.frames = {}
        self.current_frame = None

        # Show authentication frame initially
        self.show_auth()

    def setup_styles(self):
        """Configure modern ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configure colors
        bg_dark = "#0f172a"
        bg_card = "#1e293b"
        bg_hover = "#334155"
        primary = "#3b82f6"
        primary_hover = "#2563eb"
        success = "#10b981"
        danger = "#ef4444"
        warning = "#f59e0b"
        text_primary = "#f1f5f9"
        text_secondary = "#94a3b8"

        # Button styles
        style.configure("Primary.TButton",
                        background=primary,
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none",
                        padding=(20, 12),
                        font=("Segoe UI", 10, "bold"))
        style.map("Primary.TButton",
                  background=[("active", primary_hover)])

        style.configure("Success.TButton",
                        background=success,
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none",
                        padding=(15, 10),
                        font=("Segoe UI", 9, "bold"))
        style.map("Success.TButton",
                  background=[("active", "#059669")])

        style.configure("Danger.TButton",
                        background=danger,
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none",
                        padding=(15, 10),
                        font=("Segoe UI", 9, "bold"))
        style.map("Danger.TButton",
                  background=[("active", "#dc2626")])

        style.configure("Secondary.TButton",
                        background=bg_card,
                        foreground=text_primary,
                        borderwidth=0,
                        focuscolor="none",
                        padding=(15, 10),
                        font=("Segoe UI", 9))
        style.map("Secondary.TButton",
                  background=[("active", bg_hover)])

        # Entry styles
        style.configure("Modern.TEntry",
                        fieldbackground=bg_card,
                        foreground=text_primary,
                        borderwidth=2,
                        insertcolor=text_primary,
                        padding=12)

        # Combobox styles
        style.configure("Modern.TCombobox",
                        fieldbackground=bg_card,
                        background=bg_card,
                        foreground=text_primary,
                        borderwidth=2,
                        arrowcolor=text_primary,
                        padding=10)

        # Label styles
        style.configure("Title.TLabel",
                        background=bg_dark,
                        foreground=text_primary,
                        font=("Segoe UI", 24, "bold"))

        style.configure("Subtitle.TLabel",
                        background=bg_dark,
                        foreground=text_secondary,
                        font=("Segoe UI", 11))

        style.configure("Card.TLabel",
                        background=bg_card,
                        foreground=text_primary,
                        font=("Segoe UI", 10))

        style.configure("CardTitle.TLabel",
                        background=bg_card,
                        foreground=text_primary,
                        font=("Segoe UI", 14, "bold"))

    def show_auth(self):
        """Show authentication frame"""
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = AuthFrame(self.container, self)
        self.current_frame.pack(fill="both", expand=True)

    def login_success(self, user_id, username):
        """Called after successful login"""
        self.current_user = {"id": user_id, "username": username}
        self.show_main_app()

    def show_main_app(self):
        """Show main application with navigation"""
        if self.current_frame:
            self.current_frame.destroy()

        # Main container
        main_frame = tk.Frame(self.container, bg="#0f172a")
        main_frame.pack(fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(main_frame, bg="#1e293b", width=250)
        sidebar.pack(side="left", fill="y", padx=0, pady=0)
        sidebar.pack_propagate(False)

        # Logo/Title in sidebar
        logo_frame = tk.Frame(sidebar, bg="#1e293b")
        logo_frame.pack(fill="x", pady=30, padx=20)

        tk.Label(logo_frame,
                 text="📚 Attendify Pro",
                 bg="#1e293b",
                 fg="#3b82f6",
                 font=("Segoe UI", 18, "bold")).pack()

        tk.Label(logo_frame,
                 text=f"Welcome, {self.current_user['username']}!",
                 bg="#1e293b",
                 fg="#94a3b8",
                 font=("Segoe UI", 9)).pack(pady=(5, 0))

        # Navigation buttons frame
        nav_frame = tk.Frame(sidebar, bg="#1e293b")
        nav_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.nav_buttons = []

        nav_items = [
            ("📊 Dashboard", "dashboard"),
            ("📅 Timetable", "timetable"),
            ("📈 Statistics", "statistics")
        ]

        for text, page in nav_items:
            btn = tk.Button(nav_frame,
                            text=text,
                            bg="#1e293b",
                            fg="#f1f5f9",
                            activebackground="#334155",
                            activeforeground="#ffffff",
                            font=("Segoe UI", 11),
                            bd=0,
                            cursor="hand2",
                            anchor="w",
                            padx=20,
                            pady=15,
                            relief="flat",
                            command=lambda p=page: self.show_page(p))
            btn.pack(fill="x", pady=5)
            self.nav_buttons.append((btn, page))

        # Spacer to push logout to bottom
        spacer = tk.Frame(sidebar, bg="#1e293b")
        spacer.pack(fill="both", expand=True)

        # Logout button at bottom with fixed background
        logout_btn = tk.Button(sidebar,
                               text="🚪 Logout",
                               bg="#1e293b",
                               fg="#ef4444",
                               activebackground="#334155",
                               activeforeground="#ef4444",
                               font=("Segoe UI", 10, "bold"),
                               bd=0,
                               cursor="hand2",
                               padx=20,
                               pady=15,
                               relief="flat",
                               command=self.logout)
        logout_btn.pack(side="bottom", fill="x", padx=15, pady=20)

        # Content area
        self.content_frame = tk.Frame(main_frame, bg="#0f172a")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.current_frame = main_frame

        # Initialize page frames
        self.frames = {
            "dashboard": DashboardFrame(self.content_frame, self),
            "timetable": TimetableFrame(self.content_frame, self),
            "statistics": StatisticsFrame(self.content_frame, self)
        }

        # Show dashboard by default
        self.show_page("dashboard")

    def show_page(self, page_name):
        """Switch between pages"""
        # Hide all frames
        for frame in self.frames.values():
            frame.pack_forget()

        # Show selected frame
        if page_name in self.frames:
            self.frames[page_name].pack(fill="both", expand=True)
            self.frames[page_name].refresh()

        # Update navigation button styles
        for btn, btn_page in self.nav_buttons:
            if btn_page == page_name:
                btn.config(bg="#3b82f6", fg="#ffffff")
            else:
                btn.config(bg="#1e293b", fg="#f1f5f9")

    def logout(self):
        """Logout and return to auth screen"""
        self.current_user = None
        self.frames = {}
        self.show_auth()

    def on_quit(self):
        try:
            self.db.close()
        finally:
            self.destroy()


if __name__ == "__main__":
    app = AttendifyPro()
    app.mainloop()
