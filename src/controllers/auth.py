"""表示层控制器 —— 登录 / 登出。"""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.db import get_db
from services import auth_service

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        try:
            user = auth_service.authenticate(get_db(), username, password)
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('dashboard.index'))
        except auth_service.AuthError as exc:
            flash(str(exc), 'error')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('已退出登录', 'success')
    return redirect(url_for('auth.login'))
