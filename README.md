# Attendify Pro - Smart Attendance Tracker

A desktop application for tracking class attendance with an intuitive interface and comprehensive analytics.

---

## Table of Contents

- [Abstract](#abstract)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage Guide](#usage-guide)
- [System Architecture](#system-architecture)
- [Algorithm](#algorithm)
- [Flowchart](#flowchart)
- [Block Diagram](#block-diagram)
- [Database Schema](#database-schema)
- [Technical Details](#technical-details)
- [Project Structure](#project-structure)
- [Color Scheme](#color-scheme)
- [Screenshots](#screenshots)
- [Contributing](#contributing)

---

## Abstract

Attendify Pro is a self-contained desktop application developed using Python's standard libraries (Tkinter and SQLite). The application addresses the need for efficient attendance tracking among students by providing a secure, offline-first solution for managing class schedules, recording daily attendance, and analyzing attendance patterns. The system employs SHA-256 encryption for password security and stores all data locally, ensuring complete privacy and independence from internet connectivity.

---

## Problem Statement

Students often face challenges in tracking their class attendance effectively:

1. **Lack of Visibility**: Difficulty in monitoring attendance across multiple subjects
2. **Manual Tracking Issues**: Error-prone paper-based or spreadsheet methods
3. **No Real-time Insights**: Unable to identify attendance problems before they become critical
4. **Privacy Concerns**: Unwillingness to use cloud-based solutions with personal academic data
5. **Accessibility**: Need for simple, offline solutions without complex dependencies

---

## Solution

Attendify Pro provides a comprehensive solution through:

- **Centralized Management**: Single application for all attendance tracking needs
- **Automated Calculations**: Real-time percentage calculations and statistics
- **Visual Alerts**: Color-coded indicators for attendance status (Critical, Warning, Good)
- **Local Storage**: Complete data privacy with offline SQLite database
- **User-Friendly Interface**: Intuitive design requiring minimal learning curve
- **Zero Dependencies**: Uses only Python standard libraries for easy deployment

---

## Features

### Authentication System
- Secure user registration and login
- SHA-256 password hashing
- Session management
- Multi-user support with data isolation

### Dashboard
- Daily class schedule display
- One-click attendance marking (Present/Absent)
- Real-time daily statistics
- Quick overview of today's classes

### Timetable Management
- Add classes with complete details (Subject, Day, Time, Professor, Room)
- View organized weekly schedule
- Edit and delete class entries
- Automatic sorting by day and time

### Statistics and Analytics
- Overall attendance percentage calculation
- Subject-wise attendance breakdown
- Visual progress bars with color coding
- Attendance status indicators:
  - Green: 75% and above (Excellent)
  - Orange: 60-74% (Needs Improvement)
  - Red: Below 60% (Critical)

### Data Management
- Local SQLite database storage
- Automatic database creation
- Referential integrity maintenance
- Secure data operations

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 7/8/10/11, macOS 10.12+, Linux (any modern distribution)
- **Python**: Version 3.6 or higher
- **RAM**: 512 MB
- **Storage**: 50 MB free space
- **Display**: 1024x768 resolution minimum

### Recommended Requirements
- **Python**: Version 3.8 or higher
- **RAM**: 1 GB or more
- **Storage**: 100 MB free space
- **Display**: 1920x1080 resolution

---

## Installation

### Step 1: Verify Python Installation

```bash
python --version
```

or

```bash
python3 --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

### Step 2: Clone Repository

```bash
git clone https://github.com/yashjaiswal2818/Attendify.git
cd Attendify
```

### Step 3: Run Application

```bash
python main.py
```

or on macOS/Linux:

```bash
python3 main.py
```

### Alternative Installation: Download ZIP

1. Download ZIP from GitHub repository
2. Extract to desired location
3. Navigate to extracted folder
4. Run `python main.py`

---

## Usage Guide

### Initial Setup

**Step 1: Account Creation**
1. Launch application
2. Click "Sign Up" button
3. Enter unique username
4. Enter password (minimum 4 characters)
5. Click "Sign Up" to create account

**Step 2: Login**
1. Enter username
2. Enter password
3. Click "Login"

### Adding Classes to Timetable

1. Navigate to "Timetable" section from sidebar
2. Click "Add Class" button
3. Fill in required information:
   - Subject Name (required)
   - Day of Week (required)
   - Time Slot (required) - Format: "HH:MM - HH:MM"
4. Optional information:
   - Professor Name
   - Room Number
5. Click "Save Class"

### Marking Daily Attendance

1. Open "Dashboard" section
2. View today's scheduled classes
3. For each class:
   - Click "Present" if attended
   - Click "Absent" if missed
4. Status updates immediately and reflects in statistics

### Viewing Statistics

1. Navigate to "Statistics" section
2. Review overall attendance percentage
3. Check subject-wise breakdown
4. Identify subjects requiring attention based on color indicators

### Managing Timetable

**To Delete a Class:**
1. Go to "Timetable" section
2. Locate the class to delete
3. Click "Delete" button
4. Confirm deletion
5. Associated attendance records will be removed automatically

---

## System Architecture

### Architecture Pattern
The application follows the Model-View-Controller (MVC) architectural pattern:

- **Model**: Database layer (database.py) handles data operations
- **View**: UI components (auth.py, dashboard.py, timetable.py, statistics.py)
- **Controller**: Main application logic (main.py) coordinates between model and view

### Component Interaction

```
┌─────────────────┐
│    main.py      │  (Application Controller)
│   (Entry Point) │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼──────┐ ┌─▼────────┐
│  UI Layer│ │ Database │
│          │ │   Layer  │
│  - auth  │ │          │
│  - dash  │◄┼─────────►│database.py
│  - time  │ │          │
│  - stats │ │          │
└──────────┘ └──────────┘
```

---

## Algorithm

### Main Application Flow

```
START
│
├─ Initialize Application Window
├─ Configure UI Styles
├─ Create Database Connection
│
├─ IF user not authenticated THEN
│  ├─ Display Login/Signup Screen
│  ├─ WAIT for user credentials
│  ├─ Validate credentials
│  │  ├─ IF valid THEN authenticate
│  │  └─ ELSE show error
│  └─ GOTO Main Application
│
├─ Display Main Application
│  ├─ Render Sidebar Navigation
│  └─ Load Dashboard (default view)
│
├─ User Navigation Loop
│  ├─ Listen for navigation events
│  ├─ SWITCH selected page
│  │  ├─ CASE Dashboard: Load today's classes
│  │  ├─ CASE Timetable: Load all classes
│  │  ├─ CASE Statistics: Calculate and display stats
│  │  └─ CASE Logout: Return to login
│  └─ REPEAT until logout
│
└─ END
```

### Attendance Marking Algorithm

```
FUNCTION markAttendance(classId, userId, status, date)
│
├─ BEGIN TRANSACTION
│
├─ CHECK if attendance exists for (classId, date)
│  ├─ IF exists THEN
│  │  └─ UPDATE attendance SET status = newStatus
│  └─ ELSE
│     └─ INSERT new attendance record
│
├─ COMMIT TRANSACTION
│
├─ Refresh dashboard statistics
│
└─ RETURN success
```

### Statistics Calculation Algorithm

```
FUNCTION calculateStatistics(userId)
│
├─ QUERY all attendance records for user
│
├─ Overall Statistics:
│  ├─ totalClasses = COUNT(all records)
│  ├─ presentClasses = COUNT(status = 'Present')
│  ├─ absentClasses = COUNT(status = 'Absent')
│  └─ percentage = (presentClasses / totalClasses) × 100
│
├─ Subject-wise Statistics:
│  ├─ FOR each unique subject DO
│  │  ├─ total = COUNT(records for subject)
│  │  ├─ present = COUNT(Present for subject)
│  │  ├─ absent = COUNT(Absent for subject)
│  │  ├─ percentage = (present / total) × 100
│  │  └─ STORE in results array
│  └─ END FOR
│
└─ RETURN statistics object
```

---

## Flowchart

### Application Startup Flowchart

```
        START
          |
          v
    Initialize App
          |
          v
    Setup Database
          |
          v
    Configure Styles
          |
          v
    Show Login Screen
          |
          v
    Wait for User Input
          |
     ┌────┴────┐
     v         v
  Login    Signup
     |         |
     v         v
  Validate  Create
   Creds    Account
     |         |
     v         v
  Valid? ──No──>Error
     |            |
    Yes           v
     |         Retry?
     |            |
     v           Yes
  Authenticate    |
     |            |
     └────┬───────┘
          v
   Show Main App
          |
     ┌────┴────┐
     v         v
  Dashboard  Menu
     |         |
     v         |
  Display     |
   Today's    |
   Classes <──┘
     |
     v
   Action?
     |
  ┌──┴──┐
  v     v
Mark   Navigate
Attend   |
  |      v
  |   Refresh
  |      |
  └──────┘
     |
     v
   Logout?
     |
    Yes
     |
     v
    END
```

### Attendance Marking Flowchart

```
      START
        |
        v
  Select Class
        |
        v
  Choose Status
   (Present/Absent)
        |
        v
   Get Current Date
        |
        v
  Check Existing Record
        |
    ┌───┴───┐
    v       v
  Exists  New
    |       |
    v       v
 UPDATE  INSERT
  Record  Record
    |       |
    └───┬───┘
        v
  Save to Database
        |
        v
   Update UI
        |
        v
 Recalculate Stats
        |
        v
  Display Success
        |
        v
       END
```

---

## Block Diagram

### System Block Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     ATTENDIFY PRO SYSTEM                     │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              v               v               v
    ┌─────────────────┐ ┌─────────────┐ ┌──────────────┐
    │  Presentation   │ │  Business   │ │     Data     │
    │     Layer       │ │    Logic    │ │    Layer     │
    └─────────────────┘ └─────────────┘ └──────────────┘
              │               │               │
    ┌─────────┴─────────┐    │    ┌──────────┴──────────┐
    │                   │    │    │                     │
    v                   v    v    v                     v
┌────────┐      ┌──────────────────┐           ┌──────────────┐
│  Auth  │      │    Dashboard     │           │   SQLite     │
│  UI    │      │    - Display     │           │   Database   │
└────────┘      │    - Mark        │           │              │
                │      Attendance  │           │  - users     │
┌────────┐      └──────────────────┘           │  - classes   │
│Timetable│                                     │  - attendance│
│  UI    │      ┌──────────────────┐           └──────────────┘
└────────┘      │   Statistics     │
                │    - Calculate   │
┌────────┐      │    - Display     │
│ Stats  │      │    - Analyze     │
│  UI    │      └──────────────────┘
└────────┘
```

### Data Flow Diagram

```
┌──────────┐         ┌───────────────┐         ┌──────────┐
│          │ Login/  │               │  Query/ │          │
│   USER   │─Signup─>│  APPLICATION  │─Update─>│ DATABASE │
│          │         │               │         │          │
└──────────┘         └───────────────┘         └──────────┘
     ^                       │                       │
     │                       │                       │
     │       Display         │        Return         │
     └───────Results─────────┘────────Data───────────┘
```

---

## Database Schema

### Entity Relationship Diagram

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ password_hash   │
│ created_at      │
└────────┬────────┘
         │ 1
         │
         │ N
         │
┌────────▼────────┐         ┌─────────────────┐
│    CLASSES      │         │   ATTENDANCE    │
├─────────────────┤         ├─────────────────┤
│ id (PK)         │ 1     N │ id (PK)         │
│ user_id (FK)    │◄────────│ class_id (FK)   │
│ subject_name    │         │ user_id (FK)    │
│ day_of_week     │         │ date            │
│ time_slot       │         │ status          │
│ professor       │         └─────────────────┘
│ room_number     │
└─────────────────┘
```

### Table Definitions

**USERS Table**

| Column        | Type      | Constraints           | Description                    |
|---------------|-----------|----------------------|--------------------------------|
| id            | INTEGER   | PRIMARY KEY, AUTO    | Unique user identifier         |
| username      | TEXT      | UNIQUE, NOT NULL     | User's login name             |
| password_hash | TEXT      | NOT NULL             | SHA-256 hashed password       |
| created_at    | TIMESTAMP | DEFAULT CURRENT      | Account creation timestamp    |

**CLASSES Table**

| Column       | Type    | Constraints              | Description                  |
|--------------|---------|--------------------------|------------------------------|
| id           | INTEGER | PRIMARY KEY, AUTO        | Unique class identifier      |
| user_id      | INTEGER | FOREIGN KEY, NOT NULL    | Reference to users table     |
| subject_name | TEXT    | NOT NULL                 | Name of the subject          |
| day_of_week  | TEXT    | NOT NULL                 | Day of class (Monday-Sunday) |
| time_slot    | TEXT    | NOT NULL                 | Time period (e.g., 09:00-10:30) |
| professor    | TEXT    | NULL                     | Professor's name             |
| room_number  | TEXT    | NULL                     | Classroom identifier         |

**ATTENDANCE Table**

| Column    | Type    | Constraints                    | Description                      |
|-----------|---------|--------------------------------|----------------------------------|
| id        | INTEGER | PRIMARY KEY, AUTO              | Unique attendance record ID      |
| class_id  | INTEGER | FOREIGN KEY, NOT NULL          | Reference to classes table       |
| user_id   | INTEGER | FOREIGN KEY, NOT NULL          | Reference to users table         |
| date      | DATE    | NOT NULL                       | Date of class                    |
| status    | TEXT    | NOT NULL                       | 'Present' or 'Absent'            |
|           |         | UNIQUE(class_id, date)         | One record per class per day     |

### SQL Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Classes Table
CREATE TABLE classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    subject_name TEXT NOT NULL,
    day_of_week TEXT NOT NULL,
    time_slot TEXT NOT NULL,
    professor TEXT,
    room_number TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Attendance Table
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Present', 'Absent')),
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(class_id, date)
);

-- Indexes for Performance
CREATE INDEX idx_attendance_user ON attendance(user_id);
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_classes_user ON classes(user_id);
```

---

## Technical Details

### Technology Stack

| Component      | Technology        | Purpose                           |
|----------------|-------------------|-----------------------------------|
| Language       | Python 3.6+       | Core application development      |
| GUI Framework  | Tkinter           | User interface rendering          |
| Database       | SQLite3           | Data persistence                  |
| Encryption     | hashlib (SHA-256) | Password security                 |
| Date/Time      | datetime          | Date and time operations          |

### Key Libraries and Modules

**Standard Library Modules Used:**
- `tkinter` - GUI components and styling
- `sqlite3` - Database operations
- `hashlib` - Cryptographic hashing
- `datetime` - Date and time handling

### Security Implementation

**Password Security:**
- SHA-256 hashing algorithm
- No plain text password storage
- Salting not implemented (can be enhanced)

**Data Security:**
- Local database storage
- User data isolation via user_id foreign keys
- SQL injection prevention via parameterized queries

**Session Management:**
- In-memory session storage
- Automatic logout on application close
- No persistent sessions

### Application Performance

**Optimization Techniques:**
- Lazy loading of UI components
- Database connection pooling
- Indexed database queries
- Event-driven architecture

**Memory Management:**
- Proper widget cleanup on navigation
- Database connection closure
- Frame destruction on page changes

---

## Project Structure

```
Attendify/
│
├── main.py                 # Application entry point and main controller
│   ├─ AttendifyPro class  # Main application window
│   ├─ Style configuration # TTK style setup
│   ├─ Navigation logic    # Page switching
│   └─ Authentication flow # Login/logout handling
│
├── database.py            # Database operations layer
│   ├─ Database class      # Database connection manager
│   ├─ Table creation      # Schema initialization
│   ├─ User operations     # Create, authenticate users
│   ├─ Class operations    # CRUD for classes
│   ├─ Attendance ops      # Mark and retrieve attendance
│   └─ Statistics queries  # Aggregate calculations
│
├── auth.py                # Authentication UI component
│   ├─ AuthFrame class     # Login/signup interface
│   ├─ Form validation     # Input validation
│   └─ User feedback       # Error/success messages
│
├── dashboard.py           # Dashboard UI component
│   ├─ DashboardFrame      # Main dashboard container
│   ├─ Daily stats cards   # Statistics display
│   ├─ Class list          # Today's schedule
│   └─ Attendance marking  # Quick mark interface
│
├── timetable.py           # Timetable management UI
│   ├─ TimetableFrame      # Timetable container
│   ├─ Class entry form    # Add class dialog
│   ├─ Class list view     # Organized by day
│   └─ Edit/delete ops     # Class management
│
├── statistics.py          # Statistics and analytics UI
│   ├─ StatisticsFrame     # Statistics container
│   ├─ Overall stats       # Global attendance metrics
│   ├─ Subject breakdown   # Per-subject statistics
│   └─ Visual indicators   # Progress bars and colors
│
├── attendify.db           # SQLite database file (auto-generated)
│
├── README.md              # Project documentation
│
└── .gitignore            # Git ignore rules
```

### File Descriptions

**main.py** (350 lines)
- Main application window initialization
- TTK style configuration for modern UI
- Navigation sidebar implementation
- Page routing and frame management
- User session handling

**database.py** (250 lines)
- SQLite connection management
- Database schema creation
- User authentication methods
- CRUD operations for all tables
- Statistical query methods

**auth.py** (120 lines)
- Login and signup forms
- Input validation and sanitization
- Password hashing integration
- User feedback messaging

**dashboard.py** (180 lines)
- Today's class display logic
- Attendance marking interface
- Daily statistics calculation
- Dynamic UI updates

**timetable.py** (220 lines)
- Class addition dialog
- Weekly schedule view
- Class editing and deletion
- Form validation

**statistics.py** (200 lines)
- Overall attendance calculation
- Subject-wise analytics
- Visual progress bar rendering
- Color-coded status indicators

---

## Color Scheme

### Primary Colors

| Color Name      | Hex Code  | RGB Values      | Usage                          |
|-----------------|-----------|-----------------|--------------------------------|
| Primary Blue    | #3b82f6   | (59, 130, 246)  | Primary buttons, highlights    |
| Primary Hover   | #2563eb   | (37, 99, 235)   | Button hover states            |
| Success Green   | #10b981   | (16, 185, 129)  | Present status, good attendance|
| Warning Orange  | #f59e0b   | (245, 158, 11)  | Warning state (60-74%)         |
| Danger Red      | #ef4444   | (239, 68, 68)   | Absent status, critical (<60%) |

### Background Colors

| Color Name      | Hex Code  | RGB Values      | Usage                          |
|-----------------|-----------|-----------------|--------------------------------|
| Dark Background | #0f172a   | (15, 23, 42)    | Main application background    |
| Card Background | #1e293b   | (30, 41, 59)    | Cards and panels               |
| Hover Background| #334155   | (51, 65, 85)    | Hover states for buttons       |

### Text Colors

| Color Name      | Hex Code  | RGB Values      | Usage                          |
|-----------------|-----------|-----------------|--------------------------------|
| Text Primary    | #f1f5f9   | (241, 245, 249) | Main text, headings            |
| Text Secondary  | #94a3b8   | (148, 163, 184) | Secondary text, descriptions   |

### Attendance Status Colors

| Status Level    | Percentage | Color      | Hex Code  | Meaning                      |
|-----------------|------------|------------|-----------|------------------------------|
| Excellent       | >= 75%     | Green      | #10b981   | Meets attendance requirement |
| Warning         | 60-74%     | Orange     | #f59e0b   | Needs improvement            |
| Critical        | < 60%      | Red        | #ef4444   | Immediate attention required |

---

## Screenshots

### 1. Login Screen
![Login Screen](screenshots/login.png)

**Features Visible:**
- Clean authentication interface
- Username and password fields
- Login and Sign Up buttons
- Application branding

---

### 2. Dashboard View
![Dashboard](screenshots/dashboard.png)

**Features Visible:**
- Today's class schedule
- Daily statistics cards (Total, Attended, Absent)
- Quick attendance marking buttons
- Real-time status updates

---

### 3. Timetable Management
![Timetable](screenshots/timetable.png)

**Features Visible:**
- Weekly class schedule
- Classes organized by day
- Add new class button
- Delete class functionality
- Class details (time, professor, room)

---

### 4. Statistics Page
![Statistics](screenshots/statistics.png)

**Features Visible:**
- Overall attendance percentage
- Subject-wise breakdown
- Color-coded progress bars
- Detailed attendance counts

---

## Contributing

Contributions are welcome. Please follow these guidelines:

### Contribution Process

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/feature-name
   ```
3. Make changes with clear commit messages
4. Test thoroughly
5. Submit pull request with description

### Code Standards

- Follow PEP 8 style guide for Python code
- Include docstrings for all functions and classes
- Maintain modular structure
- Add comments for complex logic
- Update documentation for new features

### Testing Guidelines

- Test all features before committing
- Verify database operations
- Check UI responsiveness
- Test edge cases and error handling

---

## License

This project is licensed under the MIT License.

---

**Attendify Pro** - Professional Attendance Management System

Version 1.0.0 | Last Updated: 2024
# Python-Project
# Attendify
# Attendify
