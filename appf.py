# from datetime import datetime, timedelta
# import json
# import uuid
# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)


# # ---------- JSON LOAD / SAVE ----------
# def load_tasks():
#     try:
#         with open("tasks.json", "r") as file:
#             return json.load(file)
#     except:
#         return []


# def save_tasks(tasks):
#     with open("tasks.json", "w") as file:
#         json.dump(tasks, file, indent=4)

# def clean_old_tasks(days=30):
#     global tasks

#     cutoff = datetime.now() - timedelta(days=days)

#     new_tasks = []
#     for t in tasks:
#         try:
#             task_date = datetime.strptime(t["date"], "%Y-%m-%d")
#             if task_date >= cutoff:
#                 new_tasks.append(t)
#         except:
#             # agar date format galat ho to skip
#             continue

#     tasks = new_tasks
#     save_tasks(tasks)       


# # ---------- STORAGE ----------
# tasks = load_tasks()
# clean_old_tasks(30)   # last 30 days only
# def clean_old_tasks(days=30):
#     global tasks

#     cutoff = datetime.now() - timedelta(days=days)

#     cleaned = []

#     for t in tasks:
#         try:
#             task_date = datetime.strptime(t["date"], "%Y-%m-%d")

#             if task_date >= cutoff:
#                 cleaned.append(t)

#         except:
#             continue

#     tasks = cleaned
#     save_tasks(tasks)

# # ---------- HOME ----------
# @app.route("/")
# def home():
#     return render_template("index.html")


# # ---------- ADD TASKS ----------
# @app.route("/add", methods=["POST"])
# def add_task():
#     global tasks

#     name = request.form.get("name")
#     date = request.form.get("date")

#     for i in range(1, 12):
#         work_type = request.form.get(f"work_type{i}")
#         details = request.form.get(f"details{i}")
#         status = request.form.get(f"status{i}")
#         tat = request.form.get(f"tat{i}")
#         qa = request.form.get(f"qa{i}")
#         others = request.form.get(f"others{i}")

#         if details or tat or qa or others:
#             tasks.append({
#                 "id": str(uuid.uuid4()),
#                 "name": name,
#                 "date": date,
#                 "work_type": work_type,
#                 "details": details,
#                 "status": status,
#                 "tat": tat,
#                 "qa": qa,
#                 "others": others
                
#             })

#     save_tasks(tasks)
#     return redirect(url_for("home"))


# # ---------- VIEW USER TASKS ----------
# @app.route("/mytasks")
# def my_tasks():
#     name = request.args.get("name")
#     date = request.args.get("date")

#     user_tasks = []

#     for t in tasks:
#         if t["name"].lower() == name.lower() and t["date"] == date:
#             user_tasks.append(t)

#     return render_template("mytasks.html", tasks=user_tasks, name=name)


# # ---------- EDIT TASK ----------
# @app.route("/edit/<task_id>", methods=["GET", "POST"])
# def edit_task(task_id):
#     global tasks

#     task = None
#     for t in tasks:
#         if t["id"] == task_id:
#             task = t
#             break

#     if not task:
#         return "Task not found"

#     if request.method == "POST":
#         task["details"] = request.form.get("details")
#         task["status"] = request.form.get("status")
#         task["tat"] = request.form.get("tat")
#         task["qa"] = request.form.get("qa")
#         task["others"] = request.form.get("others")

#         save_tasks(tasks)

#         return redirect(f"/mytasks?name={task['name']}&date={task['date']}")

#     return render_template("edituser.html", task=task)


# # ---------- DASHBOARD (DATE-WISE CLEAN) ----------
# @app.route("/dashboard")
# def dashboard():
#     name = request.args.get("name")
#     date = request.args.get("date")

#     filtered_tasks = tasks

#     if name:
#         filtered_tasks = [
#             t for t in filtered_tasks
#             if name.lower() in t["name"].lower()
#         ]

#     if date:
#         filtered_tasks = [
#             t for t in filtered_tasks
#             if t["date"] == date
#         ]

#     # GROUP BY DATE → THEN USER
#     grouped = {}

#     for t in filtered_tasks:
#         d = t["date"]

