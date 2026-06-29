import customtkinter as ctk


class TodoApp:
    def __init__(self, root, manager, db):
        self.root = root
        self.db = db
        self.manager = manager
        self.root.title("Habit Tracker")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # scrolling between the tasks
        self.scroll_frame = ctk.CTkScrollableFrame(self.root)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

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
            card.pack(fill="x", padx=20, pady=8)

            label_name = ctk.CTkLabel(
                card, text=items["task"], font=("Segoe UI", 17), anchor="w"
            )
            label_name.pack(side="left", padx=20, pady=15)

            streak_label = ctk.CTkLabel(
                card, text=f"streak: {items['streak']}", font=("Segoe UI", 14)
            )
            streak_label.pack(side="right", padx=10)

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

    def mark_done(self, task):
        result = self.manager.mark_task_done(task)

        if result["success"]:
            self.db.save(self.manager.tasks_list)

        self.refresh_list()

    def remove(self, task):
        result = self.manager.remove_task(task)

        if result["success"]:
            self.db.save(self.manager.tasks_list)

        self.refresh_list()
