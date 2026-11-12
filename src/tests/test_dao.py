"""数据访问层（DAO）单元测试。"""
import sqlite3
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import class_dao, course_dao, grade_dao, student_dao

SCHEMA = Path(__file__).resolve().parents[1] / 'schema.sql'


def make_conn():
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text(encoding='utf-8'))
    return conn


class TestClassDao(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()

    def tearDown(self):
        self.conn.close()

    def test_create_and_list(self):
        class_dao.create(self.conn, '软工2101班', '软件工程', '2021', '张老师')
        rows = class_dao.list_all(self.conn)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['name'], '软工2101班')

    def test_update_and_delete(self):
        cid = class_dao.create(self.conn, '软工2101班', '软件工程', '2021', '张老师')
        class_dao.update(self.conn, cid, '软工2101班', '软件工程', '2021', '李老师')
        self.assertEqual(class_dao.get(self.conn, cid)['head_teacher'], '李老师')
        class_dao.delete(self.conn, cid)
        self.assertIsNone(class_dao.get(self.conn, cid))


class TestStudentDao(unittest.TestCase):
    def setUp(self):
        self.conn = make_conn()
        self.cid = class_dao.create(self.conn, '软工2101班', '软件工程', '2021', '张老师')

    def tearDown(self):
        self.conn.close()

    def _data(self, no='20210101'):
        return {
            'student_no': no, 'name': '王小明', 'gender': '男',
            'birth_date': '2003-01-15', 'class_id': self.cid,
            'phone': '13800000001', 'email': 'a@b.com',
        }

    def test_create_get_list(self):
        sid = student_dao.create(self.conn, self._data())
        s = student_dao.get(self.conn, sid)
        self.assertEqual(s['name'], '王小明')
        self.assertEqual(s['class_name'], '软工2101班')
        self.assertEqual(len(student_dao.list_all(self.conn)), 1)

    def test_search(self):
        student_dao.create(self.conn, self._data('20210101'))
        student_dao.create(self.conn, self._data('20210102'))
        self.assertEqual(len(student_dao.list_all(self.conn, '王小明')), 2)
        self.assertEqual(len(student_dao.list_all(self.conn, '20210101')), 1)

    def test_delete_cascades_grade(self):
        sid = student_dao.create(self.conn, self._data())
        course_id = course_dao.create(self.conn, 'CS101', '软件工程', 3.0, 48, '王教授')
        grade_dao.create(self.conn, sid, course_id, 90, '2025-2026-1')
        student_dao.delete(self.conn, sid)
        self.assertEqual(len(grade_dao.list_all(self.conn)), 0)


class TestGradeDao(unittest.TestCase):
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

    def test_create_and_statistics(self):
        grade_dao.create(self.conn, self.sid, self.course_id, 80, '2025-2026-1')
        grade_dao.create(self.conn, self.sid, self.course_id, 40, '2025-2026-2')
        stats = grade_dao.statistics(self.conn)
        self.assertEqual(stats['count'], 2)
        self.assertEqual(stats['avg'], 60.0)
        self.assertEqual(stats['pass_count'], 1)
        self.assertEqual(stats['pass_rate'], 50.0)


if __name__ == '__main__':
    unittest.main()
