# StudySprint 📚

A beginner-friendly command-line study planner built with Python. Organize study tasks, set priorities and due dates, track completed work, and review your progress — all stored locally in a JSON file.

## Features

- Add, list, complete, edit, and delete study tasks
- Set task priorities (low, medium, high) and optional due dates
- Filter tasks by status
- View a progress summary
- Persist tasks in a local JSON file
- Validate user input and handle missing or malformed data
- Unit tests using Python's built-in `unittest`

## Requirements

- Python 3.10 or newer
- No third-party packages required

## Quick start

```bash
git clone https://github.com/chsaimazhar-cell/studysprint-python.git
cd studysprint-python
python main.py
```

On Windows, use `py main.py` if `python` is not recognized.

## Example workflow

1. Choose **Add task** from the menu.
2. Enter a title, priority, and optional due date (`YYYY-MM-DD`).
3. Choose **List tasks** to review your plan.
4. Mark a task complete when you finish it.
5. Open **Progress** to see your completion rate.

## Run the tests

```bash
python -m unittest discover -s tests -v
```

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

## Data and privacy

Tasks are saved in `tasks.json` in the project directory. This file is created automatically the first time the app saves data. It is excluded from Git so your personal study plan is not accidentally committed.

## Roadmap

- [ ] Add CSV export
- [ ] Add weekly study goals
- [ ] Build a graphical interface

## Author

**Saim.Tec** — Student developer learning Python and software development.

If you find this project useful, consider giving the repository a ⭐.
