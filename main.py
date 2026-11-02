"""Demo script: exercises the PawPal+ logic layer from the terminal."""

from pawpal_system import Owner, Pet, Scheduler, Task


def print_tasks(title, tasks):
    """Print a titled, readable list of tasks."""
    print(f"\n{title}")
    print("-" * len(title))
    if not tasks:
        print("  (nothing scheduled)")
    for t in tasks:
        status = "x" if t.completed else " "
        print(f"  [{status}] {t.due_date} {t.time}  {t.pet_name:<6} {t.description} ({t.frequency})")


def main():
    owner = Owner("Alex")
    buddy = Pet("Buddy", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(buddy)
    owner.add_pet(luna)

    # Added out of order on purpose to test sorting.
    buddy.add_task(Task("Evening walk", "18:00", "daily"))
    buddy.add_task(Task("Breakfast", "08:00", "daily"))
    luna.add_task(Task("Give medication", "09:30", "once"))
    luna.add_task(Task("Vet appointment", "09:30", "once"))  # conflicts with medication

    scheduler = Scheduler(owner)

    print_tasks("Today's Schedule", scheduler.get_todays_schedule())

    print("\nConflict check")
    print("--------------")
    for warning in scheduler.detect_conflicts() or ["No conflicts found."]:
        print(f"  {warning}")

    print_tasks("Luna's tasks only", scheduler.filter_tasks(pet_name="Luna"))

    # Complete a daily task: a new one should appear for tomorrow.
    breakfast = scheduler.filter_tasks(pet_name="Buddy")[1]
    next_task = scheduler.mark_task_complete(breakfast)
    print(f"\nCompleted '{breakfast.description}'. Next occurrence: {next_task.due_date}")

    print_tasks("Completed tasks", scheduler.filter_tasks(completed=True))
    print_tasks("All Buddy tasks, sorted", scheduler.sort_by_time(buddy.tasks))


if __name__ == "__main__":
    main()
