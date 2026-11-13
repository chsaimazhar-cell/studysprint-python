"""Study task management and JSON persistence."""

import json
from datetime import date
from pathlib import Path

from .models import Priority, Task


class StudyPlanner:
    """Manage study tasks and save them as JSON."""

    def __init__(self, storage_path: str | Path = "tasks.json") -> None:
        self.storage_path = Path(storage_path)
        self.tasks = self._load()

    def _load(self) -> list[Task]:
        if not self.storage_path.exists():
            return []
        try:
            raw_tasks = json.loads(self.storage_path.read_text(encoding="utf-8"))
            return [Task.from_dict(item) for item in raw_tasks]
        except (json.JSONDecodeError, TypeError, KeyError, ValueError) as error:
            raise ValueError(
                f"Could not read task data from {self.storage_path}: {error}"
            ) from error

    def _save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        payload = [task.to_dict() for task in self.tasks]
        self.storage_path.write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )

    def _find(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task found with ID {task_id}.")

    def add_task(
        self,
        title: str,
        priority: str = "medium",
        due_date: date | None = None,
    ) -> Task:
        """Create, store, and return a task."""
        next_id = max((task.id for task in self.tasks), default=0) + 1
        task = Task(next_id, title, Priority(priority.lower()), due_date)
        self.tasks.append(task)
        self._save()
        return task

    def list_tasks(self, completed: bool | None = None) -> list[Task]:
        """Return tasks, optionally filtered by completion status."""
        if completed is None:
            return list(self.tasks)
        return [task for task in self.tasks if task.completed is completed]

    def complete_task(self, task_id: int) -> Task:
        task = self._find(task_id)
        task.completed = True
        self._save()
        return task

    def delete_task(self, task_id: int) -> None:
        task = self._find(task_id)
        self.tasks.remove(task)
        self._save()

    def progress(self) -> dict[str, int | float]:
        total = len(self.tasks)
        completed = sum(task.completed for task in self.tasks)
        remaining = total - completed
        percentage = (completed / total * 100) if total else 0.0
        return {
            "total": total,
            "completed": completed,
            "remaining": remaining,
            "percentage": percentage,
        }
