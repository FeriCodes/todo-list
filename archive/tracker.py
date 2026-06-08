"""
Task and Habit Tracker Application.

This module provides a command-line interface for managing daily tasks,
tracking completion streaks, and persistence using a JSON database.
"""

import json
import sys
import os
from datetime import datetime


def main_menu(formatted_now):
    """
    Display the main menu options and the current timestamp.
    """
    print("----------Main Menu----------\n")
    print(f"📅 Current Time: {formatted_now}\n")
    print("1-Add task")
    print("2-Mark task done")
    print("3-edit tasks")
    print("4-Remove task")
    print("5-View streaks")
    print("6-show all the tasks")
    print("7-Exit")


def load_file():
    """
    this is for read the "tasks.json" file
    if the file dosen't exsist then return an empty list for prevent the an Error.
    """
    if not os.path.exists("tasks.json"):
        return []

    try:
        with open("tasks.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:

        return []


def write_file(tasks_list):
    """
    this is can write the file when user give the program an input.
    """

    with open("tasks.json", "w", encoding="utf-8") as file:
        json.dump(tasks_list, file, indent=4, ensure_ascii=False)


def get_choice():
    """
    Get and validate the user's menu selection.

    Returns:
        int: The selected option number if valid, None otherwise.
    """
    try:
        user = int(input("\nChoose a number from the menu: "))
        return user
    except ValueError:
        print("❌ Invalid input! Please enter a number.")
        return None


def select_task(tasks_list, action_message):
    """
    selecting one of your task of your list for remove or tap Done.
    """

    if show_tasks(tasks_list) is False:
        return None
    try:
        task_number = int(
            input(f"\nEnter the number of the task you want to {action_message}: ")
        )

        if task_number <= 0 or task_number > len(tasks_list):
            print("❌ Error: Task number out of range!")
            return None
        return task_number - 1
    except ValueError:
        print("❌ Error: please enter a number")
        return None


def updated_tasks_by_time(tasks_list):
    """
    Checks the elapsed time and automatically updates task completion statuses and streaks.
    """

    now = datetime.now()

    for item in tasks_list:

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

    write_file(tasks_list)


def create_task_structure(activity_name):
    """
    Creates and returns the default dictionary structure for a new task.
    """
    return {
        "task": activity_name,
        "streak": 0,
        "done_today": False,
        "last_updated": "",
        "longest_streak": 0,
    }


def add_task(tasks_list):
    """
    1-Adds tasks to help build streaks and habits. tasks are also saved to a json file.
    """
    while True:

        activity_name = input("\nEnter the task or habit you want to add: ")

        if activity_name.isdigit():
            print("❌ please enter a task instead the numbers.")
            continue

        if not activity_name:
            print("❌ Task name cannot be empty.")
            continue

        new_task = create_task_structure(activity_name)
        tasks_list.append(new_task)

        # write down on the file by the users input
        write_file(tasks_list)
        print(f"✅ '{activity_name}' added successfully!")

        asking = input("\nDo you want to add another task? (y/n): ").lower().strip()

        if asking == "y":
            continue
        if asking == "n":
            break
        print("❌ Invalid input! Please enter 'y' or 'n'.")
        break


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
    write_file(tasks_list)


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
            edit_current_streak = int(input("enter the new streak for this task: "))
            selected_task["streak"] = edit_current_streak
            print("✅ This streak number updated successfully!")

        elif choice == 3:
            edit_longest_streak = int(
                input("enter your longest streak for this task: ")
            )
            selected_task["longest_streak"] = edit_longest_streak
            print("✅ This longest streak updated successfully!")

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
        write_file(tasks_list)


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
        write_file(tasks_list)
        print("✅Task removed successfully!")
    else:
        print("❌Removal canceled.")


def view_streaks(tasks_list):
    """
    5-Displays all tracked streaks for the user's tasks.
    """
    if not tasks_list:
        print("❌ No tasks found. Add some tasks first.")
        return

    print("\n🔥 --- Your Coding & Habit Streaks --- 🔥\n")

    for item in tasks_list:
        streak_count = item["streak"]
        longest = item["longest_streak"]

        if streak_count == 0:
            medal = "⚪"
        elif streak_count < 5:
            medal = "🌱"
        elif streak_count < 15:
            medal = "🔥"
        else:
            medal = "👑"

        task_summary = (
            f"{medal} Task: {item['task']} | "
            f"Current: {streak_count} days | "
            f"🏆 Best Record: {longest} days"
        )
        print(task_summary)

    print("\nKeep pushing forward! Consistency is the key to mastery. 🚀")


def show_tasks(tasks_list):
    """
    6-Displays all the tasks which you add to the "tasks.json" file.
    """
    if not tasks_list:
        print("no tasks found. add some tasks.")
        return False

    # this is for choose the every task you want.
    print("\n--- Your Tasks---")
    for index, item in enumerate(tasks_list):
        status = "✅" if item["done_today"] else "❌"
        print(
            f"{index + 1}. Task: {item['task']} | "
            f"Streak: {item['streak']} | "
            f"status: {status} | "
            f"Longest Streak: {item['longest_streak']}"
        )

    return True


def main():
    """
    Run the main application loop, handling database initialization and menu routing.
    """

    current_tasks = load_file()
    # this is origin time in our todolist.
    updated_tasks_by_time(current_tasks)

    while True:

        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        main_menu(formatted_now)
        choice = get_choice()

        if choice == 1:
            add_task(current_tasks)
        elif choice == 2:
            mark_task_done(current_tasks)
        elif choice == 3:
            edit_tasks(current_tasks)
        elif choice == 4:
            remove_task(current_tasks)
        elif choice == 5:
            view_streaks(current_tasks)
        elif choice == 6:
            show_tasks(current_tasks)
        elif choice == 7:
            print("\ngoodbye!")
            return sys.exit()
        elif choice is None:
            continue
        else:
            print("Option not found. Please try again.")


if __name__ == "__main__":
    main()
