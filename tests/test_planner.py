"""Unit tests for the StudySprint planner."""

import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from study_sprint.models import Priority
from study_sprint.planner import StudyPlanner


class StudyPlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tasks.json"
        self.planner = StudyPlanner(self.data_file)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_task_and_persist_it(self) -> None:
        task = self.planner.add_task(
            "Revise Python loops", "high", date(2026, 12, 1)
        )
        self.assertEqual(task.id, 1)
        self.assertEqual(task.priority, Priority.HIGH)

        reloaded = StudyPlanner(self.data_file)
        self.assertEqual(reloaded.list_tasks()[0].title, "Revise Python loops")
        self.assertEqual(reloaded.list_tasks()[0].due_date, date(2026, 12, 1))

    def test_reject_empty_title(self) -> None:
        with self.assertRaises(ValueError):
            self.planner.add_task("   ")

    def test_reject_invalid_priority(self) -> None:
        with self.assertRaises(ValueError):
            self.planner.add_task("Study", "urgent")

    def test_complete_task_updates_progress(self) -> None:
        self.planner.add_task("Read chapter")
        self.planner.complete_task(1)
        self.assertEqual(
            self.planner.progress(),
            {"total": 1, "completed": 1, "remaining": 0, "percentage": 100.0},
        )

    def test_delete_task(self) -> None:
        self.planner.add_task("Practice functions")
        self.planner.delete_task(1)
        self.assertEqual(self.planner.list_tasks(), [])

    def test_unknown_task_id_raises_error(self) -> None:
        with self.assertRaises(KeyError):
            self.planner.complete_task(99)

    def test_filter_tasks_by_status(self) -> None:
        self.planner.add_task("Task one")
        self.planner.add_task("Task two")
        self.planner.complete_task(1)
        self.assertEqual(len(self.planner.list_tasks(completed=True)), 1)
        self.assertEqual(len(self.planner.list_tasks(completed=False)), 1)

    def test_non_list_storage_file_is_rejected(self) -> None:
        self.data_file.write_text('{"not": "a task list"}', encoding="utf-8")
        with self.assertRaises(ValueError):
            StudyPlanner(self.data_file)

    def test_failed_save_rolls_back_new_task(self) -> None:
        with patch.object(self.planner, "_save", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.planner.add_task("Unsaved task")
        self.assertEqual(self.planner.list_tasks(), [])

    def test_failed_save_rolls_back_completion(self) -> None:
        task = self.planner.add_task("Keep active")
        with patch.object(self.planner, "_save", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.planner.complete_task(task.id)
        self.assertFalse(task.completed)

    def test_failed_save_rolls_back_deletion(self) -> None:
        task = self.planner.add_task("Keep stored")
        with patch.object(self.planner, "_save", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.planner.delete_task(task.id)
        self.assertEqual(self.planner.list_tasks(), [task])


if __name__ == "__main__":
    unittest.main()
