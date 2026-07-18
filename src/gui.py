from tkinter import messagebox, Menu
import customtkinter as ctk
from src.theme import DARK_THEME


class TodoApp:
    def __init__(self, root, manager, db):
        self.root = root
        self.db = db
        self.manager = manager
        self.root.title("Habit Tracker")
        self.root.geometry("550x620")
        self.root.configure(fg_color=DARK_THEME["bg"])
        self.root.resizable(False, False)

        add_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        add_frame.pack(padx=10, pady=(15, 5), fill="x")

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
            width=35,
            height=35,
            fg_color=DARK_THEME["add"],
            hover_color=DARK_THEME["add_hover"],
            text_color=DARK_THEME["text"],
            border_color=DARK_THEME["border"],
            border_width=1,
            command=self.add,
        )
        self.add_btn.pack(side="right")
        self.entry_box.pack(side="right", padx=(0, 5))

        # Bind Enter key to the add function when inside entry box
        self.entry_box.bind("<Return>", lambda event: self.add())

        self.scroll_frame = ctk.CTkScrollableFrame(self.root)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.scroll_frame.configure(fg_color=DARK_THEME["bg"])

        self.message_label = ctk.CTkLabel(
            self.root,
            text="",
            font=(DARK_THEME["font"], 13),
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
            bd=0,
            relief="flat",
        )
        self.selected_task_for_menu = None
        self.refresh_list()

    def refresh_list(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        for items in self.manager.tasks_list:
            card = ctk.CTkFrame(
                self.scroll_frame,
                corner_radius=10,
                fg_color=DARK_THEME["card"],
                border_width=1,
                border_color=DARK_THEME["border"],
            )
            card.pack(fill="x", padx=15, pady=8)
            card.grid_columnconfigure(0, weight=1)

            # --- determine status ---
            done_today = items["done_today"]
            if done_today == "✅ Done":
                status_text = "✅ Done"
                status_color = DARK_THEME["done"]
                is_done = True
            elif done_today == "💔 Streak Broken":
                status_text = "💔 Broken"
                status_color = DARK_THEME["danger"]
                is_done = False
            else:
                status_text = "⏳ Pending"
                status_color = DARK_THEME["accent"]
                is_done = False

            # --- task name + status in same row (column 0) ---
            name_frame = ctk.CTkFrame(card, fg_color="transparent")
            name_frame.grid(row=0, column=0, padx=(15, 5), pady=12, sticky="w")

            label_name = ctk.CTkLabel(
                name_frame,
                text=items["task"],
                font=(DARK_THEME["font"], 15, "bold"),
                text_color=DARK_THEME["text"],
                anchor="w",
            )
            label_name.pack(side="left", padx=(0, 10))

            status_label = ctk.CTkLabel(
                name_frame,
                text=status_text,
                font=(DARK_THEME["font"], 12),
                text_color=status_color,
                anchor="w",
            )
            status_label.pack(side="left")

            # --- streak info (column 1) ---
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.grid(row=0, column=1, padx=5, pady=8)

            streak_label = ctk.CTkLabel(
                info_frame,
                text=f"🔥 {items['streak']}",
                font=(DARK_THEME["font"], 15),
                text_color=DARK_THEME["text"],
            )
            streak_label.pack(anchor="center")

            best_label = ctk.CTkLabel(
                info_frame,
                text=f"⭐ {items['longest_streak']}",
                font=(DARK_THEME["font"], 13),
                text_color=DARK_THEME["gold"],
            )
            best_label.pack(anchor="center")

            # --- done button (column 2) ---
            done_btn = ctk.CTkButton(
                card,
                text="✔️",
                width=35,
                height=35,
                fg_color=DARK_THEME["done"] if not is_done else "#2d3748",
                hover_color=DARK_THEME["success"],
                border_width=1,
                border_color=DARK_THEME["border"],
                state="disabled" if is_done else "normal",
                command=lambda t=items: self.mark_done(t),
            )
            done_btn.grid(row=0, column=2, padx=(5, 15), pady=8)

            # right-click bindings
            for widget in (card, label_name, status_label, name_frame):
                widget.bind(
                    "<Button-3>", lambda e, t=items: self.show_context_menu(e, t)
                )
                widget.bind(
                    "<Button-2>", lambda e, t=items: self.show_context_menu(e, t)
                )

    def show_context_menu(self, event, task):
        self.selected_task_for_menu = task
        self.context_menu.delete(0, "end")
        self.context_menu.add_command(
            label="  ✏  Edit Task",
            foreground=DARK_THEME["edit"],
            command=lambda: self.open_edit_popup(task),
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(
            label="  ✖  Delete Task",
            foreground=DARK_THEME["danger"],
            command=self.confirm_and_remove,
        )
        self.context_menu.post(event.x_root, event.y_root)

    def add(self, event=None):
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
        popup.title("Edit Task")
        popup.geometry("300x330")
        popup.resizable(False, False)
        popup.configure(fg_color=DARK_THEME["bg"])
        popup.grab_set()

        ctk.CTkLabel(popup, text="Task Name").pack(pady=(15, 2))
        name_entry = ctk.CTkEntry(popup, width=220)
        name_entry.insert(0, task["task"])
        name_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Streak").pack(pady=(10, 2))
        streak_entry = ctk.CTkEntry(popup, width=220)
        streak_entry.insert(0, str(task["streak"]))
        streak_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Best Streak").pack(pady=(10, 2))
        best_entry = ctk.CTkEntry(popup, width=220)
        best_entry.insert(0, str(task["longest_streak"]))
        best_entry.pack(pady=5)

        def save():
            result = self.manager.edit_tasks(
                task, name_entry.get(), streak_entry.get(), best_entry.get()
            )
            self.show_message(result["message"])
            if result["success"]:
                self.db.save(self.manager.tasks_list)
                self.refresh_list()
            popup.destroy()

        ctk.CTkButton(
            popup,
            text="Save",
            fg_color=DARK_THEME["add"],
            hover_color=DARK_THEME["add_hover"],
            command=save,
            width=220,
        ).pack(pady=15)

    def confirm_and_remove(self):
        if self.selected_task_for_menu:
            task = self.selected_task_for_menu
            if messagebox.askyesno("Confirm Delete", f"Delete '{task['task']}'?"):
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
