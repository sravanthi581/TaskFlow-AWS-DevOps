import sqlite3

DATABASE = "taskflow.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():

    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            status INTEGER DEFAULT 0

        )
    """)

    conn.commit()
    conn.close()


# --------------------------
# CRUD OPERATIONS
# --------------------------

def get_tasks():
    conn = get_connection()

    tasks = conn.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return tasks


def add_task(title):

    conn = get_connection()

    conn.execute(
        "INSERT INTO tasks(title) VALUES(?)",
        (title,)
    )

    conn.commit()
    conn.close()

def delete_task(task_id):

    conn = get_connection()

    conn.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()

    conn.close()

def complete_task(task_id):

    conn = get_connection()

    conn.execute(
        "UPDATE tasks SET status=1 WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()