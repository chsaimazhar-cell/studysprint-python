# StudySprint CLI

A beginner-friendly command-line study planner built with Python. Add study tasks, set a priority and optional due date, mark tasks complete, delete tasks, and review your progress. Task data is saved locally in JSON.

## Features in the current command-line menu

1. **Add task** — enter a title, priority, and optional due date.
2. **List tasks** — display every saved task and its status.
3. **Complete task** — mark a task as completed by its ID.
4. **Delete task** — remove a task by its ID.
5. **View progress** — show total, completed, remaining, and completion percentage.
6. **Exit** — close the application.

Priorities are `low`, `medium`, and `high`. Due dates use `YYYY-MM-DD`.

> **Feature accuracy:** The current CLI menu does not include an edit-task option or a status-filter menu. The planner class has an internal `list_tasks(completed=...)` filtering method, but the command-line interface does not currently expose it.

## Requirements

- Python 3.10 or newer.
- No third-party packages are required.

## Run on Windows

Open PowerShell in the project folder:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python main.py
```

If PowerShell blocks activation, use Command Prompt:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python main.py
```

No package installation step is needed because the project uses only the Python standard library.

To leave the virtual environment, run `deactivate`.

## Run on macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python main.py
```

## Run the tests

```bash
python -m unittest discover -s tests -v
```

## Data storage

The application stores tasks in `tasks.json` beside `main.py`. The file is created automatically when a task is saved and is excluded from Git by `.gitignore`. Back it up if you want to preserve your study plan.

## Project structure

```text
studysprint-python/
├── main.py
├── study_sprint/
│   ├── __init__.py
│   ├── models.py
│   └── planner.py
├── tests/
│   ├── __init__.py
│   └── test_planner.py
├── .gitignore
├── LICENSE
└── README.md
```

## Learning concepts

This project demonstrates Python functions, classes, dataclasses, enums, lists, loops, conditions, exceptions, JSON serialization, file handling, and unit testing with `unittest`.

## License

MIT. See [LICENSE](LICENSE).
