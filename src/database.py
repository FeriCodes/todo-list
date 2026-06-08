import json
import os


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