#         if d not in grouped:
#             grouped[d] = {}

#         if t["name"] not in grouped[d]:
#             grouped[d][t["name"]] = []

#         grouped[d][t["name"]].append(t)

#     return render_template("dashboard.html", grouped_tasks=grouped)


# # ---------- UPDATE STATUS ----------
# @app.route("/update_status/<task_id>", methods=["POST"])
# def update_status(task_id):
#     global tasks

#     new_status = request.form.get("status")

#     for t in tasks:
#         if t["id"] == task_id:
#             t["status"] = new_status
#             break

#     save_tasks(tasks)
#     return redirect("/dashboard")
# @app.route("/analytics")
# def analytics():
#     grouped = {}

#     for t in tasks:
#         d = t["date"]

#         if d not in grouped:
#             grouped[d] = {
#                 "total": 0,
#                 "completed": 0,
#                 "in_progress": 0,
#                 "not_started": 0
#             }

#         grouped[d]["total"] += 1

#         if t["status"] == "completed":
#             grouped[d]["completed"] += 1
#         elif t["status"] == "in_progress":
#             grouped[d]["in_progress"] += 1
#         else:
#             grouped[d]["not_started"] += 1

#     return render_template("analytics.html", data=grouped)


# # ---------- RUN ----------
# if __name__ == "__main__":
#     app.run(debug=True)

# import psycopg2
# import os
# import uuid
# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)
# def get_db():
#     DATABASE_URL = "postgresql://kanban_a94j_user:GhPg0XVmULrCA8ODKM9OHiT59f7pY4G8@dpg-d7i70hfavr4c73ffh2m0-a.virginia-postgres.render.com/kanban_a94j"
#     conn = psycopg2.connect(DATABASE_URL)
#     return conn
# def create_table():
#     conn = get_db()
#     cur = conn.cursor()

#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS tasks (
#         id SERIAL PRIMARY KEY,
#         name TEXT,
#         date TEXT,
#         work_type TEXT,
#         details TEXT,
#         status TEXT,
#         tat TEXT,
#         qa TEXT,
#         others TEXT
#     )
#     """)

#     conn.commit()
#     cur.close()
#     conn.close()
# create_table()



# # ---------- INIT DB ----------
# def init_db():
#     conn = get_db()
#     conn.execute("""
#         CREATE TABLE IF NOT EXISTS tasks (
#             id TEXT PRIMARY KEY,
#             name TEXT,
#             date TEXT,
#             work_type TEXT,
#             details TEXT,
#             status TEXT,
#             tat TEXT,
#             qa TEXT,
#             others TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()


# init_db()


# # ---------- HOME ----------
# @app.route("/")
# def home():
#     return render_template("index.html")


# # ---------- ADD TASK ----------
# @app.route("/add", methods=["POST"])
# def add_task():
#     name = request.form.get("name")
#     date = request.form.get("date")

#     conn = get_db()

#     for i in range(1, 12):
#         work_type = request.form.get(f"work_type{i}")
#         details = request.form.get(f"details{i}")
#         status = request.form.get(f"status{i}")
#         tat = request.form.get(f"tat{i}")
#         qa = request.form.get(f"qa{i}")
#         others = request.form.get(f"others{i}")

#         if details or tat or qa or others:
#             conn.execute("""
#                 INSERT INTO tasks (id, name, date, work_type, details, status, tat, qa, others)
#                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
#             """, (
#                 str(uuid.uuid4()),
#                 name,
#                 date,
#                 work_type,
#                 details,
#                 status,
#                 tat,
#                 qa,
#                 others
#             ))

#     conn.commit()
#     conn.close()

#     return redirect(url_for("home"))


# # ---------- VIEW USER TASKS ----------
# @app.route("/mytasks")
# def my_tasks():
#     name = request.args.get("name")
#     date = request.args.get("date")

#     conn = get_db()

#     rows = conn.execute("""
#         SELECT * FROM tasks
#         WHERE LOWER(name) = LOWER(?) AND date = ?
#     """, (name, date)).fetchall()

#     conn.close()

#     tasks = [dict(row) for row in rows]

#     return render_template("mytasks.html", tasks=tasks, name=name)


