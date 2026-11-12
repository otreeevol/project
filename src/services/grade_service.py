"""业务逻辑层 —— 成绩管理。"""
from models import grade_dao


def _validate(data):
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    if not student_id:
        raise ValueError("请选择学生")
    if not course_id:
        raise ValueError("请选择课程")

    score = data.get('score')
    if score in (None, ''):
        raise ValueError("成绩不能为空")
    score = float(score)
    if not (0 <= score <= 100):
        raise ValueError("成绩必须在 0~100 之间")

    return {
        'student_id': int(student_id),
        'course_id': int(course_id),
        'score': score,
        'semester': (data.get('semester') or '').strip(),
    }


def list_grades(conn, student_id=None, course_id=None):
    return grade_dao.list_all(conn, student_id, course_id)


def get_grade(conn, grade_id):
    return grade_dao.get(conn, grade_id)


def add_grade(conn, data):
    d = _validate(data)
    return grade_dao.create(conn, d['student_id'], d['course_id'], d['score'], d['semester'])


def update_grade(conn, grade_id, data):
    d = _validate(data)
    grade_dao.update(conn, grade_id, d['student_id'], d['course_id'], d['score'], d['semester'])


def delete_grade(conn, grade_id):
    grade_dao.delete(conn, grade_id)


def statistics(conn, course_id=None):
    return grade_dao.statistics(conn, course_id)
