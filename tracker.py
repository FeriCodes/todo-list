import json
import sys
import os
from datetime import datetime


def main_menu(formatted_now):
    print("----------Main Menu----------\n")
    print(f"📅 Current Time: {formatted_now}\n")
    print("1-Add task")
    print("2-Mark task done")
    print("3-View calendar")
    print("4-Remove task")
    print("5-View streaks")
    print("6-show all the tasks")
    print("7-Exit")


def load_file():
    """
    this is for read the "tasks.json" file and if the file dosen't exsist then return an empty list for prevent the an Error.
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
            input(f"\nEnter the number of the task you want to {action_message}: "))

        if task_number <= 0 or task_number > len(tasks_list):
            print("❌ Error: Task number out of range!")
            return None
        return task_number - 1
    
    except ValueError:
        print("❌ Error: please enter a number")


def updated_tasks_by_time(tasks_list):
    """
    Checks the elapsed time and automatically updates task completion statuses and streaks.
    """

    now = datetime.now()

    for item in tasks_list:

        if item["last_updated"] == "":
            continue
        last_time = datetime.strptime(item["last_updated"] , "%Y-%m-%d %H:%M:%S")

        days_passed = (now.date() - last_time.date()).days

        if days_passed == 0:
            continue
        elif days_passed == 1:
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
            "longest_streak": 0
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
        elif asking == "n":
            break
        else:
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


def view_calendar():
    """
    3-Creates a simple calendar view and displays all associated tasks.
    """
    pass


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
            
        print(f"{medal} Task: {item['task']} | Current: {streak_count} days | 🏆 Best Record: {longest} days")
        
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
        status = "✅" if item['done_today'] else "❌"
        print(f"{index + 1}. Task: {item['task']} | Streak: {item['streak']} | status: {status} | Longest Streak: {item['longest_streak']}")

    return True

def main():

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
            view_calendar()
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
