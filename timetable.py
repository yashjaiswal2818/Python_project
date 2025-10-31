import tkinter as tk
from tkinter import ttk, messagebox


class TimetableFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#0f172a")
        self.app = app
        self.create_widgets()
    
    def create_widgets(self):
        """Create timetable UI"""
        # Header
        header = tk.Frame(self, bg="#0f172a")
        header.pack(fill="x", padx=40, pady=(30, 20))
        
        tk.Label(header,
                text="📅 Timetable Management",
                bg="#0f172a",
                fg="#f1f5f9",
                font=("Segoe UI", 28, "bold")).pack(side="left")
        
        # Add button
        add_btn = ttk.Button(header,
                            text="➕ Add Class",
                            style="Primary.TButton",
                            command=self.show_add_dialog)
        add_btn.pack(side="right")
        
        # Classes list container
        self.classes_container = tk.Frame(self, bg="#0f172a")
        self.classes_container.pack(fill="both", expand=True, padx=40, pady=(0, 30))
    
    def refresh(self):
        """Refresh timetable display"""
        # Clear existing
        for widget in self.classes_container.winfo_children():
            widget.destroy()
        
        # Get all classes
        classes = self.app.db.get_user_classes(self.app.current_user['id'])
        
        if not classes:
            self.show_no_classes()
        else:
            self.show_classes(classes)
    
    def show_no_classes(self):
        """Show message when no classes"""
        card = tk.Frame(self.classes_container, bg="#1e293b")
        card.pack(fill="both", expand=True)
        
        msg_frame = tk.Frame(card, bg="#1e293b")
        msg_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(msg_frame,
                text="📚",
                bg="#1e293b",
                font=("Segoe UI", 48)).pack()
        
        tk.Label(msg_frame,
                text="No classes added yet!",
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 16, "bold")).pack(pady=(10, 5))
        
        tk.Label(msg_frame,
                text="Click 'Add Class' to build your timetable.",
                bg="#1e293b",
                fg="#94a3b8",
                font=("Segoe UI", 11)).pack()
    
    def show_classes(self, classes):
        """Show all classes in a table"""
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
        
        # Group by day
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_classes = {day: [] for day in days}
        
        for cls in classes:
            day_classes[cls['day_of_week']].append(cls)
        
        # Display by day
        for day in days:
            if day_classes[day]:
                # Day header
                day_header = tk.Frame(scrollable_frame, bg="#0f172a")
                day_header.pack(fill="x", pady=(20, 10))
                
                tk.Label(day_header,
                        text=day,
                        bg="#0f172a",
                        fg="#3b82f6",
                        font=("Segoe UI", 16, "bold")).pack(anchor="w")
                
                # Classes for this day
                for cls in day_classes[day]:
                    self.create_class_row(scrollable_frame, cls)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_class_row(self, parent, class_info):
        """Create a row for each class"""
        card = tk.Frame(parent, bg="#1e293b", highlightthickness=0)
        card.pack(fill="x", pady=(0, 10))
        
        inner = tk.Frame(card, bg="#1e293b")
        inner.pack(fill="x", padx=25, pady=20)
        
        # Left - Class info
        left = tk.Frame(inner, bg="#1e293b")
        left.pack(side="left", fill="both", expand=True)
        
        tk.Label(left,
                text=class_info['subject_name'],
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 14, "bold")).pack(anchor="w")
        
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
        
        # Right - Delete button
        delete_btn = ttk.Button(inner,
                               text="🗑 Delete",
                               style="Danger.TButton",
                               command=lambda: self.delete_class(class_info['id'], class_info['subject_name']))
        delete_btn.pack(side="right")
    
    def show_add_dialog(self):
        """Show dialog to add new class"""
        dialog = tk.Toplevel(self)
        dialog.title("Add New Class")
        dialog.geometry("500x600")
        dialog.configure(bg="#1e293b")
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"500x600+{x}+{y}")
        
        # Content
        content = tk.Frame(dialog, bg="#1e293b")
        content.pack(fill="both", expand=True, padx=40, pady=40)
        
        tk.Label(content,
                text="Add New Class",
                bg="#1e293b",
                fg="#f1f5f9",
                font=("Segoe UI", 20, "bold")).pack(pady=(0, 30))
        
        # Form fields
        fields = []
        
        # Subject Name
        tk.Label(content, text="Subject Name *", bg="#1e293b", fg="#f1f5f9",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        subject_entry = ttk.Entry(content, style="Modern.TEntry", font=("Segoe UI", 11))
        subject_entry.pack(fill="x", pady=(0, 20))
        fields.append(("Subject Name", subject_entry))
        
        # Day of Week
        tk.Label(content, text="Day of Week *", bg="#1e293b", fg="#f1f5f9",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        day_combo = ttk.Combobox(content, style="Modern.TCombobox",
                                values=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                state="readonly", font=("Segoe UI", 11))
        day_combo.pack(fill="x", pady=(0, 20))
        fields.append(("Day", day_combo))
        
        # Time Slot
        tk.Label(content, text="Time Slot *", bg="#1e293b", fg="#f1f5f9",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        time_entry = ttk.Entry(content, style="Modern.TEntry", font=("Segoe UI", 11))
        time_entry.insert(0, "e.g., 09:00 - 10:30")
        time_entry.pack(fill="x", pady=(0, 20))
        fields.append(("Time Slot", time_entry))
        
        # Professor (optional)
        tk.Label(content, text="Professor (Optional)", bg="#1e293b", fg="#f1f5f9",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        prof_entry = ttk.Entry(content, style="Modern.TEntry", font=("Segoe UI", 11))
        prof_entry.pack(fill="x", pady=(0, 20))
        
        # Room Number (optional)
        tk.Label(content, text="Room Number (Optional)", bg="#1e293b", fg="#f1f5f9",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 5))
        room_entry = ttk.Entry(content, style="Modern.TEntry", font=("Segoe UI", 11))
        room_entry.pack(fill="x", pady=(0, 30))
        
        # Buttons
        btn_frame = tk.Frame(content, bg="#1e293b")
        btn_frame.pack(fill="x")
        
        def save_class():
            subject = subject_entry.get().strip()
            day = day_combo.get()
            time = time_entry.get().strip()
            professor = prof_entry.get().strip()
            room = room_entry.get().strip()
            
            if not subject or not day or not time:
                messagebox.showerror("Error", "Please fill in all required fields", parent=dialog)
                return
            
            self.app.db.add_class(
                self.app.current_user['id'],
                subject, day, time, professor, room
            )
            
            messagebox.showinfo("Success", "Class added successfully!", parent=dialog)
            dialog.destroy()
            self.refresh()
        
        save_btn = ttk.Button(btn_frame, text="Save Class", style="Primary.TButton", command=save_class)
        save_btn.pack(side="left", expand=True, fill="x", padx=(0, 10))
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", style="Secondary.TButton", command=dialog.destroy)
        cancel_btn.pack(side="right", expand=True, fill="x")
        
        subject_entry.focus()
    
    def delete_class(self, class_id, subject_name):
        """Delete a class"""
        if messagebox.askyesno("Confirm Delete",
                              f"Are you sure you want to delete '{subject_name}'?\n\n"
                              "This will also delete all attendance records for this class."):
            self.app.db.delete_class(class_id)
            messagebox.showinfo("Success", "Class deleted successfully!")
            self.refresh()