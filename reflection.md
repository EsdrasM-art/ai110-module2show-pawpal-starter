# PawPal+ Project Reflection

## 1. System Design

**Three core actions**

1. Add a pet to the owner's profile.
2. Schedule a task (feeding, walk, medication, or appointment) for a pet.
3. See today's schedule, sorted by time, with warnings for conflicts.

**a. Initial design**

I chose four classes, each with one clear job:

- **Task** (dataclass): one care activity. It holds a description, a time in "HH:MM" format, a frequency (once, daily, or weekly), a due date, a completed flag, and the name of the pet it belongs to. It can mark itself complete and create the next occurrence of a recurring task.
- **Pet** (dataclass): holds a pet's name, species, and its list of tasks. It can add or remove a task.
- **Owner**: holds the owner's name and their pets. It can add a pet, find a pet by name, and return every task across all pets.
- **Scheduler**: the "brain." It works through the Owner to get tasks, then sorts them, filters them by pet or status, creates recurring tasks, and detects conflicts.

The relationships are simple: an Owner has many Pets, a Pet has many Tasks, and the Scheduler manages an Owner. The Scheduler does not keep its own copy of the tasks. It always asks the Owner, so there is one source of truth and the data cannot get out of sync.

**b. Design changes**

I asked my AI coding assistant to review my class skeleton. It did not flag any missing relationships or problems, so I did not make any changes to the four classes. The AI did suggest adding a Color class, but I left it out (see 3b).

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers the task's date and time, how often it repeats (once, daily, or weekly), and whether it is already done. I focused on time and recurrence because time is important: I need to know exactly when each task happens for each pet. Recurrence matters because it sets how often a task comes back, like daily feeding or weekly medication. Those will always be important factors in pet care, so they mattered most to me.

**b. Tradeoffs**

My scheduler only detects conflicts when two tasks have the exact same date and time. It does not check for overlapping durations (for example, a 30-minute walk at 09:00 and a vet appointment at 09:15). I chose this because tasks in my system only have a start time, not a length, and exact matching keeps the code short, readable, and easy to test. The downside is that it can miss real overlaps, so a future version could add a duration to each task and check whether the time ranges intersect.

---

## 3. AI Collaboration

**a. How you used AI**

The AI chat was the most useful feature because it could actively change my files and run my tests, not just suggest code for me to copy. The most helpful requests were asking it to fix errors. If I messed up part of my code, it found the problem and fixed it, which saved me time and effort. At one point part of my code was not working, so I let the AI run some debugging, and it found the problem. I accepted that fix because I could verify it by rerunning the tests.

I did not use separate chat sessions for different phases, because the phases felt closely related and roughly equal in size, so I kept the work in one place.

**b. Judgment and verification**

The AI suggested adding a Color class, and I chose not to add it. Color isn't necessary for this app, and it just isn't a good or needed class. I kept the design to the four classes the app actually needs. For the code I did accept, I verified it by running the test suite and the demo script (`main.py`) to make sure the output matched what I expected.

---

## 4. Testing and Verification

**a. What you tested**

I wrote 9 automated tests with pytest. They cover marking a task complete, adding a task to a pet, sorting tasks in chronological order, a daily task creating a new task for the next day, a one-off task not repeating, conflict detection (flagged when two tasks share a time, not flagged when times differ), a pet with no tasks, and filtering by pet and by status. These tests matter because they check the scheduler's core promises: tasks show up in the right order, recurring tasks come back, and conflicts are caught instead of silently missed.

**b. Confidence**

I would rate my confidence at 4.1 out of 5. The core logic and edge cases pass, but conflict detection only checks exact times, and the Streamlit UI is not covered by automated tests. With more time I would play with the app more and expand it, for example by testing overlapping tasks with different start times once tasks have durations.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the overall structure. Each class has one clear job, and the result looks neat and pleasing to me.

**b. What you would improve**

I would not redesign anything. If I kept going, I would expand the app with new features, like adding durations so the scheduler can catch overlapping tasks.

**c. Key takeaway**

Using AI is like having a very helpful assistant. It can complete what it is given, but at the end of the day the result is my responsibility. I reap the rewards or the consequences of whatever happens, so I have to understand and check the work instead of just trusting it.
