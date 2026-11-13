"""Data models used by StudySprint."""

from dataclasses import dataclass
from datetime import date
from enum import Enum


class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """A single study task."""

    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    due_date: date | None = None
    completed: bool = False

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        if self.id < 1:
            raise ValueError("Task ID must be a positive integer.")
        if not self.title:
            raise ValueError("Task title cannot be empty.")
        if not isinstance(self.priority, Priority):
            try:
                self.priority = Priority(str(self.priority).lower())
            except ValueError as error:
                raise ValueError("Priority must be low, medium, or high.") from error

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        raw_due_date = data.get("due_date")
        return cls(
            id=int(data["id"]),
            title=str(data["title"]),
            priority=Priority(data.get("priority", "medium")),
            due_date=date.fromisoformat(raw_due_date) if raw_due_date else None,
            completed=bool(data.get("completed", False)),
        )