# # ---------- EDIT TASK ----------
# @app.route("/edit/<task_id>", methods=["GET", "POST"])
# def edit_task(task_id):
#     conn = get_db()

#     row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()

#     if not row:
#         return "Task not found"

#     task = dict(row)

#     if request.method == "POST":
#         conn.execute("""
#             UPDATE tasks
#             SET details=?, status=?, tat=?, qa=?, others=?
#             WHERE id=?
#         """, (
#             request.form.get("details"),
#             request.form.get("status"),
#             request.form.get("tat"),
#             request.form.get("qa"),
#             request.form.get("others"),
#             task_id
#         ))

#         conn.commit()
#         conn.close()

#         return redirect(f"/mytasks?name={task['name']}&date={task['date']}")

#     conn.close()
#     return render_template("edituser.html", task=task)


# # ---------- DASHBOARD ----------
# @app.route("/dashboard")
# def dashboard():
#     name = request.args.get("name")
#     date = request.args.get("date")

#     conn = get_db()
#     rows = conn.execute("SELECT * FROM tasks").fetchall()
#     conn.close()

#     tasks = [dict(row) for row in rows]

#     # FILTER
#     if name:
#         tasks = [t for t in tasks if name.lower() in t["name"].lower()]

#     if date:
#         tasks = [t for t in tasks if t["date"] == date]

#     # GROUP
#     grouped = {}

#     for t in tasks:
#         d = t["date"]

#         if d not in grouped:
#             grouped[d] = {}

#         if t["name"] not in grouped[d]:
#             grouped[d][t["name"]] = []

#         grouped[d][t["name"]].append(t)

#     return render_template("dashboard.html", grouped_tasks=grouped)


# # ---------- UPDATE STATUS ----------
# @app.route("/update_status/<task_id>", methods=["POST"])
# def update_status(task_id):
#     new_status = request.form.get("status")

#     conn = get_db()
#     conn.execute("UPDATE tasks SET status=? WHERE id=?", (new_status, task_id))
#     conn.commit()
#     conn.close()

#     return redirect("/dashboard")


# # ---------- ANALYTICS ----------
# @app.route("/analytics")
# def analytics():
#     conn = get_db()
#     rows = conn.execute("SELECT * FROM tasks").fetchall()
#     conn.close()

#     tasks = [dict(row) for row in rows]

#     # -------- Date-wise summary --------
#     grouped = {}
#     for t in tasks:
#         d = t["date"]

#         if d not in grouped:
#             grouped[d] = {
#                 "total": 0,
#                 "completed": 0,
#                 "in_progress": 0,
#                 "not_started": 0
#             }

#         grouped[d]["total"] += 1

#         if t["status"] == "completed":
#             grouped[d]["completed"] += 1
#         elif t["status"] == "in_progress":
#             grouped[d]["in_progress"] += 1
#         else:
#             grouped[d]["not_started"] += 1

#     # -------- Busy employee --------
#     from collections import Counter

#     user_load = Counter([t["name"] for t in tasks])
#     top_user = user_load.most_common(1)[0] if user_load else ("N/A", 0)

#     # -------- Busiest day --------
#     date_load = {d: data["total"] for d, data in grouped.items()}
#     busiest_day = max(date_load, key=date_load.get) if date_load else "N/A"

#     # -------- Bottleneck --------
#     total_in_progress = sum([t["status"] == "in_progress" for t in tasks])

#     return render_template(
#         "analytics.html",
#         data=grouped,
#         top_user=top_user,
#         busiest_day=busiest_day,
#         in_progress=total_in_progress
#     )

# # ---------- RUN ----------
# if __name__ == "__main__":
#     app.run(debug=True)

import psycopg2
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------- DB CONNECTION ----------
def get_db():
    DATABASE_URL = "postgresql://kanban_a94j_user:GhPg0XVmULrCA8ODKM9OHiT59f7pY4G8@dpg-d7i70hfavr4c73ffh2m0-a.virginia-postgres.render.com/kanban_a94j"   # 👈 apna URL paste kar
    return psycopg2.connect(DATABASE_URL)


