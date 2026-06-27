import customtkinter as ctk
from src.database import Database
from src.manager import Manager
from src.gui import TodoApp


def main():
    db = Database("tasks.json")
    tasks = db.load()
    manager = Manager(tasks)
    manager.updated_tasks_by_time()

    root = ctk.CTk()
    app = TodoApp(root, manager, db)
    root.mainloop()


if __name__ == "__main__":
    main()
