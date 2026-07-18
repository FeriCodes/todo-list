from tkinter import messagebox, Menu
import customtkinter as ctk
from src.theme import DARK_THEME


class TodoApp:
    def __init__(self, root, manager, db):
        self.root = root
        self.db = db
        self.manager = manager
        self.root.title("Habit Tracker")
        self.root.geometry("550x600")
        self.root.configure(fg_color=DARK_THEME["bg"])
        self.root.resizable(False, False)

        add_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        add_frame.pack(padx=10, pady=20, fill="x")

        self.entry_box = ctk.CTkEntry(
            add_frame,
            placeholder_text="Add a new task...",
            border_color=DARK_THEME["border"],
            border_width=1,
            height=35,
            corner_radius=8,
            width=150,
        )
        self.add_btn = ctk.CTkButton(
            add_frame,
            text="➕",
            width=30,
            height=30,
            fg_color=DARK_THEME["add"],
            hover_color=DARK_THEME["add_hover"],
            text_color=DARK_THEME["text"],
            border_color=DARK_THEME["border"],
            border_width=1,
            command=self.add,
        )
        self.add_btn.pack(side="right")
        self.entry_box.pack(side="right", padx=(0, 5))

        # scrolling between the tasks
        self.scroll_frame = ctk.CTkScrollableFrame(self.root)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.scroll_frame.configure(fg_color=DARK_THEME["bg"])

        # handling the messages
        self.message_label = ctk.CTkLabel(
            self.root,
            text="",
            font=(DARK_THEME["font"], 14),
            text_color=DARK_THEME["accent"],
        )
        self.message_label.pack(pady=5)

        self.context_menu = Menu(
            self.root,
            tearoff=0,
            bg=DARK_THEME["menu_bg"],
            fg=DARK_THEME["menu_fg"],
            activebackground=DARK_THEME["menu_active_bg"],
            activeforeground=DARK_THEME["menu_active_fg"],
            font=(DARK_THEME["font"], 11),
            bd=1,
            relief="flat",
        )
        self.selected_task_for_menu = None

        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for items in self.manager.tasks_list:

            # create a frame for every tasks.
            card = ctk.CTkFrame(
                self.scroll_frame,
                corner_radius=10,
                fg_color=DARK_THEME["card"],
                border_width=1,
                border_color=DARK_THEME["border"],
            )
            card.pack(fill="x", padx=20, pady=10)
            card.grid_columnconfigure(0, weight=1)

            text_frame = ctk.CTkFrame(card, fg_color="transparent")
            text_frame.grid(row=0, column=1, padx=10)

            label_name = ctk.CTkLabel(
                card,
                text=items["task"],
                font=(DARK_THEME["font"], 16),
                text_color=DARK_THEME["text"],
                anchor="w",
            )
            label_name.grid(row=0, column=0, padx=20, pady=15, sticky="w")

            # Bind right-click to the card frame
            card.bind(
                "<Button-3>", lambda event, t=items: self.show_context_menu(event, t)
            )
            card.bind(
                "<Button-2>", lambda event, t=items: self.show_context_menu(event, t)
            )

            # Bind right-click to the task name label too
            label_name.bind(
                "<Button-3>", lambda event, t=items: self.show_context_menu(event, t)
            )
            label_name.bind(
                "<Button-2>", lambda event, t=items: self.show_context_menu(event, t)
            )

            streak_label = ctk.CTkLabel(
                text_frame,
                text=f"streak: {items['streak']}",
                font=(DARK_THEME["font"], 15),
            )
            streak_label.pack(anchor="e")

            best_streak_label = ctk.CTkLabel(
                text_frame,
                text=f"Best: {items['longest_streak']}",
                font=(DARK_THEME["font"], 13),
                text_color=DARK_THEME["gold"],
            )
            best_streak_label.pack(anchor="e")

            done_btn = ctk.CTkButton(
                card,
                text="✔️",
                width=30,
                height=30,
                fg_color=DARK_THEME["done"],
                hover_color=DARK_THEME["success"],
                border_width=1,
                border_color=DARK_THEME["border"],
                command=lambda t=items: self.mark_done(t),
            )
            done_btn.grid(row=0, column=4, padx=5)

    def show_context_menu(self, event, task):
        self.selected_task_for_menu = task
        self.context_menu.delete(0, "end")

        self.context_menu.add_command(
            label="  Edit Task",
            foreground=DARK_THEME["edit"],
            command=lambda: self.open_edit_popup(task),
        )
        self.context_menu.add_separator()

        self.context_menu.add_command(
            label="  Delete Task",
            foreground=DARK_THEME["danger"],
            command=self.confirm_and_remove,
        )

        self.context_menu.configure(bd=0)
        self.context_menu.post(event.x_root, event.y_root)

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
        popup.geometry("300x330")
        popup.resizable(False, False)
        popup.configure(fg_color=DARK_THEME["bg"])

        ctk.CTkLabel(popup, text="New Task Name...").pack(pady=(10, 2))
        name_entry = ctk.CTkEntry(popup, width=200)
        name_entry.insert(0, task["task"])  # displaying the current task name
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="New streak Number...").pack(pady=(10, 2))
        streak_entry = ctk.CTkEntry(popup, width=200)
        streak_entry.insert(0, str(task["streak"]))
        streak_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="New Best Streak...").pack(pady=(10, 2))
        best_entry = ctk.CTkEntry(popup, width=200)
        best_entry.insert(0, str(task["longest_streak"]))
        best_entry.pack(pady=5)

        def save():
            new_name = name_entry.get()
            new_streak_number = streak_entry.get()
            new_best_streak = best_entry.get()

            result = self.manager.edit_tasks(
                task, new_name, new_streak_number, new_best_streak
            )
            self.show_message(result["message"])
            if result["success"]:
                self.db.save(self.manager.tasks_list)
                self.refresh_list()
            popup.destroy()

        ctk.CTkButton(popup, text="Save", command=save).pack(pady=10)
        popup.grab_set()  # this is for user can not close the main window

    def confirm_and_remove(self):
        if self.selected_task_for_menu:
            task = self.selected_task_for_menu
            confirm = messagebox.askyesno(
                title="Confirm Delete",
                message=f"Are you sure you want to delete '{task['task']}' ?",
            )
            if confirm:
                self.remove(task)

    def remove(self, task):
        result = self.manager.remove_task(task)

        if result["success"]:
            self.db.save(self.manager.tasks_list)

        self.show_message(result["message"])
        self.refresh_list()

    def show_message(self, text):
        self.message_label.configure(text=text)
        self.root.after(3000, lambda: self.message_label.configure(text=""))
