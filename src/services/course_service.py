"""业务逻辑层 —— 课程管理。"""
from models import course_dao


def _validate(data):
    course_no = (data.get('course_no') or '').strip()
    name = (data.get('name') or '').strip()
    if not course_no:
        raise ValueError("课程编号不能为空")
    if not name:
        raise ValueError("课程名称不能为空")
    credit = data.get('credit') or None
    hours = data.get('hours') or None
    return {
        'course_no': course_no,
        'name': name,
        'credit': float(credit) if credit not in (None, '') else None,
        'hours': int(hours) if hours not in (None, '') else None,
        'teacher': (data.get('teacher') or '').strip(),
    }


def list_courses(conn, keyword=None):
    return course_dao.list_all(conn, keyword)


def get_course(conn, course_id):
    return course_dao.get(conn, course_id)


def add_course(conn, data):
    d = _validate(data)
    return course_dao.create(conn, d['course_no'], d['name'], d['credit'], d['hours'], d['teacher'])


def update_course(conn, course_id, data):
    d = _validate(data)
    course_dao.update(conn, course_id, d['course_no'], d['name'], d['credit'], d['hours'], d['teacher'])


def delete_course(conn, course_id):
    course_dao.delete(conn, course_id)
