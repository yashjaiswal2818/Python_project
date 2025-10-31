import sqlite3
import hashlib
from datetime import datetime, date


class Database:
    def __init__(self, db_name="attendify.db"):
        self.db_name = db_name
        self.create_tables()

    def close(self):
        """Provided for API symmetry; connections are short-lived per call."""
        try:
            # No persistent connection to close; method exists for callers to use safely
            pass
        except Exception:
            pass

    def get_connection(self):
        """Get database connection configured for concurrency and short transactions."""
        conn = sqlite3.connect(
            self.db_name, timeout=15.0, isolation_level=None)
        conn.row_factory = sqlite3.Row
        # Improve concurrency and durability; apply per-connection PRAGMAs
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA busy_timeout=5000;")
        return conn

    def create_tables(self):
        """Create all necessary tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Classes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                subject_name TEXT NOT NULL,
                day_of_week TEXT NOT NULL,
                time_slot TEXT NOT NULL,
                professor TEXT,
                room_number TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

        # Attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                UNIQUE(class_id, date)
            )
        ''')

        conn.commit()
        conn.close()

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password):
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, user_id
        except sqlite3.IntegrityError:
            return False, "Username already exists"

    def authenticate_user(self, username, password):
        """Authenticate user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        password_hash = self.hash_password(password)
        cursor.execute(
            "SELECT id FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            return True, user['id']
        return False, None

    def add_class(self, user_id, subject_name, day_of_week, time_slot, professor="", room_number=""):
        """Add a new class to timetable"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO classes (user_id, subject_name, day_of_week, time_slot, professor, room_number)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, subject_name, day_of_week, time_slot, professor, room_number)
        )
        conn.commit()
        conn.close()
        return True

    def get_user_classes(self, user_id):
        """Get all classes for a user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT * FROM classes WHERE user_id = ? 
               ORDER BY CASE day_of_week
                   WHEN 'Monday' THEN 1
                   WHEN 'Tuesday' THEN 2
                   WHEN 'Wednesday' THEN 3
                   WHEN 'Thursday' THEN 4
                   WHEN 'Friday' THEN 5
                   WHEN 'Saturday' THEN 6
                   WHEN 'Sunday' THEN 7
               END, time_slot""",
            (user_id,)
        )
        classes = cursor.fetchall()
        conn.close()
        return [dict(row) for row in classes]

    def get_today_classes(self, user_id):
        """Get classes for today"""
        today = datetime.now().strftime("%A")
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM classes WHERE user_id = ? AND day_of_week = ? ORDER BY time_slot",
            (user_id, today)
        )
        classes = cursor.fetchall()
        conn.close()
        return [dict(row) for row in classes]

    def delete_class(self, class_id):
        """Delete a class and its attendance records"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM classes WHERE id = ?", (class_id,))
        conn.commit()
        conn.close()
        return True

    def mark_attendance(self, class_id, user_id, status, date_str=None):
        """Mark attendance for a class"""
        if date_str is None:
            date_str = date.today().isoformat()

        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT OR REPLACE INTO attendance (class_id, user_id, date, status)
                   VALUES (?, ?, ?, ?)""",
                (class_id, user_id, date_str, status)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            return False

    def get_attendance_for_date(self, user_id, date_str=None):
        """Get attendance records for a specific date"""
        if date_str is None:
            date_str = date.today().isoformat()

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT a.*, c.subject_name FROM attendance a
               JOIN classes c ON a.class_id = c.id
               WHERE a.user_id = ? AND a.date = ?""",
            (user_id, date_str)
        )
        records = cursor.fetchall()
        conn.close()
        return [dict(row) for row in records]

    def get_overall_statistics(self, user_id):
        """Get overall attendance statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) as present
               FROM attendance WHERE user_id = ?""",
            (user_id,)
        )
        stats = cursor.fetchone()
        conn.close()

        total = stats['total'] if stats['total'] else 0
        present = stats['present'] if stats['present'] else 0
        percentage = (present / total * 100) if total > 0 else 0

        return {
            'total': total,
            'present': present,
            'absent': total - present,
            'percentage': round(percentage, 2)
        }

    def get_subject_statistics(self, user_id):
        """Get attendance statistics per subject"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """SELECT 
                c.subject_name,
                COUNT(a.id) as total,
                SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present
               FROM classes c
               LEFT JOIN attendance a ON c.id = a.class_id
               WHERE c.user_id = ?
               GROUP BY c.subject_name
               HAVING total > 0
               ORDER BY c.subject_name""",
            (user_id,)
        )
        results = cursor.fetchall()
        conn.close()

        stats = []
        for row in results:
            total = row['total']
            present = row['present'] if row['present'] else 0
            percentage = (present / total * 100) if total > 0 else 0

            stats.append({
                'subject': row['subject_name'],
                'total': total,
                'present': present,
                'absent': total - present,
                'percentage': round(percentage, 2)
            })

        return stats
