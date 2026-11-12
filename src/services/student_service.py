"""业务逻辑层 —— 学生信息管理。"""
from models import student_dao

REQUIRED_FIELDS = ('student_no', 'name')


def _validate(data):
    """校验学生数据，返回清洗后的数据字典。"""
    student_no = (data.get('student_no') or '').strip()
    name = (data.get('name') or '').strip()
    if not student_no:
        raise ValueError("学号不能为空")
    if not name:
        raise ValueError("姓名不能为空")

    class_id = data.get('class_id') or None
    if class_id is not None:
        class_id = int(class_id)

    return {
        'student_no': student_no,
        'name': name,
        'gender': (data.get('gender') or '').strip(),
        'birth_date': (data.get('birth_date') or '').strip() or None,
        'class_id': class_id,
        'phone': (data.get('phone') or '').strip(),
        'email': (data.get('email') or '').strip(),
    }


def list_students(conn, keyword=None):
    return student_dao.list_all(conn, keyword)


def get_student(conn, student_id):
    return student_dao.get(conn, student_id)


def add_student(conn, data):
    data = _validate(data)
    if student_dao.get_by_no(conn, data['student_no']):
        raise ValueError("学号已存在")
    return student_dao.create(conn, data)


def update_student(conn, student_id, data):
    data = _validate(data)
    existing = student_dao.get_by_no(conn, data['student_no'])
    if existing and existing['id'] != student_id:
        raise ValueError("学号已被其他学生使用")
    student_dao.update(conn, student_id, data)


def delete_student(conn, student_id):
    student_dao.delete(conn, student_id)
