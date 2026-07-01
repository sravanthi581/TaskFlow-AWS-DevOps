from flask import Flask, render_template, request, redirect
from database import *

app = Flask(__name__)

initialize_database()


@app.route("/")
def home():

    tasks = get_tasks()

    return render_template(
        "index.html",
        tasks=tasks
    )


@app.route("/add", methods=["POST"])
def add():

    title = request.form["title"]

    if title:

        add_task(title)

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    delete_task(id)

    return redirect("/")

@app.route("/complete/<int:id>")
def complete(id):

    complete_task(id)

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)