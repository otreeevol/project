"""数据访问层 —— 班级表（class）的增删改查。"""


def list_all(conn):
    """查询全部班级，附带每个班级的学生人数。"""
    return conn.execute(
        """
        SELECT c.*, COUNT(s.id) AS student_count
        FROM class c
        LEFT JOIN student s ON s.class_id = c.id
        GROUP BY c.id
        ORDER BY c.grade, c.name
        """
    ).fetchall()


def get(conn, class_id):
    """按主键查询班级。"""
    return conn.execute("SELECT * FROM class WHERE id = ?", (class_id,)).fetchone()


def create(conn, name, major, grade, head_teacher):
    """新增班级。"""
    cur = conn.execute(
        "INSERT INTO class (name, major, grade, head_teacher) VALUES (?, ?, ?, ?)",
        (name, major, grade, head_teacher),
    )
    conn.commit()
    return cur.lastrowid


def update(conn, class_id, name, major, grade, head_teacher):
    """更新班级。"""
    conn.execute(
        "UPDATE class SET name = ?, major = ?, grade = ?, head_teacher = ? WHERE id = ?",
        (name, major, grade, head_teacher, class_id),
    )
    conn.commit()


def delete(conn, class_id):
    """删除班级（学生因外键 ON DELETE SET NULL 而保留）。"""
    conn.execute("DELETE FROM class WHERE id = ?", (class_id,))
    conn.commit()
