"""表示层控制器（路由）包 —— 接收 HTTP 请求、调用业务逻辑层、返回视图。"""
from functools import wraps

from flask import flash, redirect, session, url_for


def login_required(view):
    """登录校验装饰器：未登录用户重定向到登录页。"""
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'error')
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped
