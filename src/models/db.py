"""数据访问层 —— 数据库连接管理。

提供两类接口：
1. `connect(db_path)`：面向测试/独立脚本的显式连接；
2. `get_db()` / `close_db()`：面向 Flask 应用上下文的请求级连接。
"""
import sqlite3

from flask import g, current_app


def connect(db_path):
    """建立数据库连接，返回配置好 Row 工厂与外键约束的 Connection。"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row          # 查询结果以列名访问
    conn.execute("PRAGMA foreign_keys = ON")  # 开启外键约束
    return conn


def get_db():
    """获取当前请求的数据库连接（惰性创建，请求结束自动关闭）。"""
    if 'db' not in g:
        g.db = connect(current_app.config['DATABASE'])
    return g.db


def close_db(e=None):
    """关闭请求级数据库连接。"""
    db = g.pop('db', None)
    if db is not None:
        db.close()
