import json
import uuid
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except:
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
# In-memory storage
tasks = load_tasks()


# ---------- HOME (USER FORM) ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- ADD TASKS (TABLE FORMAT) ----------
@app.route("/add", methods=["POST"])
def add_task():
    global tasks

    name = request.form.get("name")
    date = request.form.get("date")

    # Loop through 11 work types
    for i in range(1, 12):
        work_type = request.form.get(f"work_type{i}")
        details = request.form.get(f"details{i}")
        status = request.form.get(f"status{i}")
        tat = request.form.get(f"tat{i}")
        qa = request.form.get(f"qa{i}")
        others = request.form.get(f"others{i}")

        # Save only if at least one field is filled
        if details or tat or qa or others:
            tasks.append({
                "id": str(uuid.uuid4()),
                "name": name,
                "date": date,
                "work_type": work_type,
                "details": details,
                "status": status,
                "tat": tat,
                "qa": qa,
                "others": others
            })
    save_tasks(tasks)

    return redirect(url_for("home"))


# ---------- VIEW USER TASKS ----------
@app.route("/mytasks")
def my_tasks():
    name = request.args.get("name")
    date = request.args.get("date")

    user_tasks = []

    for t in tasks:
        if t["name"] == name and t["date"] == date:
            user_tasks.append(t)

    return render_template("mytasks.html", tasks=user_tasks, name=name)

@app.route("/edit/<task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    global tasks

    # FIND TASK
    task = None
    for t in tasks:
        if t["id"] == task_id:
            task = t
            break

    if request.method == "POST":
        task["details"] = request.form.get("details")
        task["status"] = request.form.get("status")
        task["tat"] = request.form.get("tat")
        task["qa"] = request.form.get("qa")
        task["others"] = request.form.get("others")
        save_tasks(tasks)

        return redirect(f"/mytasks?name={task['name']}&date={task['date']}")

    return render_template("edituser.html", task=task)

# ---------- DASHBOARD (MANAGER VIEW) ----------
@app.route("/dashboard")
def dashboard():
    name = request.args.get("name")
    date = request.args.get("date")

    filtered_tasks = tasks

    # Name filter (partial + case insensitive)
    if name:
        filtered_tasks = [
            t for t in filtered_tasks
            if name.lower() in t["name"].lower()
        ]

    # Date filter
    if date:
        filtered_tasks = [
            t for t in filtered_tasks
            if t["date"] == date
        ]

    # GROUP + SUMMARY
    grouped = {}

    for t in filtered_tasks:
        if t["name"] not in grouped:
            grouped[t["name"]] = {
                "tasks": [],
                "total": 0,
                "completed": 0
            }

        grouped[t["name"]]["tasks"].append(t)
        grouped[t["name"]]["total"] += 1

        if t["status"] == "completed":
            grouped[t["name"]]["completed"] += 1

    # GLOBAL SUMMARY
    total = len(filtered_tasks)
    completed = len([t for t in filtered_tasks if t["status"] == "completed"])
    pending = total - completed

    return render_template(
        "dashboard.html",
        grouped_tasks=grouped,
        total=total,
        completed=completed,
        pending=pending
    )
@app.route("/update_status/<task_id>", methods=["POST"])
def update_status(task_id):
    global tasks

    new_status = request.form.get("status")

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = new_status
            break
    save_tasks(tasks)
    return redirect("/dashboard")


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)

    