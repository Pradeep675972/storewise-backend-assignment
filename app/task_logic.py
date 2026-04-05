from fastapi import HTTPException
from datetime import datetime, timedelta

# Q2: group tasks by parent id and sort latest first
def question2(task_list): 
    grouped_tasks = {}

    for task in task_list:
        parent = task.parent_id

        if parent not in grouped_tasks:
            grouped_tasks[parent] = []

        grouped_tasks[parent].append(task)

    for parent in grouped_tasks:
        grouped_tasks[parent].sort(
            key=lambda item: item.created_at,
            reverse=True
        )

    return grouped_tasks


# Q3: find urgent tasks (today or tomorrow + priority = 1)
def question3(task_list):
    urgent_tasks = []

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    for task in task_list:
        if task.priority == 1:
            due = task.due_date.date()

            if due == today or due == tomorrow:
                urgent_tasks.append(task)

    return urgent_tasks


# Q4: find parent tasks which have no children
def question4(task_list):
    parent_ids = set()

    for task in task_list:
        if task.parent_id:
            parent_ids.add(task.parent_id)

    result = []

    for task in task_list:
        if task.id not in parent_ids:
            result.append(task)

    return result


# Q5: count siblings of a given task
def question5(task_list, task_id: int):
    target_task = None

    for task in task_list:
        if task.id == task_id:
            target_task = task
            break

    if not target_task:
        return 0

    count = 0

    for task in task_list:
        if task.parent_id == target_task.parent_id and task.id != task_id:
            count += 1

    return count


# Q6: simple search (case-insensitive)
def question6(task_list, query: str):
    matched_tasks = []

    for task in task_list:
        if query.lower() in task.name.lower():
            matched_tasks.append(task)

    return matched_tasks


# Q7: check if tasks are related as parent-child
def question7(task_list):
    relations = []

    def is_subtask(parent_id, child_id):
        current = child_id

        while current:
            found = None

            for task in task_list:
                if task.id == current:
                    found = task
                    break

            if not found:
                return False

            if found.parent_id == parent_id:
                return True

            current = found.parent_id

        return False

    for t1 in task_list:
        for t2 in task_list:
            if t1.id != t2.id:
                if is_subtask(t1.id, t2.id):
                    relations.append({
                        "parent": t1.id,
                        "child": t2.id
                    })

    return relations


# Q8: already instructed to use SQLAlchemy directly
def question8(tasks, criteria: dict, sort_by: str):
    raise HTTPException(
        status_code=401,
        detail="Solve this using SQLAlchemy in main.py"
    )


# Q9: simulate task execution with workers
def question9(task_list, worker_threads: int):
    import time

    queue = task_list[:]
    active_tasks = []
    completed_tasks = []

    while queue or active_tasks:

        while len(active_tasks) < worker_threads and queue:
            task = queue.pop(0)
            active_tasks.append((task, time.time()))

        remaining_tasks = []

        for task, start_time in active_tasks:
            duration = task.duration / 10

            if time.time() - start_time >= duration:
                completed_tasks.append(task)
            else:
                remaining_tasks.append((task, start_time))

        active_tasks = remaining_tasks

    return completed_tasks