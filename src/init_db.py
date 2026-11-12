"""数据库初始化脚本。

用法：在 src/ 目录下运行
    python init_db.py
"""
from pathlib import Path

from werkzeug.security import generate_password_hash

from models.db import connect

SCHEMA = Path(__file__).with_name('schema.sql')


def init(db_path):
    conn = connect(db_path)
    # 1. 建表
    conn.executescript(SCHEMA.read_text(encoding='utf-8'))

    # 2. 默认管理员账号（admin / admin123）
    conn.execute(
        "INSERT OR IGNORE INTO user (username, password_hash, role) VALUES (?, ?, ?)",
        ('admin', generate_password_hash('admin123'), 'admin'),
    )

    # 3. 示例数据（便于演示，仅当表为空时插入）
    if conn.execute("SELECT COUNT(*) AS c FROM class").fetchone()['c'] == 0:
        classes = [
            ('软件工程2101班', '软件工程', '2021', '张老师'),
            ('计算机科学2102班', '计算机科学与技术', '2021', '李老师'),
        ]
        conn.executemany(
            "INSERT INTO class (name, major, grade, head_teacher) VALUES (?, ?, ?, ?)",
            classes,
        )

    if conn.execute("SELECT COUNT(*) AS c FROM student").fetchone()['c'] == 0:
        students = [
            ('20210101', '王小明', '男', '2003-01-15', 1, '13800000001', 'wangxm@example.com'),
            ('20210102', '李小红', '女', '2003-05-20', 1, '13800000002', 'lixh@example.com'),
            ('20210201', '张伟', '男', '2002-11-02', 2, '13800000003', 'zhangwei@example.com'),
        ]
        conn.executemany(
            "INSERT INTO student (student_no, name, gender, birth_date, class_id, phone, email) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            students,
        )

    if conn.execute("SELECT COUNT(*) AS c FROM course").fetchone()['c'] == 0:
        courses = [
            ('CS101', '软件工程', 3.0, 48, '王教授'),
            ('CS102', '数据库原理', 3.5, 56, '刘教授'),
            ('CS103', '数据结构', 4.0, 64, '陈教授'),
        ]
        conn.executemany(
            "INSERT INTO course (course_no, name, credit, hours, teacher) VALUES (?, ?, ?, ?, ?)",
            courses,
        )

    if conn.execute("SELECT COUNT(*) AS c FROM grade").fetchone()['c'] == 0:
        grades = [
            (1, 1, 88.0, '2025-2026-1'),
            (1, 2, 92.0, '2025-2026-1'),
            (2, 1, 75.5, '2025-2026-1'),
            (2, 3, 59.0, '2025-2026-1'),
            (3, 2, 81.0, '2025-2026-1'),
        ]
        conn.executemany(
            "INSERT INTO grade (student_id, course_id, score, semester) VALUES (?, ?, ?, ?)",
            grades,
        )

    conn.commit()
    conn.close()
    print(f"数据库初始化完成：{db_path}")


if __name__ == '__main__':
    from config import DATABASE

    init(DATABASE)
