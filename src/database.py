"""
This module is responsible for handling data storage in the "tasks.json" file.
It contains two main classes: Task and Database.

"""

import json
import os


class Task:
    """
    Represents the structure and blueprint of a task/habit.

    Attributes:
        task (str): The name of the task or habit.
        streak (int): The number of consecutive days the task has been completed.
        done_today (bool): Indicates whether the task has been completed today.
        last_updated (str): The last date when the task was updated.
        longest_streak (int): The longest streak achieved for this task.
    """

    def __init__(self, activity_name):
        self.task = activity_name
        self.streak = 0
        self.done_today = "⏳ Pending"
        self.last_updated = ""
        self.longest_streak = 0

    def to_dict(self):
        return {
            "task": self.task,
            "streak": self.streak,
            "done_today": self.done_today,
            "last_updated": self.last_updated,
            "longest_streak": self.longest_streak,
        }


class Database:
    """
    Handles data persistence by saving and loading tasks from a JSON file. file.
    """

    def __init__(self, filename):
        self.filename = filename

    def load(self):
        """
        Reads the JSON file and returns the list of tasks.

        If the file doesn't exist or is corrupted, it returns an empty list
        to prevent runtime errors.
        """
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:

            return []

    def save(self, tasks_list):
        """
        Writes the current list of tasks to the JSON file.
        """

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(tasks_list, file, indent=4, ensure_ascii=False)
