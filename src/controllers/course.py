"""表示层控制器 —— 课程管理。"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers import login_required
from models.db import get_db
from services import course_service

bp = Blueprint('course', __name__, url_prefix='/courses')


@bp.route('/')
@login_required
def index():
    keyword = request.args.get('q', '').strip()
    courses = course_service.list_courses(get_db(), keyword or None)
    return render_template('courses.html', courses=courses, keyword=keyword)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            course_service.add_course(get_db(), request.form)
            flash('课程添加成功', 'success')
            return redirect(url_for('course.index'))
        except (ValueError, TypeError) as exc:
            flash(str(exc), 'error')
    return render_template('course_form.html', course=None)


@bp.route('/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def edit(course_id):
    course = course_service.get_course(get_db(), course_id)
    if course is None:
        flash('课程不存在', 'error')
        return redirect(url_for('course.index'))
    if request.method == 'POST':
        try:
            course_service.update_course(get_db(), course_id, request.form)
            flash('课程更新成功', 'success')
            return redirect(url_for('course.index'))
        except (ValueError, TypeError) as exc:
            flash(str(exc), 'error')
    return render_template('course_form.html', course=course)


@bp.route('/delete/<int:course_id>', methods=['POST'])
@login_required
def delete(course_id):
    course_service.delete_course(get_db(), course_id)
    flash('课程已删除', 'success')
    return redirect(url_for('course.index'))
