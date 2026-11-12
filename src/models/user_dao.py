"""数据访问层 —— 用户表（user）的增删改查。"""


def get_by_username(conn, username):
    """按用户名查询用户。"""
    cur = conn.execute("SELECT * FROM user WHERE username = ?", (username,))
    return cur.fetchone()


def get_by_id(conn, user_id):
    """按主键查询用户。"""
    cur = conn.execute("SELECT * FROM user WHERE id = ?", (user_id,))
    return cur.fetchone()


def create(conn, username, password_hash, role='admin'):
    """新增用户。"""
    cur = conn.execute(
        "INSERT INTO user (username, password_hash, role) VALUES (?, ?, ?)",
        (username, password_hash, role),
    )
    conn.commit()
    return cur.lastrowid
