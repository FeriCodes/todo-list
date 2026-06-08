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
