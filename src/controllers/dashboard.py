"""表示层控制器 —— 首页 / 仪表盘。"""
from flask import Blueprint, render_template

from controllers import login_required
from models.db import get_db

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@login_required
def index():
    db = get_db()
    counts = {
        'students': db.execute("SELECT COUNT(*) AS c FROM student").fetchone()['c'],
        'classes': db.execute("SELECT COUNT(*) AS c FROM class").fetchone()['c'],
        'courses': db.execute("SELECT COUNT(*) AS c FROM course").fetchone()['c'],
        'grades': db.execute("SELECT COUNT(*) AS c FROM grade").fetchone()['c'],
    }
    return render_template('dashboard.html', counts=counts)
