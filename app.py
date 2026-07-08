from flask import Flask, render_template, request, redirect
from database import *
from datetime import datetime
import logging

import os

app = Flask(__name__)

logging.basicConfig(

    filename="taskflow.log",

    level=logging.INFO,

    format="%(asctime)s %(levelname)s %(message)s"

)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "taskflow-secret-key"
)

initialize_database()


@app.route("/")
def home():

    search = request.args.get("search", "").strip()

    filter_status = request.args.get("status", "all")

    if search:

        tasks = get_tasks(search)

    else:

        tasks = get_tasks_by_status(filter_status)

    stats = task_statistics()

    return render_template(

        "index.html",

        tasks=tasks,

        total=stats["total"],

        completed=stats["completed"],

        pending=stats["pending"],

        search=search,

        status=filter_status,

        today=datetime.now().strftime("%d %B %Y")

    )


@app.route("/add", methods=["POST"])
def add():

    title = request.form["title"]


    description = request.form["description"]

    priority = request.form["priority"]

    category = request.form["category"]

    due_date = request.form["due_date"]

    if title:

        add_task(

            title,



            description,

            priority,

            category,

            due_date

        )

        logging.info(f"Task Added : {title}")

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    delete_task(id)

    logging.info(f"Deleted Task {id}")

    return redirect("/")


@app.route("/complete/<int:id>")
def complete(id):

    complete_task(id)

    logging.info(f"Completed Task {id}")

    return redirect("/")


if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )

@app.route("/health")
def health():

    return {

        "status":"healthy",

        "application":"TaskFlow",

        "version":"1.0"

    },200

@app.errorhandler(404)

def page_not_found(e):

    return render_template("404.html"),404

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    conn = get_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id=?",
        (id,)
    ).fetchone()

    conn.close()

    if request.method == "POST":

        update_task(

            id,

            request.form["title"],

            request.form["description"],

            request.form["priority"],

            request.form["category"],

            request.form["due_date"]

        )

        return redirect("/")

    return render_template(

        "edit_task.html",

        task=task

    )