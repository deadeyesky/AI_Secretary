from datetime import datetime
from typing import Any

from taskwarrior import TaskWarrior, TaskInputDTO

tw = TaskWarrior()


def get_tasks(
    start_date: datetime,
    end_date: datetime,
) -> list[Any]:
    start = start_date.strftime("%Y-%m-%d")
    end = end_date.strftime("%Y-%m-%d")

    return tw.get_tasks(
        f"due.after:{start} due.before:{end}"
    )


def add_task(task: dict[str, Any]) -> Any:
    return tw.add_task(
        TaskInputDTO(
            description=task["summary"],
            due=task["due"].strftime("%Y-%m-%dT%H:%M:%S"),
        )
    )


def complete_task(task_id: str) -> bool:
    try:
        tw.done_task(task_id)
        return True
    except Exception:
        return False


def get_completed_tasks() -> list[Any]:
    return tw.get_tasks("status:completed")
