import json
import os
import uuid

TASKS_FILE = "app/data/tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(task_type, trigger_time, message):
    tasks = load_tasks()
    task = {
        "id": str(uuid.uuid4()),
        "type": task_type,
        "trigger_time": trigger_time,
        "message": message,
        "active": True
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def deactivate_all(task_type=None):
    tasks = load_tasks()
    for t in tasks:
        if task_type is None or t["type"] == task_type:
            t["active"] = False
    save_tasks(tasks)

