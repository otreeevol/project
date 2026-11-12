"""数据访问层 —— 成绩表（grade）的增删改查。"""


def list_all(conn, student_id=None, course_id=None):
    """查询成绩列表，附带学生姓名、学号与课程名称，支持按学生/课程过滤。"""
    sql = """
        SELECT g.*, s.name AS student_name, s.student_no AS student_no,
               c.name AS course_name
        FROM grade g
        JOIN student s ON g.student_id = s.id
        JOIN course  c ON g.course_id  = c.id
    """
    where, params = [], []
    if student_id:
        where.append("g.student_id = ?")
        params.append(student_id)
    if course_id:
        where.append("g.course_id = ?")
        params.append(course_id)
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY s.student_no, c.course_no"
    return conn.execute(sql, params).fetchall()


def get(conn, grade_id):
    """按主键查询成绩。"""
    return conn.execute("SELECT * FROM grade WHERE id = ?", (grade_id,)).fetchone()


def create(conn, student_id, course_id, score, semester):
    """新增成绩。"""
    cur = conn.execute(
        "INSERT INTO grade (student_id, course_id, score, semester) VALUES (?, ?, ?, ?)",
        (student_id, course_id, score, semester),
    )
    conn.commit()
    return cur.lastrowid


def update(conn, grade_id, student_id, course_id, score, semester):
    """更新成绩。"""
    conn.execute(
        "UPDATE grade SET student_id = ?, course_id = ?, score = ?, semester = ? WHERE id = ?",
        (student_id, course_id, score, semester, grade_id),
    )
    conn.commit()


def delete(conn, grade_id):
    """删除成绩。"""
    conn.execute("DELETE FROM grade WHERE id = ?", (grade_id,))
    conn.commit()


def statistics(conn, course_id=None):
    """统计成绩：平均分、最高分、最低分、及格率、人数。"""
    sql = "SELECT COUNT(*) AS cnt, AVG(score) AS avg, MAX(score) AS max, MIN(score) AS min FROM grade"
    params = ()
    if course_id:
        sql += " WHERE course_id = ?"
        params = (course_id,)
    row = conn.execute(sql, params).fetchone()

    pass_sql = "SELECT COUNT(*) AS cnt FROM grade WHERE score >= 60"
    pass_params = ()
    if course_id:
        pass_sql += " AND course_id = ?"
        pass_params = (course_id,)
    pass_row = conn.execute(pass_sql, pass_params).fetchone()

    cnt = row['cnt'] or 0
    return {
        'count': cnt,
        'avg': round(row['avg'], 2) if row['avg'] is not None else 0,
        'max': row['max'] if row['max'] is not None else 0,
        'min': row['min'] if row['min'] is not None else 0,
        'pass_count': pass_row['cnt'],
        'pass_rate': round(pass_row['cnt'] / cnt * 100, 2) if cnt else 0,
    }
