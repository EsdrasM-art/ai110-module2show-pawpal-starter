from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A smart pet care planner: add pets, schedule tasks, and see a sorted daily plan.")

# --- Application "memory" -------------------------------------------------
# Streamlit reruns this script on every click, so the Owner lives in session_state.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)


def task_rows(tasks):
    """Convert Task objects into dicts that st.table can display."""
    return [
        {
            "Date": str(t.due_date),
            "Time": t.time,
            "Pet": t.pet_name,
            "Task": t.description,
            "Repeats": t.frequency,
            "Done": "yes" if t.completed else "no",
        }
        for t in tasks
    ]


# --- Owner ----------------------------------------------------------------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name, key="owner_name")

# --- Add a pet ------------------------------------------------------------
st.subheader("Add a pet")
col1, col2 = st.columns(2)
with col1:
    new_pet_name = st.text_input("Pet name", value="Mochi", key="new_pet_name")
with col2:
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], key="new_pet_species")

if st.button("Add pet", key="add_pet"):
    name = new_pet_name.strip()
    if not name:
        st.error("Please enter a pet name.")
    elif owner.get_pet(name) is not None:
        st.warning(f"You already have a pet named {name}.")
    else:
        owner.add_pet(Pet(name, new_pet_species))
        st.success(f"Added {name} the {new_pet_species}!")

if owner.pets:
    st.write("Your pets: " + ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Schedule a task ------------------------------------------------------
st.subheader("Schedule a task")
if not owner.pets:
    st.info("Add a pet first, then you can schedule tasks for it.")
else:
    col1, col2 = st.columns(2)
    with col1:
        task_pet = st.selectbox("Pet", [p.name for p in owner.pets], key="task_pet")
        task_desc = st.text_input("Task", value="Morning walk", key="task_desc")
        task_freq = st.selectbox("Repeats", ["once", "daily", "weekly"], key="task_freq")
    with col2:
        task_time = st.time_input("Time", value=time(8, 0), key="task_time")
        task_date = st.date_input("Date", value=date.today(), key="task_date")

    if st.button("Add task", key="add_task"):
        if not task_desc.strip():
            st.error("Please enter a task description.")
        else:
            pet = owner.get_pet(task_pet)
            pet.add_task(
                Task(
                    description=task_desc.strip(),
                    time=task_time.strftime("%H:%M"),
                    frequency=task_freq,
                    due_date=task_date,
                )
            )
            st.success(f"Scheduled '{task_desc.strip()}' for {task_pet} at {task_time.strftime('%H:%M')}.")

st.divider()

# --- Conflict warnings ----------------------------------------------------
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.subheader("Heads up")
    for message in conflicts:
        st.warning(message + " You may want to move one of these tasks.")

# --- Today's schedule -----------------------------------------------------
st.subheader("Today's schedule")
todays = scheduler.get_todays_schedule()
if todays:
    st.table(task_rows(todays))
elif owner.get_all_tasks():
    st.success("Nothing left to do today!")
else:
    st.info("No tasks yet. Schedule one above.")

# --- Mark a task complete -------------------------------------------------
pending = scheduler.sort_by_time(scheduler.filter_tasks(completed=False))
if pending:
    st.subheader("Mark a task complete")
    labels = [f"{t.due_date} {t.time} - {t.pet_name}: {t.description}" for t in pending]
    choice = st.selectbox("Task", range(len(pending)), format_func=lambda i: labels[i], key="complete_choice")
    if st.button("Mark complete", key="mark_complete"):
        next_task = scheduler.mark_task_complete(pending[choice])
        if next_task is not None:
            st.success(f"Done! Next {next_task.frequency} occurrence added for {next_task.due_date}.")
        else:
            st.success("Done!")
        st.rerun()

st.divider()

# --- Filter and browse all tasks -----------------------------------------
st.subheader("All tasks")
col1, col2 = st.columns(2)
with col1:
    pet_filter = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets], key="pet_filter")
with col2:
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Completed"], key="status_filter")

filtered = scheduler.filter_tasks(
    pet_name=None if pet_filter == "All" else pet_filter,
    completed={"All": None, "Pending": False, "Completed": True}[status_filter],
)
filtered = scheduler.sort_by_time(filtered)
if filtered:
    st.table(task_rows(filtered))
else:
    st.info("No tasks match these filters.")
