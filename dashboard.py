import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class DashboardFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create dashboard UI"""
        # Header
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        tk.Label(header,
                text="📊 Dashboard",
                bg="#0f172a",
                fg="#f1f5f9",
                font=("Segoe UI", 28, "bold")).pack(side="left")
        
        # Date
        today = datetime.now().strftime("%A, %B %d, %Y")
        tk.Label(header,
                text=today,
                bg="#0f172a",
                fg="#94a3b8",
                font=("Segoe UI", 12)).pack(side="right")
        
        # Stats cards container
        self.stats_container = tk.Frame(self, bg="#0f172a")
        self.stats_container.pack(fill="x", padx=40, pady=(0, 30))
        
        # Classes container
        self.classes_container = tk.Frame(self, bg="#0f172a")
        self.classes_container.pack(fill="both", expand=True, padx=40, pady=(0, 30))
    
    def refresh(self):
        """Refresh dashboard data"""
        # Clear existing widgets
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        for widget in self.classes_container.winfo_children():
            widget.destroy()
        
        # Get today's data
        today_classes = self.app.db.get_today_classes(self.app.current_user['id'])
        today_date = datetime.now().date().isoformat()
        attendance_records = self.app.db.get_attendance_for_date(self.app.current_user['id'], today_date)
        
        # Convert to dict for easy lookup
        attendance_dict = {record['class_id']: record['status'] for record in attendance_records}
        
        # Calculate stats
        total_today = len(today_classes)
        attended = sum(1 for c in today_classes if attendance_dict.get(c['id']) == 'Present')
        absent = sum(1 for c in today_classes if attendance_dict.get(c['id']) == 'Absent')
        
        # Display stats cards
        stats = [
            ("Total Classes Today", str(total_today), "#3b82f6"),
            ("Attended", str(attended), "#10b981"),
            ("Absent", str(absent), "#ef4444")
        ]
        
        for i, (label, value, color) in enumerate(stats):
            self.create_stat_card(self.stats_container, label, value, color, i)
        
        # Display classes
        if not today_classes:
            self.show_no_classes()
        else:
            self.show_classes(today_classes, attendance_dict, today_date)
    
    def create_stat_card(self, parent, label, value, color, index):
        """Create a statistics card"""
        card = tk.Frame(parent, bg="#1e293b", highlightthickness=0)
        card.grid(row=0, column=index, padx=10, sticky="ew")
        parent.grid_columnconfigure(index, weight=1)
        
        inner = tk.Frame(card, bg="#1e293b")
        inner.pack(padx=30, pady=25)
        
        tk.Label(inner,
                text=value,
                bg="#1e293b",
                fg=color,
                font=("Segoe UI", 36, "bold")).pack()
        
        tk.Label(inner,
                text=label,
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 11)).pack()
    
    def show_no_classes(self):
        """Show message when no classes today"""
        card = tk.Frame(self.classes_container, bg="#1e293b")
        card.pack(fill="both", expand=True, padx=0, pady=0)
        
        msg_frame = tk.Frame(card, bg="#1e293b")
        msg_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(msg_frame,
                text="🎉",
                bg="#1e293b",
                font=("Segoe UI", 48)).pack()
        
        tk.Label(msg_frame,
                text="No classes scheduled for today!",
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 16, "bold")).pack(pady=(10, 5))
        
        tk.Label(msg_frame,
                text="Enjoy your free time or add classes in the Timetable section.",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 11)).pack()
    
    def show_classes(self, classes, attendance_dict, today_date):
        """Show today's classes with attendance marking"""
        # Header
        tk.Label(self.classes_container,
                text="Today's Schedule",
                bg="#0f172a",
                fg="#f1f5f9",
                font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Scrollable frame
        canvas = tk.Canvas(self.classes_container, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.classes_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f172a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Class cards
        for class_info in classes:
            self.create_class_card(scrollable_frame, class_info, attendance_dict, today_date)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_class_card(self, parent, class_info, attendance_dict, today_date):
        """Create a card for each class"""
        status = attendance_dict.get(class_info['id'])
        
        # Card
        card = tk.Frame(parent, bg="#1e293b", highlightthickness=0)
        card.pack(fill="x", pady=(0, 15))
        
        inner = tk.Frame(card, bg="#1e293b")
        inner.pack(fill="x", padx=25, pady=20)
        
        # Left side - Class info
        left = tk.Frame(inner, bg="#1e293b")
        left.pack(side="left", fill="both", expand=True)
        
        # Subject name
        tk.Label(left,
                text=class_info['subject_name'],
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 16, "bold")).pack(anchor="w")
        
        # Details
        details = f"⏰ {class_info['time_slot']}"
        if class_info.get('professor'):
            details += f"  •  👨‍🏫 {class_info['professor']}"
        if class_info.get('room_number'):
            details += f"  •  🚪 {class_info['room_number']}"
        
        tk.Label(left,
                text=details,
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 10)).pack(anchor="w", pady=(5, 0))
        
        # Right side - Attendance buttons
        right = tk.Frame(inner, bg="#1e293b")
        right.pack(side="right", padx=(20, 0))
        
        if status == "Present":
            tk.Label(right,
                    text="✓ Present",
                    bg="#10b981",
                    fg="white",
                    font=("Segoe UI", 11, "bold"),
                    padx=20,
                    pady=10).pack()
        elif status == "Absent":
            tk.Label(right,
                    text="✗ Absent",
                    bg="#ef4444",
                    fg="white",
                    font=("Segoe UI", 11, "bold"),
                    padx=20,
                    pady=10).pack()
        else:
            btn_frame = tk.Frame(right, bg="#1e293b")
            btn_frame.pack()
            
            present_btn = ttk.Button(btn_frame,
                                    text="Present ✓",
                                    style="Success.TButton",
                                    command=lambda: self.mark_attendance(class_info['id'], "Present", today_date))
            present_btn.pack(side="left", padx=(0, 10))
            
            absent_btn = ttk.Button(btn_frame,
                                   text="Absent ✗",
                                   style="Danger.TButton",
                                   command=lambda: self.mark_attendance(class_info['id'], "Absent", today_date))
            absent_btn.pack(side="left")
    
    def mark_attendance(self, class_id, status, date):
        """Mark attendance for a class"""
        success = self.app.db.mark_attendance(class_id, self.app.current_user['id'], status, date)
        if success:
            self.refresh()