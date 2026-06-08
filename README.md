# Personal Todo List and Habit Tracker

A command-line application to manage daily tasks and build long-term habits using streak tracking. Built with Python using modular architecture and object-oriented design.

## 🎯 Project Purpose

This is a **personal learning project** where I practice:
- Modular code architecture
- Object-Oriented Programming (OOP)
- Separation of concerns
- Clean code principles
- Project organization
- Error handling and validation

## ✨ Features

### ✅ Implemented
- **Add Task:** Create new tasks and habits, saved to JSON
- **Mark Task Done:** Update task status and maintain streaks
- **View Streaks:** Track current and longest streaks for each habit
- **Remove Task:** Delete tasks from your list
- **Edit Tasks:** Modify task names, streaks, and status
- **View All Tasks:** Display all tasks with their status and streak info

### 🚧 In Progress
- Error handling and input validation
- OOP refactoring with classes

### 📋 Planned (Long-term)
- Visual calendar view for tasks
- GUI with tkinter
- Enhanced color-coded status display
- Backup and restore functionality
- Data export (CSV, PDF)

## 📁 Project Structure

```
ToDoList/
├── main.py              # Entry point - runs the application
├── README.md
├── tasks.json           # Task data storage
├── .gitignore
│
├── src/                 # Main package
│   ├── __init__.py
│   ├── database.py      # JSON file operations (load/save tasks)
│   ├── ui.py            # Display menus and task information
│   ├── manager.py       # Core business logic (add, edit, remove tasks)
│   └── models.py        # Data models and structures (TBD)
│
├── archive/             # Previous implementation versions
│   └── tracker.py
│
└── .github/
    └── workflows/       # CI/CD workflows (future)
```

### What Each Module Does

- **`main.py`:** Application entry point, handles main loop and menu routing
- **`database.py`:** Handles all JSON file operations (loading and saving tasks)
- **`ui.py`:** Displays menus, task lists, and streak information
- **`manager.py`:** Contains all task operations (add, edit, remove, mark done, etc.)
- **`models.py`:** Data models and class definitions (planned for OOP refactoring)


## 🛠️ How to Run

```bash
python main.py
```


## 📖 Skills Being Developed

Through this project, I'm learning:
- Python project structure and organization
- Modular design and code organization
- File operations and JSON handling
- Error handling and exception management
- Object-Oriented Programming principles
- GUI development with tkinter (future)
- Clean code and best practices
- Git and version control


**Made with ❤️ while learning Python development**