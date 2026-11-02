"""PawPal+ logic layer: Task, Pet, Owner and Scheduler classes."""

from dataclasses import dataclass, field, replace
from datetime import date, timedelta
from typing import List, Optional


@dataclass
class Task:
    """A single pet care activity (feeding, walk, medication, appointment)."""

    description: str
    time: str  # "HH:MM" in 24-hour format
    frequency: str = "once"  # "once", "daily" or "weekly"
    due_date: date = field(default_factory=date.today)
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return a fresh task for the next daily/weekly occurrence, or None for one-off tasks."""
        if self.frequency == "daily":
            return replace(self, due_date=self.due_date + timedelta(days=1), completed=False)
        if self.frequency == "weekly":
            return replace(self, due_date=self.due_date + timedelta(weeks=1), completed=False)
        return None


@dataclass
class Pet:
    """A pet and the list of care tasks assigned to it."""

    name: str
    species: str = "dog"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet's list."""
        self.tasks.remove(task)


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Find a pet by name (case-insensitive), or return None."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of the owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """The 'brain': retrieves, organizes and manages tasks across an owner's pets."""

    def __init__(self, owner: Owner):
        """Create a scheduler for the given owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks for the owner, in the order they were added."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """Sort tasks chronologically by due date, then by their 'HH:MM' time."""
        if tasks is None:
            tasks = self.get_all_tasks()
        # Zero-padded "HH:MM" strings sort correctly as plain text.
        return sorted(tasks, key=lambda t: (t.due_date, t.time))

    def filter_tasks(
        self, pet_name: Optional[str] = None, completed: Optional[bool] = None
    ) -> List[Task]:
        """Filter tasks by pet name and/or completion status (None means 'any')."""
        tasks = self.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name.lower() == pet_name.lower()]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def get_todays_schedule(self) -> List[Task]:
        """Return today's incomplete tasks sorted by time."""
        today = [
            t for t in self.get_all_tasks()
            if t.due_date == date.today() and not t.completed
        ]
        return self.sort_by_time(today)

    def mark_task_complete(self, task: Task) -> Optional[Task]:
        """Complete a task; if it recurs, add the next occurrence to the same pet and return it."""
        task.mark_complete()
        next_task = task.next_occurrence()
        if next_task is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(next_task)
        return next_task

    def detect_conflicts(self) -> List[str]:
        """Return warning messages for pending tasks scheduled at the exact same date and time."""
        seen = {}
        for task in self.get_all_tasks():
            if task.completed:
                continue
            seen.setdefault((task.due_date, task.time), []).append(task)

        warnings = []
        for (due, time), group in seen.items():
            if len(group) > 1:
                names = ", ".join(f"{t.description} ({t.pet_name})" for t in group)
                warnings.append(f"WARNING: conflict on {due} at {time}: {names}")
        return warnings
