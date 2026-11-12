"""数据访问层 —— 学生表（student）的增删改查。"""


def list_all(conn, keyword=None):
    """查询学生列表，可按学号/姓名模糊搜索，附带班级名称。"""
    sql = """
        SELECT s.*, c.name AS class_name
        FROM student s
        LEFT JOIN class c ON s.class_id = c.id
    """
    params = ()
    if keyword:
        sql += " WHERE s.student_no LIKE ? OR s.name LIKE ?"
        like = f"%{keyword}%"
        params = (like, like)
    sql += " ORDER BY s.student_no"
    return conn.execute(sql, params).fetchall()


def get(conn, student_id):
    """按主键查询学生，附带班级名称。"""
    return conn.execute(
        """
        SELECT s.*, c.name AS class_name
        FROM student s
        LEFT JOIN class c ON s.class_id = c.id
        WHERE s.id = ?
        """,
        (student_id,),
    ).fetchone()


def get_by_no(conn, student_no):
    """按学号查询学生。"""
    return conn.execute(
        "SELECT * FROM student WHERE student_no = ?", (student_no,)
    ).fetchone()


def create(conn, data):
    """新增学生。data 为字段字典。"""
    cur = conn.execute(
        """
        INSERT INTO student (student_no, name, gender, birth_date, class_id, phone, email)
        VALUES (:student_no, :name, :gender, :birth_date, :class_id, :phone, :email)
        """,
        data,
    )
    conn.commit()
    return cur.lastrowid


def update(conn, student_id, data):
    """更新学生。"""
    data = dict(data)
    data['id'] = student_id
    conn.execute(
        """
        UPDATE student
        SET student_no = :student_no, name = :name, gender = :gender,
            birth_date = :birth_date, class_id = :class_id,
            phone = :phone, email = :email
        WHERE id = :id
        """,
        data,
    )
    conn.commit()


def delete(conn, student_id):
    """删除学生（成绩因外键 ON DELETE CASCADE 一并删除）。"""
    conn.execute("DELETE FROM student WHERE id = ?", (student_id,))
    conn.commit()
