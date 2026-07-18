# Student Management System

A production-ready command-line Student Management System built with Python, adhering to clean architecture and industry-standard software engineering principles. This application enables Teachers and Parents to seamlessly view records while allowing authenticated CRUD management over a local CSV data file.

## 🚀 Features

- **Create**: Add new student records with automatic duplicate prevention.
- **Read**: Search for individual students instantly by their unique ID or display all records in a formatted table.
- **Update**: Flexibly update specific student fields (Name, Age, Grade) while preserving untouched fields if left blank.
- **Delete**: Safely delete a student record permanently after a data safety confirmation step.
- **Persistent Storage**: Automatic generation and management of a local `students.csv` file database.

## 🛠️ Professional Engineering Techniques Used

Instead of relying on basic loose scripting, this project implements design choices expected in production-level development teams:

- **Object-Oriented Programming (OOP):** Segregated data structures from application logic using dedicated `Student` and `StudentManager` engine classes.
- **Strict Type Hinting:** Utilized Python's `typing` module (`Dict`, `Optional`) to ensure explicit data pass-through definitions and avoid type errors.
- **Resource Context Managers:** Employed `with open(...)` wrappers to guarantee deterministic file I/O operations and avoid unclosed stream leaks or corruption.
- **In-Memory Cache with Disk Sync:** Modeled after enterprise database ORMs, the engine maps the CSV to an active memory dictionary for fast lookups before writing batch-updated outputs back to disk space.

## 📂 Project Structure

```text
├── student_system.py  # Main application logic and user loop interface
└── students.csv       # Automatically generated text-based dataset