# ---------- CREATE TABLE ----------
def create_table():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        name TEXT,
        date TEXT,
        work_type TEXT,
        details TEXT,
        status TEXT,
        tat TEXT,
        qa TEXT,
        others TEXT
    )
    """)

    conn.commit()
    cur.close()
    conn.close()


create_table()


# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")


# ---------- ADD TASK ----------
@app.route("/add", methods=["POST"])
def add_task():
    conn = get_db()
    cur = conn.cursor()

    name = request.form.get("name")
    date = request.form.get("date")

    for i in range(1, 12):
        work_type = request.form.get(f"work_type{i}")
        details = request.form.get(f"details{i}")
        status = request.form.get(f"status{i}")
        tat = request.form.get(f"tat{i}")
        qa = request.form.get(f"qa{i}")
        others = request.form.get(f"others{i}")

        if details or tat or qa or others:
            cur.execute("""
                INSERT INTO tasks (name, date, work_type, details, status, tat, qa, others)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, date, work_type, details, status, tat, qa, others))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("home"))


# ---------- VIEW USER TASKS ----------
@app.route("/mytasks")
def my_tasks():
    name = request.args.get("name")
    date = request.args.get("date")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM tasks
        WHERE LOWER(name) = LOWER(%s) AND date = %s
    """, (name, date))

    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    tasks = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()

    return render_template("mytasks.html", tasks=tasks, name=name)


# ---------- EDIT TASK ----------
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    row = cur.fetchone()

    if not row:
        return "Task not found"

    columns = [desc[0] for desc in cur.description]
    task = dict(zip(columns, row))

    if request.method == "POST":
        cur.execute("""
            UPDATE tasks
            SET details=%s, status=%s, tat=%s, qa=%s, others=%s
            WHERE id=%s
        """, (
            request.form.get("details"),
            request.form.get("status"),
            request.form.get("tat"),
            request.form.get("qa"),
            request.form.get("others"),
            task_id
        ))

        conn.commit()
        cur.close()
        conn.close()

        return redirect(f"/mytasks?name={task['name']}&date={task['date']}")

    cur.close()
    conn.close()

    return render_template("edituser.html", task=task)


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    name = request.args.get("name")
    date = request.args.get("date")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    tasks = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()

    # FILTER
    if name:
        tasks = [t for t in tasks if name.lower() in t["name"].lower()]

    if date:
        tasks = [t for t in tasks if t["date"] == date]

    # GROUP
    grouped = {}

    for t in tasks:
        d = t["date"]

        if d not in grouped:
            grouped[d] = {}

        if t["name"] not in grouped[d]:
            grouped[d][t["name"]] = []

        grouped[d][t["name"]].append(t)

    return render_template("dashboard.html", grouped_tasks=grouped)


# ---------- UPDATE STATUS ----------
@app.route("/update_status/<int:task_id>", methods=["POST"])
def update_status(task_id):
    new_status = request.form.get("status")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE tasks SET status=%s WHERE id=%s", (new_status, task_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect("/dashboard")


# ---------- ANALYTICS ----------
@app.route("/analytics")
def analytics():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    tasks = [dict(zip(columns, row)) for row in rows]

    cur.close()
    conn.close()

    # SUMMARY
    grouped = {}

    for t in tasks:
        d = t["date"]

        if d not in grouped:
            grouped[d] = {"total": 0, "completed": 0, "in_progress": 0, "not_started": 0}

        grouped[d]["total"] += 1

        if t["status"] == "completed":
            grouped[d]["completed"] += 1
        elif t["status"] == "in_progress":
            grouped[d]["in_progress"] += 1
        else:
            grouped[d]["not_started"] += 1

    from collections import Counter

    user_load = Counter([t["name"] for t in tasks])
    top_user = user_load.most_common(1)[0] if user_load else ("N/A", 0)

    date_load = {d: data["total"] for d, data in grouped.items()}
    busiest_day = max(date_load, key=date_load.get) if date_load else "N/A"

    total_in_progress = sum([t["status"] == "in_progress" for t in tasks])

    return render_template(
        "analytics.html",
        data=grouped,
        top_user=top_user,
        busiest_day=busiest_day,
        in_progress=total_in_progress
    )


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)