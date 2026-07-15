import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = "taskflow.db"


# =====================================================
# DATABASE CONNECTION
# =====================================================

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# =====================================================
# INITIALIZE DATABASE
# =====================================================

def init_db():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cur.execute("""

    CREATE TABLE IF NOT EXISTS tasks(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT NOT NULL,

        description TEXT,

        priority TEXT DEFAULT 'Medium',

        status TEXT DEFAULT 'Pending',

        due_date TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        user_id INTEGER NOT NULL,

        FOREIGN KEY(user_id) REFERENCES users(id)

    )

    """)

    conn.commit()

    conn.close()


# =====================================================
# USER FUNCTIONS
# =====================================================

def register_user(

        username,

        email,

        password

):

    conn = get_connection()

    cur = conn.cursor()

    hashed = generate_password_hash(password)

    try:

        cur.execute("""

        INSERT INTO users(

            username,

            email,

            password

        )

        VALUES(

            ?,

            ?,

            ?

        )

        """,

        (

            username,

            email,

            hashed

        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def authenticate_user(

        email,

        password

):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )

    user = cur.fetchone()

    conn.close()

    if user:

        if check_password_hash(

            user["password"],

            password

        ):

            return dict(user)

    return None


def get_user(user_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM users WHERE id=?",

        (user_id,)

    )

    user = cur.fetchone()

    conn.close()

    if user:

        return dict(user)

    return None


def update_password(

        user_id,

        new_password

):

    conn = get_connection()

    cur = conn.cursor()

    hashed = generate_password_hash(

        new_password

    )

    cur.execute("""

    UPDATE users

    SET password=?

    WHERE id=?

    """,

    (

        hashed,

        user_id

    ))

    conn.commit()

    conn.close()


# =====================================================
# TASK FUNCTIONS
# =====================================================

def add_task(

        title,

        description,

        priority,

        status,

        due_date,

        user_id

):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO tasks(

        title,

        description,

        priority,

        status,

        due_date,

        user_id

    )

    VALUES(

        ?,

        ?,

        ?,

        ?,

        ?,

        ?

    )

    """,

    (

        title,

        description,

        priority,

        status,

        due_date,

        user_id

    ))

    conn.commit()

    conn.close()


def get_tasks(user_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM tasks

    WHERE user_id=?

    ORDER BY created_at DESC

    """,

    (user_id,))

    tasks = cur.fetchall()

    conn.close()

    return tasks


def get_task(task_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        "SELECT * FROM tasks WHERE id=?",

        (task_id,)

    )

    task = cur.fetchone()

    conn.close()

    return task

# =====================================================
# UPDATE TASK
# =====================================================

def update_task(

        task_id,

        title,

        description,

        priority,

        status,

        due_date

):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    UPDATE tasks

    SET

        title=?,

        description=?,

        priority=?,

        status=?,

        due_date=?

    WHERE id=?

    """,

    (

        title,

        description,

        priority,

        status,

        due_date,

        task_id

    ))

    conn.commit()

    conn.close()


# =====================================================
# DELETE TASK
# =====================================================

def delete_task(task_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """

        DELETE FROM tasks

        WHERE id=?

        """,

        (task_id,)

    )

    conn.commit()

    conn.close()


# =====================================================
# COMPLETE TASK
# =====================================================

def complete_task(task_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """

        UPDATE tasks

        SET status='Completed'

        WHERE id=?

        """,

        (task_id,)

    )

    conn.commit()

    conn.close()


# =====================================================
# SEARCH TASKS
# =====================================================

def search_tasks(

        user_id,

        keyword

):

    conn = get_connection()

    cur = conn.cursor()

    keyword = f"%{keyword}%"

    cur.execute("""

    SELECT *

    FROM tasks

    WHERE

        user_id=?

        AND

        (

            title LIKE ?

            OR

            description LIKE ?

        )

    ORDER BY created_at DESC

    """,

    (

        user_id,

        keyword,

        keyword

    ))

    tasks = cur.fetchall()

    conn.close()

    return tasks


# =====================================================
# FILTER TASKS
# =====================================================

def get_tasks_by_status(

        user_id,

        status

):

    conn = get_connection()

    cur = conn.cursor()

    if status.lower() == "all":

        cur.execute("""

        SELECT *

        FROM tasks

        WHERE user_id=?

        ORDER BY created_at DESC

        """,

        (user_id,))

    else:

        cur.execute("""

        SELECT *

        FROM tasks

        WHERE

            user_id=?

            AND

            status=?

        ORDER BY created_at DESC

        """,

        (

            user_id,

            status

        ))

    tasks = cur.fetchall()

    conn.close()

    return tasks


# =====================================================
# DASHBOARD STATISTICS
# =====================================================

def get_statistics(user_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """

        SELECT COUNT(*)

        FROM tasks

        WHERE user_id=?

        """,

        (user_id,)

    )

    total = cur.fetchone()[0]

    cur.execute(

        """

        SELECT COUNT(*)

        FROM tasks

        WHERE

            status='Completed'

            AND

            user_id=?

        """,

        (user_id,)

    )

    completed = cur.fetchone()[0]

    cur.execute(

        """

        SELECT COUNT(*)

        FROM tasks

        WHERE

            status='Pending'

            AND

            user_id=?

        """,

        (user_id,)

    )

    pending = cur.fetchone()[0]

    cur.execute(

        """

        SELECT COUNT(*)

        FROM tasks

        WHERE

            priority='High'

            AND

            user_id=?

        """,

        (user_id,)

    )

    high = cur.fetchone()[0]

    conn.close()

    return {

        "total": total,

        "completed": completed,

        "pending": pending,

        "high": high

    }


# =====================================================
# DELETE USER
# =====================================================

def delete_user(user_id):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(

        """

        DELETE FROM tasks

        WHERE user_id=?

        """,

        (user_id,)

    )

    cur.execute(

        """

        DELETE FROM users

        WHERE id=?

        """,

        (user_id,)

    )

    conn.commit()

    conn.close()


# =====================================================
# INITIALIZE DATABASE
# =====================================================

init_db()