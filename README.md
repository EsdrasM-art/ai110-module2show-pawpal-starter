# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Output from running `python main.py`:

```
Today's Schedule
----------------
  [ ] 2026-11-01 08:00  Buddy  Breakfast (daily)
  [ ] 2026-11-01 09:30  Luna   Give medication (once)
  [ ] 2026-11-01 09:30  Luna   Vet appointment (once)
  [ ] 2026-11-01 18:00  Buddy  Evening walk (daily)

Conflict check
--------------
  WARNING: conflict on 2026-11-01 at 09:30: Give medication (Luna), Vet appointment (Luna)

Luna's tasks only
-----------------
  [ ] 2026-11-01 09:30  Luna   Give medication (once)
  [ ] 2026-11-01 09:30  Luna   Vet appointment (once)

Completed 'Breakfast'. Next occurrence: 2026-11-02

Completed tasks
---------------
  [x] 2026-11-01 08:00  Buddy  Breakfast (daily)

All Buddy tasks, sorted
-----------------------
  [x] 2026-11-01 08:00  Buddy  Breakfast (daily)
  [ ] 2026-11-01 18:00  Buddy  Evening walk (daily)
  [ ] 2026-11-02 08:00  Buddy  Breakfast (daily)
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest
```

The 9 tests in `tests/test_pawpal.py` cover marking a task complete, adding a task to a pet, chronological sorting, daily recurrence (a new task for the next day), one-off tasks not recurring, conflict detection (flagged for the same time, not flagged for different times), a pet with no tasks, and filtering by pet and status.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.14.8, pytest-9.1.1, pluggy-1.7.0
rootdir: C:\Users\esdra\Documents\ai110-module2show-pawpal-starter
collected 9 items

tests\test_pawpal.py .........                                           [100%]

============================== 9 passed in 0.07s ==============================
```

**Confidence level:** 4.1 / 5 stars. The core logic and edge cases pass, but conflict detection only checks exact times, and the Streamlit UI is not covered by automated tests.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks by due date, then by "HH:MM" time. Zero-padded time strings sort correctly as text, so a simple `lambda` key works. |
| Filtering | `Scheduler.filter_tasks(pet_name, completed)` | Returns tasks for one pet, by completion status, or both. `get_todays_schedule()` uses it to show only today's pending tasks. |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups pending tasks by date and time and returns warning messages (it never raises an error) when two or more share the exact same slot. Exact matches only, not overlapping durations. |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Completing a daily task adds a copy for the next day (+1 day); weekly adds +7 days, using `timedelta`. One-off tasks do not repeat. |

## 📸 Demo Walkthrough

Start the app with `streamlit run app.py`, then:

1. **Set the owner.** Type a name in the "Owner name" box at the top.
2. **Add pets.** Enter a pet name, pick a species (dog, cat, or other), and click **Add pet**. The pet appears in the "Your pets" list. Adding the same name twice shows a warning instead of a duplicate.
3. **Schedule tasks.** Under "Schedule a task," pick a pet, type a task (for example, "Morning walk"), choose how often it repeats (once, daily, or weekly), set a time and date, and click **Add task**.
4. **See today's schedule.** The "Today's schedule" table lists today's pending tasks across all pets, sorted by time.
5. **Spot conflicts.** If two pending tasks share the same date and time (for example, a walk for one pet and medication for another, both at 08:00), a yellow "Heads up" warning appears above the schedule.
6. **Mark a task complete.** Pick a task under "Mark a task complete" and click **Mark complete**. If the task repeats, the next occurrence is added automatically (tomorrow for daily, next week for weekly) and the success message shows its date.
7. **Browse and filter.** In "All tasks," filter by pet and by status (All, Pending, Completed) to see every task, sorted by date and time.

**Screenshot or video** *(optional)*: not included.
