# Attendify Pro - Smart Attendance Tracker

A desktop application for tracking class attendance with an intuitive interface and comprehensive analytics.

---

## Table of Contents

- [Abstract](#abstract)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [System Architecture](#system-architecture)
- [Database Schema](#database-schema)
- [Technical Stack](#technical-stack)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)

---

## Abstract

Attendify Pro is a self-contained desktop application built with Python's standard libraries (Tkinter and SQLite). It helps students track class attendance efficiently through a secure, offline-first solution. The system uses SHA-256 encryption for passwords and stores all data locally, ensuring complete privacy.

---

## Problem Statement

Students face several challenges in tracking attendance:

- Difficulty monitoring attendance across multiple subjects
- Error-prone manual tracking methods
- No real-time insights into attendance patterns
- Privacy concerns with cloud-based solutions
- Need for simple, offline solutions

---

## Solution

Attendify Pro provides:

- Centralized attendance management
- Automated percentage calculations
- Color-coded visual alerts (Green ≥75%, Orange 60-74%, Red <60%)
- Complete data privacy with local storage
- Zero external dependencies

---

## Features

### Authentication System
- Secure user registration and login
- SHA-256 password hashing
- Multi-user support with data isolation

### Dashboard
- Daily class schedule display
- One-click attendance marking
- Real-time statistics

### Timetable Management
- Add classes with complete details
- Organized weekly schedule view
- Edit and delete functionality

### Statistics and Analytics
- Overall attendance percentage
- Subject-wise breakdown
- Visual progress bars
- Status indicators

---

## Installation

### Prerequisites

- Python 3.6 or higher
- No additional dependencies required

### Steps

```bash
# Clone the repository
git clone https://github.com/yashjaiswal2818/Python_project.git
cd Python_project

# Run the application
python main.py

# On macOS/Linux
python3 main.py
```

---

## Usage Guide

### First Time Setup

1. Launch the application
2. Click "Sign Up"
3. Enter username and password (minimum 4 characters)
4. Login with your credentials

### Adding Classes

1. Navigate to "Timetable" section
2. Click "Add Class"
3. Fill in details:
   - Subject Name (required)
   - Day of Week (required)
   - Time Slot (required)
   - Professor Name (optional)
   - Room Number (optional)
4. Click "Save Class"

### Marking Attendance

1. Open "Dashboard"
2. View today's classes
3. Click "Present" or "Absent" for each class
4. Status updates immediately

### Viewing Statistics

1. Navigate to "Statistics"
2. Check overall attendance percentage
3. Review subject-wise breakdown
4. Monitor color-coded alerts

---

## System Architecture

### Architecture Pattern

Model-View-Controller (MVC):

- **Model**: Database layer (database.py)
- **View**: UI components (auth.py, dashboard.py, timetable.py, statistics.py)
- **Controller**: Application logic (main.py)

### Component Flow

```
User → Main App → UI Components → Database Layer → SQLite
```

---

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| username | TEXT | Unique username |
| password_hash | TEXT | SHA-256 hashed password |
| created_at | TIMESTAMP | Account creation time |

### Classes Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key to users |
| subject_name | TEXT | Subject name |
| day_of_week | TEXT | Day (Monday-Sunday) |
| time_slot | TEXT | Time period |
| professor | TEXT | Professor name (optional) |
| room_number | TEXT | Room number (optional) |

### Attendance Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| class_id | INTEGER | Foreign key to classes |
| user_id | INTEGER | Foreign key to users |
| date | DATE | Attendance date |
| status | TEXT | Present/Absent |

**Constraint**: Unique(class_id, date) - One record per class per day

---

## Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Language | Python 3.6+ | Core development |
| GUI | Tkinter | User interface |
| Database | SQLite3 | Data storage |
| Security | hashlib (SHA-256) | Password encryption |

### Key Features

- Zero external dependencies
- Cross-platform compatibility
- Local-only data storage
- Parameterized SQL queries for security

---

## Project Structure

```
Python_project/
│
├── main.py              # Application entry point
├── database.py          # Database operations
├── auth.py              # Authentication UI
├── dashboard.py         # Dashboard interface
├── timetable.py         # Timetable management
├── statistics.py        # Statistics display
├── attendify.db         # SQLite database (auto-generated)
├── README.md            # Documentation
└── .gitignore          # Git ignore rules
```

### File Descriptions

- **main.py** - Main window, navigation, styling
- **database.py** - Database schema, CRUD operations, queries
- **auth.py** - Login/signup forms, validation
- **dashboard.py** - Daily schedule, attendance marking
- **timetable.py** - Class management interface
- **statistics.py** - Analytics and visualizations

---

## Screenshots

### Login Screen
![Login Screen](screenshots/login.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Timetable Management
![Timetable](screenshots/timetable.png)

### Statistics
![Statistics](screenshots/statistics.png)

---

## Color Scheme

| Element | Color | Hex Code | Usage |
|---------|-------|----------|-------|
| Primary | Blue | #3b82f6 | Buttons, highlights |
| Success | Green | #10b981 | Present, good attendance (≥75%) |
| Warning | Orange | #f59e0b | Needs improvement (60-74%) |
| Danger | Red | #ef4444 | Absent, critical (<60%) |
| Background | Dark | #0f172a | Main background |
| Cards | Dark Blue | #1e293b | Cards and panels |

---

## Algorithm Overview

### Attendance Marking

```
1. User selects class
2. User clicks Present/Absent
3. System checks if record exists for (class, date)
4. If exists: Update status
5. If not exists: Insert new record
6. Refresh statistics
7. Update UI
```

### Statistics Calculation

```
1. Query all attendance records for user
2. Calculate overall percentage:
   - Total classes = COUNT(all records)
   - Present = COUNT(status='Present')
   - Percentage = (Present / Total) × 100
3. Calculate per subject:
   - Group by subject_name
   - Calculate percentage for each
4. Apply color coding based on percentage
5. Display results
```

---

## Security Features

- SHA-256 password hashing
- No plain text password storage
- Local-only data storage
- Parameterized SQL queries (prevents SQL injection)
- User data isolation via foreign keys

---

## System Requirements

### Minimum

- OS: Windows 7+, macOS 10.12+, Linux
- Python: 3.6+
- RAM: 512 MB
- Storage: 50 MB

### Recommended

- Python: 3.8+
- RAM: 1 GB
- Display: 1920x1080

---

## Contributing

Contributions are welcome! 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -m 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Open a Pull Request

---

## Future Enhancements

- Export attendance data to CSV/Excel
- Attendance reports and printing
- Multiple semester support
- Desktop notifications
- Light theme option
- Calendar view

---

## License

MIT License - Free to use and modify for personal and educational purposes.

---

## Author

Shraddha Jaiswal

GitHub: [@yashjaiswal2818](https://github.com/yashjaiswal2818)

---

## Acknowledgments

Built with Python's standard library for maximum portability and ease of use.

---

**Made for students everywhere**

[Back to Top](#attendify-pro---smart-attendance-tracker)
