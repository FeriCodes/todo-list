import customtkinter as ctk


class TodoApp:
    def __init__(self, root, manager, db):
        self.root = root
        self.db = db
        self.manager = manager
        self.root.title("Habit Tracker")
        self.root.geometry("550x600")
        self.root.resizable(False, False)

        add_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        add_frame.pack(padx=10, pady=20, fill="x")

        self.entry_box = ctk.CTkEntry(
            add_frame,
            placeholder_text="Add a new task...",
            height=35,
            corner_radius=8,
            width=150,
        )
        self.add_btn = ctk.CTkButton(
            add_frame,
            text="+",
            width=30,
            height=30,
            fg_color="#3a3a3a",
            hover_color="#006DEA",
            border_color="white",
            border_width=1,
            command=self.add,
        )
        self.add_btn.pack(side="right")
        self.entry_box.pack(side="right", padx=(0, 5))

        # scrolling between the tasks
        self.scroll_frame = ctk.CTkScrollableFrame(self.root)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.root.configure(fg_color="#1a1a1a")
        self.scroll_frame.configure(fg_color="#1a1a1a")

        # handling the messages
        self.message_label = ctk.CTkLabel(
            self.root, text="", font=("Segoe UI", 14), text_color="#4a7c59"
        )
        self.message_label.pack(pady=5)

        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for items in self.manager.tasks_list:

            # create a frame for every tasks.
            card = ctk.CTkFrame(
                self.scroll_frame,
                corner_radius=10,
                fg_color="#2b2b2b",
                border_width=1,
                border_color="white",
            )
            card.pack(fill="x", padx=20, pady=10)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.pack(side="right", padx=10)

            label_name = ctk.CTkLabel(
                card, text=items["task"], font=("Segoe UI", 16), anchor="w"
            )
            label_name.pack(side="left", padx=20, pady=15)

            streak_label = ctk.CTkLabel(
                text_frame, text=f"streak: {items['streak']}", font=("Segoe UI", 15)
            )
            streak_label.pack(anchor="e")

            best_streak_label = ctk.CTkLabel(
                text_frame,
                text=f"best streak: {items['longest_streak']}",
                font=("segoe UI", 13),
                text_color="#f0c14b",
            )
            best_streak_label.pack(anchor="e")

            done_btn = ctk.CTkButton(
                card,
                text="✓",
                width=30,
                height=30,
                fg_color="#3a3a3a",
                hover_color="#4a7c59",
                border_width=1,
                border_color="white",
                command=lambda t=items: self.mark_done(t),
            )
            done_btn.pack(side="right", padx=5)

            remove_btn = ctk.CTkButton(
                card,
                text="🗑",
                width=30,
                height=30,
                fg_color="#3a3a3a",
                hover_color="#a83232",
                command=lambda t=items: self.remove(t),
            )
            remove_btn.pack(side="right", padx=5)

            edit_btn = ctk.CTkButton(
                card,
                text="Edit",
                width=30,
                height=30,
                fg_color="#3a3a3a",
                hover_color="#b5860d",
                command=lambda t=items: self.open_edit_popup(t),
            )
            edit_btn.pack(side="right", padx=5)

    def add(self):
        task_name = self.entry_box.get()
        result = self.manager.new_task(task_name)

        if result["success"]:
            self.db.save(self.manager.tasks_list)
            self.entry_box.delete(0, "end")

        self.show_message(result["message"])
        self.refresh_list()

    def mark_done(self, task):
        result = self.manager.mark_task_done(task)

        if result["success"]:
            self.db.save(self.manager.tasks_list)

        self.show_message(result["message"])
        self.refresh_list()

    def open_edit_popup(self, task):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Edit Tasks")
        popup.geometry("300x320")
        popup.resizable(False, False)
        popup.grab_set()  # this is for user can not close the main window

        ctk.CTkLabel(popup, text="New Task Name...").pack(pady=(10, 2))
        name_entry = ctk.CTkEntry(popup, width=200)
        name_entry.insert(0, task["task"])  # displaying the current task name
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="New streak Number...").pack(pady=(10, 2))
        streak_entry = ctk.CTkEntry(popup, width=200)
        streak_entry.insert(0, str(task["streak"]))
        streak_entry.pack(pady=5)

        def save():
            new_name = name_entry.get()
            new_streak_number = streak_entry.get()

            result = self.manager.edit_tasks(task, new_name, new_streak_number)
            self.show_message(result["message"])
            if result["success"]:
                self.db.save(self.manager.tasks_list)
                self.refresh_list()
            popup.destroy()

        ctk.CTkButton(popup, text="Save", command=save).pack(pady=10)

    def remove(self, task):
        result = self.manager.remove_task(task)

        if result["success"]:
            self.db.save(self.manager.tasks_list)

        self.show_message(result["message"])
        self.refresh_list()

    def show_message(self, text):
        self.message_label.configure(text=text)
        self.root.after(2000, lambda: self.message_label.configure(text=""))
