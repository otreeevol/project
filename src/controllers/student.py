"""表示层控制器 —— 学生信息管理。"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers import login_required
from models.db import get_db
from services import class_service, student_service

bp = Blueprint('student', __name__, url_prefix='/students')


@bp.route('/')
@login_required
def index():
    keyword = request.args.get('q', '').strip()
    students = student_service.list_students(get_db(), keyword or None)
    return render_template('students.html', students=students, keyword=keyword)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            student_service.add_student(get_db(), request.form)
            flash('学生添加成功', 'success')
            return redirect(url_for('student.index'))
        except (ValueError, TypeError) as exc:
            flash(str(exc), 'error')
    classes = class_service.list_classes(get_db())
    return render_template('student_form.html', student=None, classes=classes)


@bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit(student_id):
    student = student_service.get_student(get_db(), student_id)
    if student is None:
        flash('学生不存在', 'error')
        return redirect(url_for('student.index'))
    if request.method == 'POST':
        try:
            student_service.update_student(get_db(), student_id, request.form)
            flash('学生更新成功', 'success')
            return redirect(url_for('student.index'))
        except (ValueError, TypeError) as exc:
            flash(str(exc), 'error')
    classes = class_service.list_classes(get_db())
    return render_template('student_form.html', student=student, classes=classes)


@bp.route('/delete/<int:student_id>', methods=['POST'])
@login_required
def delete(student_id):
    student_service.delete_student(get_db(), student_id)
    flash('学生已删除', 'success')
    return redirect(url_for('student.index'))
