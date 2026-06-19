from src.ui import main_menu, view_streaks, show_tasks, get_choice, exit_program
from src.database import Database
from src.manager import (
    add_task,
    mark_task_done,
    edit_tasks,
    remove_task,
    updated_tasks_by_time,
)
from datetime import datetime


def main():
    """
    Run the main application loop, handling database initialization and menu routing.
    """
    db = Database("tasks.json")

    current_tasks = db.load()

    # this is origin time in our todolist.
    updated_tasks_by_time(current_tasks)

    while True:

        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")

        main_menu(formatted_now)
        choice = get_choice()

        if choice == 1:
            add_task(current_tasks)
            db.save(current_tasks)
        elif choice == 2:
            mark_task_done(current_tasks)
            db.save(current_tasks)
        elif choice == 3:
            edit_tasks(current_tasks)
            db.save(current_tasks)
        elif choice == 4:
            remove_task(current_tasks)
            db.save(current_tasks)
        elif choice == 5:
            view_streaks(current_tasks)
        elif choice == 6:
            show_tasks(current_tasks)
        elif choice == 7:
            exit_program()
        elif choice is None:
            continue


if __name__ == "__main__":
    main()
