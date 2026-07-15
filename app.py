from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    session
)

from functools import wraps
from datetime import datetime
import logging
import os

from database import *

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "taskflow-secret-key"
)

logging.basicConfig(
    filename="taskflow.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

init_db()

# =====================================================
# LOGIN REQUIRED
# =====================================================

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login first.",
                "warning"
            )

            return redirect("/login")

        return func(*args, **kwargs)

    return wrapper


# =====================================================
# HOME
# =====================================================

@app.route("/")

def home():

    if "user_id" in session:

        return redirect("/dashboard")

    return redirect("/login")


# =====================================================
# LOGIN
# =====================================================

@app.route(
    "/login",
    methods=["GET","POST"]
)

def login():

    if request.method=="POST":

        email=request.form["email"].strip()

        password=request.form["password"]

        user=authenticate_user(
            email,
            password
        )

        if user:

            session["user_id"]=user["id"]

            session["username"]=user["username"]

            flash(
                f"Welcome {user['username']}!",
                "success"
            )

            logging.info(
                f"{email} logged in"
            )

            return redirect("/dashboard")

        flash(
            "Invalid Email or Password",
            "danger"
        )

    return render_template("login.html")


# =====================================================
# REGISTER
# =====================================================

@app.route(
    "/register",
    methods=["GET","POST"]
)

def register():

    if request.method=="POST":

        username=request.form["username"].strip()

        email=request.form["email"].strip()

        password=request.form["password"]

        if register_user(
            username,
            email,
            password
        ):

            flash(
                "Registration Successful. Please Login.",
                "success"
            )

            logging.info(
                f"{email} registered"
            )

            return redirect("/login")

        flash(
            "Email already exists.",
            "danger"
        )

    return render_template("register.html")


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")

def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "info"
    )

    return redirect("/login")


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")

@login_required

def dashboard():

    user_id=session["user_id"]

    search=request.args.get(
        "search",
        ""
    ).strip()

    status=request.args.get(
        "status",
        "all"
    )

    if search:

        tasks=search_tasks(
            user_id,
            search
        )

    elif status!="all":

        tasks=get_tasks_by_status(
            user_id,
            status
        )

    else:

        tasks=get_tasks(
            user_id
        )

    stats=get_statistics(
        user_id
    )

    user=get_user(
        user_id
    )

    return render_template(

        "index.html",

        tasks=tasks,

        stats=stats,

        user=user,

        search=search,

        status=status,

        today=datetime.now().strftime(
            "%d %B %Y"
        )

    )

# =====================================================
# ADD TASK
# =====================================================

@app.route(
    "/add",
    methods=["POST"]
)
@login_required
def add():

    title = request.form["title"].strip()

    description = request.form["description"].strip()

    priority = request.form["priority"]

    due_date = request.form["due_date"]

    if title:

        add_task(

            title,

            description,

            priority,

            "Pending",

            due_date,

            session["user_id"]

        )

        logging.info(

            f"{session['username']} added task '{title}'"

        )

        flash(

            "Task added successfully.",

            "success"

        )

    else:

        flash(

            "Task title cannot be empty.",

            "warning"

        )

    return redirect("/dashboard")


# =====================================================
# COMPLETE TASK
# =====================================================

@app.route(
    "/complete/<int:task_id>"
)
@login_required
def complete(task_id):

    task = get_task(task_id)

    if task:

        complete_task(task_id)

        logging.info(

            f"Completed Task : {task_id}"

        )

        flash(

            "Task marked as completed.",

            "success"

        )

    else:

        flash(

            "Task not found.",

            "danger"

        )

    return redirect("/dashboard")


# =====================================================
# DELETE TASK
# =====================================================

@app.route(
    "/delete/<int:task_id>"
)
@login_required
def delete(task_id):

    task = get_task(task_id)

    if task:

        delete_task(task_id)

        logging.info(

            f"Deleted Task : {task_id}"

        )

        flash(

            "Task deleted successfully.",

            "warning"

        )

    else:

        flash(

            "Task not found.",

            "danger"

        )

    return redirect("/dashboard")


# =====================================================
# EDIT TASK
# =====================================================

@app.route(
    "/edit/<int:task_id>",
    methods=["GET","POST"]
)
@login_required
def edit(task_id):

    task = get_task(task_id)

    if not task:

        flash(

            "Task not found.",

            "danger"

        )

        return redirect("/dashboard")

    if request.method=="POST":

        title=request.form["title"]

        description=request.form["description"]

        priority=request.form["priority"]

        status=request.form["status"]

        due_date=request.form["due_date"]

        update_task(

            task_id,

            title,

            description,

            priority,

            status,

            due_date

        )

        logging.info(

            f"Updated Task : {task_id}"

        )

        flash(

            "Task updated successfully.",

            "success"

        )

        return redirect("/dashboard")

    return render_template(

        "edit_task.html",

        task=task

    )


# =====================================================
# PROFILE
# =====================================================

@app.route("/profile")
@login_required
def profile():

    user = get_user(

        session["user_id"]

    )

    stats = get_statistics(

        session["user_id"]

    )

    tasks = get_tasks(

        session["user_id"]

    )

    return render_template(

        "profile.html",

        user=user,

        stats=stats,

        tasks=tasks,

        today=datetime.now().strftime(

            "%d %B %Y"

        )

    )
# =====================================================
# HEALTH CHECK
# =====================================================

@app.route("/health")
def health():

    return {

        "status": "healthy",

        "application": "TaskFlow",

        "version": "2.0",

        "server_time": datetime.now().strftime(
            "%d-%m-%Y %H:%M:%S"
        )

    }, 200


# =====================================================
# ABOUT PAGE (Optional)
# =====================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# =====================================================
# CONTEXT PROCESSOR
# Available in every template
# =====================================================

@app.context_processor
def inject_globals():

    return {

        "current_year": datetime.now().year,

        "app_name": "TaskFlow"

    }


# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    logging.warning(

        f"404 Error : {request.path}"

    )

    return render_template(
        "404.html"
    ),404


@app.errorhandler(500)
def internal_server_error(error):

    logging.error(

        f"500 Error : {error}"

    )

    return render_template(
        "500.html"
    ),500


# =====================================================
# BEFORE REQUEST
# =====================================================

@app.before_request
def before_request():

    logging.info(

        f"{request.method} -> {request.path}"

    )


# =====================================================
# AFTER REQUEST
# =====================================================

@app.after_request
def after_request(response):

    response.headers["Cache-Control"]="no-store"

    return response


# =====================================================
# MAIN
# =====================================================

if __name__=="__main__":

    print("="*60)
    print("          TaskFlow Application Started")
    print("="*60)
    print("Running on : http://127.0.0.1:5000")
    print("Health API : http://127.0.0.1:5000/health")
    print("="*60)

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )