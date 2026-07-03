from src.database import Task
from datetime import datetime


class Manager:
    def __init__(self, tasks_list):
        self.tasks_list = tasks_list

    def updated_tasks_by_time(self):
        """
        Checks the elapsed time and automatically updates task completion statuses and streaks.
        """
        now = datetime.now()

        for item in self.tasks_list:

            if item["last_updated"] == "":
                continue
            last_time = datetime.strptime(item["last_updated"], "%Y-%m-%d %H:%M:%S")

            days_passed = (now.date() - last_time.date()).days

            if days_passed == 0:
                continue
            if days_passed == 1:
                item["done_today"] = False
            elif days_passed >= 2:
                item["done_today"] = False
                item["streak"] = 0

    def validate_task_name(self, name_to_check, current_name=None):
        perfect_name = name_to_check.strip()

        if perfect_name.isdigit():
            return {
                "success": False,
                "status": "Error",
                "message": "Task name cannot be a number",
            }

        if not perfect_name:
            return {
                "success": False,
                "status": "empty",
                "message": "Task name cannot be empty!",
            }

        existing_names = [
            item["task"].strip().lower()
            for item in self.tasks_list
            if current_name is None
            or item["task"].strip().lower() != current_name.strip().lower()
        ]

        if perfect_name.lower() in existing_names:
            return {
                "success": False,
                "status": "duplicate",
                "message": f"The task '{perfect_name}' already exists!",
            }

        return {"success": True, "perfect_name": perfect_name}

    def new_task(self, activity_name):
        """
        Adds a new task after validation.
        """
        validation = self.validate_task_name(activity_name)

        if not validation["success"]:
            return validation
        clean_name = validation["perfect_name"]

        task_obj = Task(clean_name)
        new_task = task_obj.to_dict()
        self.tasks_list.append(new_task)

        return {
            "success": True,
            "status": "success",
            "message": "Task added successfully!",
        }

    def mark_task_done(self, selected_task):
        """
        Marks a task as completed for today and updates its streak.
        """

        if selected_task["done_today"]:
            return {
                "success": False,
                "message": "Already completed today!",
            }

        selected_task["streak"] += 1
        selected_task["done_today"] = True
        selected_task["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = (
            f"Great job! '{selected_task['task']}' marked as done. Streak updated."
        )

        if selected_task["streak"] > selected_task["longest_streak"]:
            selected_task["longest_streak"] = selected_task["streak"]
            message += f" 🏆 New personal record for '{selected_task['task']}'!"

        return {
            "success": True,
            "message": message,
        }

    # fmt: off
    def edit_tasks(self, selected_task, new_name, new_streak=None, new_longest_streak=None, new_done_today=None):
    # fmt: on
        """
        Edits task name, streaks, and status for GUI.
        """
        validation = self.validate_task_name(
            new_name, current_name=selected_task["task"]
        )
        if not validation["success"]:
            return validation

        selected_task["task"] = validation["perfect_name"]

        if new_streak is not None:
            try:
                streak_value = int(new_streak)
                if streak_value < 0:
                    return {"success": False, "message": "Streak cannot be negative!"}
                selected_task["streak"] = streak_value

                if selected_task["streak"] > selected_task["longest_streak"]:
                    selected_task["longest_streak"] = selected_task["streak"]

            except ValueError:
                return {"success": False, "message": "Streak must be a valid number!"}

        if new_longest_streak is not None:
            try:
                longest_value = int(new_longest_streak)
                if longest_value < 0:
                    return {
                        "success": False,
                        "message": "Longest streak cannot be negative!",
                    }
                selected_task["longest_streak"] = longest_value
            except ValueError:
                return {
                    "success": False,
                    "message": "Longest streak must be a valid number!",
                }

        return {"success": True, "message": "Task updated successfully!"}

    def remove_task(self, selected_task):
        """
        Removes a task from the list.
        """
        try:
            self.tasks_list.remove(selected_task)
            return {
                "success": True,
                "message": f"✅ Task '{selected_task['task']}' removed successfully!",
            }
        except ValueError:
            return {"success": False, "message": "❌ Task not found in the list."}
