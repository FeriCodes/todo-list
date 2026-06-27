import customtkinter as ctk


class TodoApp:
    def __init__(self, root, manager, db):
        self.root = root
        self.db = db
        self.manager = manager
        self.root.title("Habit Tracker")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
