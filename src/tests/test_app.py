"""表示层（Flask 应用）集成测试。"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import create_app
from init_db import init


class TestApp(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        init(self.db_path)  # 建表 + 默认账号 + 示例数据
        self.app = create_app()
        self.app.config['DATABASE'] = self.db_path
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def tearDown(self):
        os.unlink(self.db_path)

    def _login(self):
        return self.client.post('/login', data={
            'username': 'admin', 'password': 'admin123',
        }, follow_redirects=True)

    def test_redirect_when_not_logged_in(self):
        resp = self.client.get('/students/')
        self.assertEqual(resp.status_code, 302)

    def test_login_success(self):
        resp = self._login()
        self.assertEqual(resp.status_code, 200)
        self.assertIn('系统概览'.encode('utf-8'), resp.data)

    def test_login_fail(self):
        resp = self.client.post('/login', data={
            'username': 'admin', 'password': 'wrong',
        })
        self.assertIn('用户名或密码错误'.encode('utf-8'), resp.data)

    def test_student_add_flow(self):
        self._login()
        resp = self.client.post('/students/add', data={
            'student_no': '20219999', 'name': '测试学生', 'gender': '男',
            'class_id': '1', 'phone': '', 'email': '',
        }, follow_redirects=True)
        self.assertIn('学生添加成功'.encode('utf-8'), resp.data)

    def test_grade_add_invalid_score(self):
        self._login()
        resp = self.client.post('/grades/add', data={
            'student_id': '1', 'course_id': '1', 'score': '150',
        }, follow_redirects=True)
        self.assertIn('成绩必须在 0~100 之间'.encode('utf-8'), resp.data)


if __name__ == '__main__':
    unittest.main()
