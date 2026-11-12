"""业务逻辑层 —— 班级管理。"""
from models import class_dao


def _validate(data):
    name = (data.get('name') or '').strip()
    if not name:
        raise ValueError("班级名称不能为空")
    return {
        'name': name,
        'major': (data.get('major') or '').strip(),
        'grade': (data.get('grade') or '').strip(),
        'head_teacher': (data.get('head_teacher') or '').strip(),
    }


def list_classes(conn):
    return class_dao.list_all(conn)


def get_class(conn, class_id):
    return class_dao.get(conn, class_id)


def add_class(conn, data):
    d = _validate(data)
    return class_dao.create(conn, d['name'], d['major'], d['grade'], d['head_teacher'])


def update_class(conn, class_id, data):
    d = _validate(data)
    class_dao.update(conn, class_id, d['name'], d['major'], d['grade'], d['head_teacher'])


def delete_class(conn, class_id):
    class_dao.delete(conn, class_id)
