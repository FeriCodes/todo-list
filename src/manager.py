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


def add_task(tasks_list):
    """
    1-Adds tasks to help build streaks and habits. tasks are also saved to a json file.
    """
    while True:
        activity_name = input("\nEnter the task or habit you want to add: ").strip()

        if activity_name.isdigit():
            print("❌ please enter a task instead the numbers.")
            continue

        if not activity_name:
            print("❌ Task name cannot be empty.")
            continue

        existing_names = [item["task"].strip().lower() for item in tasks_list]
        if activity_name.lower() in existing_names:
            print(f"❌ '{activity_name}' already exists in your list!")
            continue

        task_obj = Task(activity_name)
        new_task = task_obj.to_dict()
        tasks_list.append(new_task)

        print(f"✅ '{activity_name}' added successfully!")

        asking = input("\nDo you want to add another task? (y/n): ").lower().strip()

        if asking == "y":
            continue
        if asking == "n":
            break
        else:
            print("❌ Invalid input! Please enter 'y' or 'n'.")
            continue


def mark_task_done(tasks_list):
    """
    2-Marks a task as completed.
    """
    index = select_task(tasks_list, "mark as done")

    if index is None:
        return
    selected_task = tasks_list[index]

    if selected_task["done_today"]:
        print("❌ Already completed today!")
        return
    selected_task = tasks_list[index]
    selected_task["streak"] += 1
    selected_task["done_today"] = True
    selected_task["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # this can count your longest streak!
    if selected_task["streak"] > selected_task["longest_streak"]:
        selected_task["longest_streak"] = selected_task["streak"]
        print(f"🏆 New Personal Record for '{selected_task['task']}'!")

    print(f"🔥 Great job! '{selected_task['task']}' marked as done. Streak updated.")


def edit_tasks(tasks_list):
    """
    3-Provides an interactive sub-menu to edit specific properties of a selected task.
    Allows changing the name, resetting streaks, toggling completion status,
    and automatically saves updates to the JSON database.
    """
    index = select_task(tasks_list, "edit")
    if index is None:
        return
    selected_task = tasks_list[index]
    while True:

        print(f"\n--- Editing Task: \"{selected_task['task']}\" ---")
        print("1. Change task name")
        print("2. Reset current streak (to 0)")
        print("3. Reset longest streak (to 0)")
        print("4. Toggle done_today (True ↔ False)")
        print("5. Back to main menu")
        choice = get_choice()
        if choice == 1:
            edit_task_name = input(
                "enter your new name for edit the choosen task name?: "
            ).strip()
            selected_task["task"] = edit_task_name
            print("✅ Task name updated successfully!")

        elif choice == 2:
            try:
                edit_current_streak = int(input("enter the new streak for this task: "))
                selected_task["streak"] = edit_current_streak
                print("✅ This streak number updated successfully!")
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
