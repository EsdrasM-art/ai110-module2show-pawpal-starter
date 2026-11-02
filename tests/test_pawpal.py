from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def make_scheduler():
    owner = Owner("Alex")
    pet = Pet("Buddy")
    owner.add_pet(pet)
    return owner, pet, Scheduler(owner)


def test_mark_complete_changes_status():
    task = Task("Walk", "08:00")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Buddy")
    assert len(pet.tasks) == 0
    pet.add_task(Task("Walk", "08:00"))
    assert len(pet.tasks) == 1


def test_sorting_returns_chronological_order():
    _, pet, scheduler = make_scheduler()
    pet.add_task(Task("Dinner", "18:00"))
    pet.add_task(Task("Breakfast", "08:00"))
    pet.add_task(Task("Lunch", "12:30"))
    times = [t.time for t in scheduler.sort_by_time()]
    assert times == ["08:00", "12:30", "18:00"]


def test_daily_task_creates_next_day_occurrence():
    _, pet, scheduler = make_scheduler()
    task = Task("Breakfast", "08:00", "daily")
    pet.add_task(task)
    new_task = scheduler.mark_task_complete(task)
    assert task.completed is True
    assert new_task is not None
    assert new_task.due_date == date.today() + timedelta(days=1)
    assert new_task.completed is False
    assert len(pet.tasks) == 2


def test_one_off_task_does_not_recur():
    _, pet, scheduler = make_scheduler()
    task = Task("Vet", "10:00", "once")
    pet.add_task(task)
    assert scheduler.mark_task_complete(task) is None
    assert len(pet.tasks) == 1


def test_conflict_detection_flags_same_time():
    owner, pet, scheduler = make_scheduler()
    other = Pet("Luna", "cat")
    owner.add_pet(other)
    pet.add_task(Task("Walk", "09:00"))
    other.add_task(Task("Medication", "09:00"))
    warnings = scheduler.detect_conflicts()
    assert len(warnings) == 1
    assert "09:00" in warnings[0]


def test_no_conflict_when_times_differ():
    _, pet, scheduler = make_scheduler()
    pet.add_task(Task("Walk", "09:00"))
    pet.add_task(Task("Feed", "10:00"))
    assert scheduler.detect_conflicts() == []


def test_pet_with_no_tasks_is_handled():
    _, _, scheduler = make_scheduler()
    assert scheduler.sort_by_time() == []
    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_filter_by_pet_and_status():
    owner, pet, scheduler = make_scheduler()
    other = Pet("Luna", "cat")
    owner.add_pet(other)
    walk = Task("Walk", "08:00")
    pet.add_task(walk)
    other.add_task(Task("Feed", "09:00"))
    walk.mark_complete()
    assert [t.description for t in scheduler.filter_tasks(pet_name="Luna")] == ["Feed"]
    assert [t.description for t in scheduler.filter_tasks(completed=True)] == ["Walk"]
