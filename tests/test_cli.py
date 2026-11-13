"""Integration tests for the StudySprint command-line interface."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "tasks.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cli(self, answers):
        output = io.StringIO()
        with patch.object(main, "DATA_FILE", self.data_file):
            with patch("builtins.input", side_effect=answers):
                with redirect_stdout(output):
                    main.main()
        return output.getvalue()

    def test_add_list_complete_progress_delete_and_exit(self):
        output = self.run_cli([
            "1", "Revise loops", "high", "",
            "2",
            "3", "1",
            "5",
            "4", "1",
            "6",
        ])
        self.assertIn("Added task #1", output)
        self.assertIn("Revise loops", output)
        self.assertIn("Task #1 marked complete.", output)
        self.assertIn("Completion:  100.0%", output)
        self.assertIn("Task #1 deleted.", output)
        self.assertTrue(self.data_file.exists())

    def test_invalid_menu_choice_is_reported(self):
        output = self.run_cli(["9", "6"])
        self.assertIn("Please choose a number from 1 to 6.", output)

    def test_invalid_due_date_can_be_corrected(self):
        output = self.run_cli(["1", "Study dates", "medium", "not-a-date", "2026-12-01", "6"])
        self.assertIn("Please enter a valid date", output)
        self.assertIn("Added task #1", output)


if __name__ == "__main__":
    unittest.main()
