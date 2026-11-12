"""数据访问层 —— 课程表（course）的增删改查。"""


def list_all(conn, keyword=None):
    """查询课程列表，可按课程号/课程名模糊搜索。"""
    sql = "SELECT * FROM course"
    params = ()
    if keyword:
        sql += " WHERE course_no LIKE ? OR name LIKE ?"
        like = f"%{keyword}%"
        params = (like, like)
    sql += " ORDER BY course_no"
    return conn.execute(sql, params).fetchall()


def get(conn, course_id):
    """按主键查询课程。"""
    return conn.execute("SELECT * FROM course WHERE id = ?", (course_id,)).fetchone()


def create(conn, course_no, name, credit, hours, teacher):
    """新增课程。"""
    cur = conn.execute(
        "INSERT INTO course (course_no, name, credit, hours, teacher) VALUES (?, ?, ?, ?, ?)",
        (course_no, name, credit, hours, teacher),
    )
    conn.commit()
    return cur.lastrowid


def update(conn, course_id, course_no, name, credit, hours, teacher):
    """更新课程。"""
    conn.execute(
        "UPDATE course SET course_no = ?, name = ?, credit = ?, hours = ?, teacher = ? WHERE id = ?",
        (course_no, name, credit, hours, teacher, course_id),
    )
    conn.commit()


def delete(conn, course_id):
    """删除课程（成绩因外键 ON DELETE CASCADE 一并删除）。"""
    conn.execute("DELETE FROM course WHERE id = ?", (course_id,))
    conn.commit()
