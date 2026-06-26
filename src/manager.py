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
            except ValueError:
                print("❌ Invalid input! Please enter a valid number for the streak.")

        elif choice == 3:
            try:
                edit_longest_streak = int(
                    input("enter your longest streak for this task: ")
                )
                selected_task["longest_streak"] = edit_longest_streak
                print("✅ This longest streak updated successfully!")
            except ValueError:
                print(
                    "❌ Invalid input! Please enter a valid number for the longest streak."
                )

        elif choice == 4:
            edit_done_today = (
                input("Have you done this task today? (y/n): ").strip().lower()
            )
            if edit_done_today == "y":
                selected_task["done_today"] = True
                print("✅ Status updated to completed (True).")

            elif edit_done_today == "n":
                selected_task["done_today"] = False
                print("✅ Status updated to not completed (False).")
            else:
                print("❌ Invalid input! Please enter 'y' or 'n'.")

        elif choice == 5:
            confirm = (
                input("Are you sure you want to back to the main menu? (y/n): ")
                .strip()
                .lower()
            )

            if confirm == "y":
                print("Returning to main menu...")
                break
            continue
        else:
            print("❌ Option not found. Please try again.")


def remove_task(tasks_list):
    """
    4-Remove the selected task from the program.
    """
    index = select_task(tasks_list, "remove task")
    if index is None:
        return

    selected_task = tasks_list[index]

    confirm = input(f"Are you sure you want to remove {selected_task['task']}?: (y/n)")
    if confirm == "y":
        tasks_list.pop(index)
        print("✅Task removed successfully!")
    else:
        print("❌Removal canceled.")
