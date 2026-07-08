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

        description TEXT,

        priority TEXT DEFAULT 'Medium',

        category TEXT DEFAULT 'Personal',

        due_date TEXT,

        status INTEGER DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()

    conn.close()


def get_tasks(search=""):

    conn = get_connection()

    if search:

        tasks = conn.execute(
            """
            SELECT *

            FROM tasks

            WHERE

            title LIKE ?

            OR description LIKE ?

            OR category LIKE ?

            ORDER BY

            CASE priority

            WHEN 'High' THEN 1

            WHEN 'Medium' THEN 2

            ELSE 3

            END,

            id DESC
            """,

            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )

        ).fetchall()

    else:

        tasks = conn.execute(
            """
            SELECT *

            FROM tasks

            ORDER BY

            CASE priority

            WHEN 'High' THEN 1

            WHEN 'Medium' THEN 2

            ELSE 3

            END,

            id DESC
            """
        ).fetchall()

    conn.close()

    return tasks


def add_task(
        title,
        description="",
        priority="Medium",
        category="Personal",
        due_date=""
):

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO tasks
        (
            title,
            description,
            priority,
            category,
            due_date
        )

        VALUES(?,?,?,?,?)
        """,

        (
            title,
            description,
            priority,
            category,
            due_date
        )

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


def task_statistics():

    conn = get_connection()

    total = conn.execute(

        "SELECT COUNT(*) FROM tasks"

    ).fetchone()[0]

    completed = conn.execute(

        "SELECT COUNT(*) FROM tasks WHERE status=1"

    ).fetchone()[0]

    pending = total - completed

    conn.close()

    return {

        "total": total,

        "completed": completed,

        "pending": pending

    }

def update_task(task_id, title, description, priority, category, due_date):

    conn = get_connection()

    conn.execute(
        """
        UPDATE tasks
        SET
            title=?,
            description=?,
            priority=?,
            category=?,
            due_date=?
        WHERE id=?
        """,
        (
            title,
            description,
            priority,
            category,
            due_date,
            task_id
        )
    )

    conn.commit()
    conn.close()
    

def get_tasks_by_status(status):

    conn = get_connection()

    if status == "completed":

        tasks = conn.execute(
            "SELECT * FROM tasks WHERE status=1 ORDER BY id DESC"
        ).fetchall()

    elif status == "pending":

        tasks = conn.execute(
            "SELECT * FROM tasks WHERE status=0 ORDER BY id DESC"
        ).fetchall()

    else:

        tasks = conn.execute(
            "SELECT * FROM tasks ORDER BY id DESC"
        ).fetchall()

    conn.close()

    return tasks