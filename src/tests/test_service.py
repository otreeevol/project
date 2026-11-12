"""业务逻辑层（Service）单元测试。"""
import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import class_dao, course_dao, student_dao
from services import auth_service, grade_service, student_service

SCHEMA = Path(__file__).resolve().parents[1] / 'schema.sql'


def make_conn():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text(encoding='utf-8'))
    return conn


class TestAuthService(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()
        auth_service.create_user(self.conn, 'admin', 'admin123', 'admin')

    def tearDown(self):
        self.conn.close()

    def test_authenticate_ok(self):
        user = auth_service.authenticate(self.conn, 'admin', 'admin123')
        self.assertEqual(user['username'], 'admin')

    def test_authenticate_fail(self):
        with self.assertRaises(auth_service.AuthError):
            auth_service.authenticate(self.conn, 'admin', 'wrong')

    def test_duplicate_user(self):
        with self.assertRaises(ValueError):
            auth_service.create_user(self.conn, 'admin', 'x', 'admin')


class TestStudentService(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()
        self.cid = class_dao.create(self.conn, '软工2101班', '软件工程', '2021', '张老师')

    def tearDown(self):
        self.conn.close()

    def test_add_student(self):
        student_service.add_student(self.conn, {
            'student_no': '20210101', 'name': '王小明', 'class_id': str(self.cid),
        })
        self.assertEqual(len(student_service.list_students(self.conn)), 1)

    def test_missing_required(self):
        with self.assertRaises(ValueError):
            student_service.add_student(self.conn, {'student_no': '', 'name': ''})

    def test_duplicate_no(self):
        data = {'student_no': '20210101', 'name': '王小明'}
        student_service.add_student(self.conn, data)
        with self.assertRaises(ValueError):
            student_service.add_student(self.conn, data)


class TestGradeService(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()
        self.cid = class_dao.create(self.conn, '软工2101班', '软件工程', '2021', '张老师')
        self.sid = student_dao.create(self.conn, {
            'student_no': '20210101', 'name': '王小明', 'gender': '男',
            'birth_date': None, 'class_id': self.cid, 'phone': None, 'email': None,
        })
        self.course_id = course_dao.create(self.conn, 'CS101', '软件工程', 3.0, 48, '王教授')

    def tearDown(self):
        self.conn.close()

    def test_score_out_of_range(self):
        with self.assertRaises(ValueError):
            grade_service.add_grade(self.conn, {
                'student_id': str(self.sid), 'course_id': str(self.course_id), 'score': '120',
            })

    def test_add_grade_ok(self):
        grade_service.add_grade(self.conn, {
            'student_id': str(self.sid), 'course_id': str(self.course_id),
            'score': '88', 'semester': '2025-2026-1',
        })
        self.assertEqual(grade_service.statistics(self.conn)['avg'], 88.0)


if __name__ == '__main__':
    unittest.main()
