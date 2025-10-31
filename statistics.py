import tkinter as tk
from tkinter import ttk


class StatisticsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create statistics UI"""
        # Header
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        tk.Label(header,
                text="📈 Attendance Statistics",
                bg="#0f172a",
                fg="#f1f5f9",
                font=("Segoe UI", 28, "bold")).pack(side="left")
        
        # Overall stats container
        self.overall_container = tk.Frame(self, bg="#0f172a")
        self.overall_container.pack(fill="x", padx=40, pady=(0, 30))
        
        # Subject stats container
        self.subject_container = tk.Frame(self, bg="#0f172a")
        self.subject_container.pack(fill="both", expand=True, padx=40, pady=(0, 30))
    
    def refresh(self):
        """Refresh statistics display"""
        # Clear existing
        for widget in self.overall_container.winfo_children():
            widget.destroy()
        for widget in self.subject_container.winfo_children():
            widget.destroy()
        
        # Get statistics
        overall = self.app.db.get_overall_statistics(self.app.current_user['id'])
        subjects = self.app.db.get_subject_statistics(self.app.current_user['id'])
        
        # Display overall stats
        self.show_overall_stats(overall)
        
        # Display subject stats
        if subjects:
            self.show_subject_stats(subjects)
        else:
            self.show_no_data()
    
    def show_overall_stats(self, stats):
        """Display overall statistics in grid format"""
        # Title
        tk.Label(self.overall_container,
                text="Overall Performance",
                bg="#0f172a",
                fg="#f1f5f9",
                font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Grid container
        grid_container = tk.Frame(self.overall_container, bg="#0f172a")
        grid_container.pack(fill="x")
        
        # Get color for percentage
        color = self.get_color_for_percentage(stats['percentage'])
        
        # Overall Percentage Card - Larger, featured
        percentage_card = tk.Frame(grid_container, bg="#1e293b", highlightthickness=0)
        percentage_card.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 15), pady=0)
        
        perc_inner = tk.Frame(percentage_card, bg="#1e293b")
        perc_inner.pack(expand=True, padx=40, pady=40)
        
        tk.Label(perc_inner,
                text=f"{stats['percentage']}%",
                bg="#1e293b",
                fg=color,
                font=("Segoe UI", 56, "bold")).pack()
        
        tk.Label(perc_inner,
                text="Overall Attendance",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 12)).pack(pady=(10, 0))
        
        # Status indicator
        if stats['percentage'] >= 75:
            status_text = "✓ Excellent"
            status_color = "#10b981"
        elif stats['percentage'] >= 60:
            status_text = "⚠ Needs Improvement"
            status_color = "#f59e0b"
        else:
            status_text = "✗ Critical"
            status_color = "#ef4444"
        
        tk.Label(perc_inner,
                text=status_text,
                bg="#1e293b",
                fg=status_color,
                font=("Segoe UI", 11, "bold")).pack(pady=(10, 0))
        
        # Total Classes Card
        total_card = tk.Frame(grid_container, bg="#1e293b", highlightthickness=0)
        total_card.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=(0, 15))
        
        total_inner = tk.Frame(total_card, bg="#1e293b")
        total_inner.pack(expand=True, padx=30, pady=25)
        
        tk.Label(total_inner,
                text=str(stats['total']),
                bg="#1e293b",
                fg="#3b82f6",
                font=("Segoe UI", 42, "bold")).pack()
        
        tk.Label(total_inner,
                text="Total Classes",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 11)).pack(pady=(5, 0))
        
        # Present Classes Card
        present_card = tk.Frame(grid_container, bg="#1e293b", highlightthickness=0)
        present_card.grid(row=0, column=2, sticky="nsew", padx=(15, 0), pady=(0, 15))
        
        present_inner = tk.Frame(present_card, bg="#1e293b")
        present_inner.pack(expand=True, padx=30, pady=25)
        
        tk.Label(present_inner,
                text=str(stats['present']),
                bg="#1e293b",
                fg="#10b981",
                font=("Segoe UI", 42, "bold")).pack()
        
        tk.Label(present_inner,
                text="Present",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 11)).pack(pady=(5, 0))
        
        # Absent Classes Card
        absent_card = tk.Frame(grid_container, bg="#1e293b", highlightthickness=0)
        absent_card.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(0, 0), pady=(0, 0))
        
        absent_inner = tk.Frame(absent_card, bg="#1e293b")
        absent_inner.pack(expand=True, padx=30, pady=25)
        
        tk.Label(absent_inner,
                text=str(stats['absent']),
                bg="#1e293b",
                fg="#ef4444",
                font=("Segoe UI", 42, "bold")).pack()
        
        tk.Label(absent_inner,
                text="Absent",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 11)).pack(pady=(5, 0))
        
        grid_container.grid_columnconfigure(0, weight=2, minsize=300)
        grid_container.grid_columnconfigure(1, weight=1, minsize=200)
        grid_container.grid_columnconfigure(2, weight=1, minsize=200)
        grid_container.grid_rowconfigure(0, weight=1)
        grid_container.grid_rowconfigure(1, weight=1)
    
    def show_subject_stats(self, subjects):

        tk.Label(self.subject_container,
                text="Subject-wise Breakdown",
                bg="#0f172a",
                fg="#f1f5f9",
                font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 20))
        
        canvas = tk.Canvas(self.subject_container, bg="#0f172a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.subject_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f172a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Subject cards
        for subject in subjects:
            self.create_subject_card(scrollable_frame, subject)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_subject_card(self, parent, subject):
        """Create a card for each subject"""
        card = tk.Frame(parent, bg="#1e293b", highlightthickness=0)
        card.pack(fill="x", pady=(0, 15))
        
        inner = tk.Frame(card, bg="#1e293b")
        inner.pack(fill="x", padx=30, pady=25)
        
        top = tk.Frame(inner, bg="#1e293b")
        top.pack(fill="x", pady=(0, 15))
        
        tk.Label(top,
                text=subject['subject'],
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 16, "bold")).pack(side="left")
        
        color = self.get_color_for_percentage(subject['percentage'])
        
        perc_frame = tk.Frame(top, bg=color, padx=15, pady=8)
        perc_frame.pack(side="right")
        
        tk.Label(perc_frame,
                text=f"{subject['percentage']}%",
                bg=color,
                fg="white",
                font=("Segoe UI", 16, "bold")).pack()
        

        stats_frame = tk.Frame(inner, bg="#1e293b")
        stats_frame.pack(fill="x", pady=(0, 15))
        
 
        stat_items = [
            ("Present", subject['present'], "#10b981"),
            ("Absent", subject['absent'], "#ef4444"),
            ("Total", subject['total'], "#3b82f6")
        ]
        
        for label, value, stat_color in stat_items:
            item = tk.Frame(stats_frame, bg="#1e293b")
            item.pack(side="left", padx=(0, 30))
            
            tk.Label(item,
                    text=str(value),
                    bg="#1e293b",
                    fg=stat_color,
                    font=("Segoe UI", 20, "bold")).pack(side="left", padx=(0, 8))
            
            tk.Label(item,
                    text=label,
                    bg="#1e293b",
                    fg="#94a3b8",
                    font=("Segoe UI", 10)).pack(side="left")
        
        # Progress bar
        progress_bg = tk.Frame(inner, bg="#334155", height=10)
        progress_bg.pack(fill="x")
        
        progress_width = subject['percentage']
        progress_bar = tk.Frame(progress_bg, bg=color, height=10)
        progress_bar.place(x=0, y=0, relwidth=progress_width/100, relheight=1)
    
    def show_no_data(self):
        card = tk.Frame(self.subject_container, bg="#1e293b")
        card.pack(fill="both", expand=True)
        
        msg_frame = tk.Frame(card, bg="#1e293b")
        msg_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(msg_frame,
                text="📊",
                bg="#1e293b",
                font=("Segoe UI", 48)).pack()
        
        tk.Label(msg_frame,
                text="No attendance data yet!",
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 16, "bold")).pack(pady=(10, 5))
        
        tk.Label(msg_frame,
                text="Start marking attendance to see statistics.",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 11)).pack()
    
    def get_color_for_percentage(self, percentage):
        if percentage >= 75:
            return "#10b981"  
        elif percentage >= 60:
            return "#f59e0b"  
        else:
            return "#ef4444"  