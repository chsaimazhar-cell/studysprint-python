"""Entry point for the StudySprint command-line application."""

from datetime import date
from pathlib import Path

from study_sprint.planner import StudyPlanner

DATA_FILE = Path(__file__).with_name("tasks.json")


def prompt_date() -> date | None:
    """Ask for an optional due date in YYYY-MM-DD format."""
    raw = input("Due date (YYYY-MM-DD, leave blank for none): ").strip()
    if not raw:
        return None
    try:
        return date.fromisoformat(raw)
    except ValueError:
        print("Please enter a valid date, for example 2026-12-31.")
        return prompt_date()


def show_tasks(planner: StudyPlanner) -> None:
    tasks = planner.list_tasks()
    if not tasks:
        print("\nNo tasks yet. Add your first study task!")
        return

    print("\nYOUR STUDY TASKS")
    print("-" * 72)
    for task in tasks:
        status = "✓" if task.completed else " "
        due = task.due_date.isoformat() if task.due_date else "No deadline"
        print(
            f"[{status}] #{task.id} {task.title} "
            f"| Priority: {task.priority.value} | Due: {due}"
        )


def main() -> None:
    planner = StudyPlanner(DATA_FILE)
    print("\n" + "=" * 42)
    print("          STUDYSPRINT 📚")
    print("      Plan small. Learn every day.")
    print("=" * 42)

    while True:
        print(
            "\n1. Add task\n"
            "2. List tasks\n"
            "3. Complete task\n"
            "4. Delete task\n"
            "5. View progress\n"
            "6. Exit"
        )
        choice = input("\nChoose an option (1-6): ").strip()

        try:
            if choice == "1":
                title = input("Task title: ").strip()
                priority = input("Priority (low/medium/high) [medium]: ").strip().lower()
                priority = priority or "medium"
                due_date = prompt_date()
                task = planner.add_task(title, priority=priority, due_date=due_date)
                print(f"Added task #{task.id}: {task.title}")

            elif choice == "2":
                show_tasks(planner)

            elif choice == "3":
                show_tasks(planner)
                task_id = int(input("\nTask ID to complete: "))
                planner.complete_task(task_id)
                print(f"Task #{task_id} marked complete.")

            elif choice == "4":
                show_tasks(planner)
                task_id = int(input("\nTask ID to delete: "))
                planner.delete_task(task_id)
                print(f"Task #{task_id} deleted.")

            elif choice == "5":
                stats = planner.progress()
                print("\nYOUR PROGRESS")
                print(f"Total tasks: {stats['total']}")
                print(f"Completed:   {stats['completed']}")
                print(f"Remaining:   {stats['remaining']}")
                print(f"Completion:  {stats['percentage']:.1f}%")

            elif choice == "6":
                print("Keep learning. See you next time! 👋")
                break

            else:
                print("Please choose a number from 1 to 6.")

        except (ValueError, KeyError) as error:
            print(f"Could not complete that action: {error}")


if __name__ == "__main__":
    main()
