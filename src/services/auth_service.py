"""业务逻辑层 —— 用户认证。"""
from werkzeug.security import check_password_hash, generate_password_hash

from models import user_dao


class AuthError(Exception):
    """认证失败异常。"""


def authenticate(conn, username, password):
    """校验用户名密码，成功返回用户记录，失败抛出 AuthError。"""
    user = user_dao.get_by_username(conn, username)
    if user is None or not check_password_hash(user['password_hash'], password):
        raise AuthError("用户名或密码错误")
    return user


def create_user(conn, username, password, role='admin'):
    """新增用户，返回用户 id。"""
    if user_dao.get_by_username(conn, username):
        raise ValueError("用户名已存在")
    return user_dao.create(conn, username, generate_password_hash(password), role)
