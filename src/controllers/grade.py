"""表示层控制器 —— 成绩管理。"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers import login_required
from models.db import get_db
from services import course_service, grade_service, student_service

bp = Blueprint('grade', __name__, url_prefix='/grades')


@bp.route('/')
@login_required
def index():
    student_id = request.args.get('student_id', type=int)
    course_id = request.args.get('course_id', type=int)
    grades = grade_service.list_grades(get_db(), student_id, course_id)
    students = student_service.list_students(get_db())
    courses = course_service.list_courses(get_db())
    return render_template(
        'grades.html', grades=grades, students=students, courses=courses,
        student_id=student_id, course_id=course_id,
    )


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            grade_service.add_grade(get_db(), request.form)
            flash('成绩录入成功', 'success')
            return redirect(url_for('grade.index'))
        except (ValueError, TypeError) as exc:
            flash(str(exc), 'error')
    students = student_service.list_students(get_db())
    courses = course_service.list_courses(get_db())
    return render_template('grade_form.html', grade=None, students=students, courses=courses)


@bp.route('/edit/<int:grade_id>', methods=['GET', 'POST'])
@login_required
def edit(grade_id):
    grade = grade_service.get_grade(get_db(), grade_id)
    if grade is None:
        flash('成绩记录不存在', 'error')
        return redirect(url_for('grade.index'))
    if request.method == 'POST':
        try:
            grade_service.update_grade(get_db(), grade_id, request.form)
            flash('成绩更新成功', 'success')
            return redirect(url_for('grade.index'))
        except (ValueError, TypeError) as exc:
            flash(str(exc), 'error')
    students = student_service.list_students(get_db())
    courses = course_service.list_courses(get_db())
    return render_template('grade_form.html', grade=grade, students=students, courses=courses)


@bp.route('/delete/<int:grade_id>', methods=['POST'])
@login_required
def delete(grade_id):
    grade_service.delete_grade(get_db(), grade_id)
    flash('成绩已删除', 'success')
    return redirect(url_for('grade.index'))


@bp.route('/statistics')
@login_required
def statistics():
    course_id = request.args.get('course_id', type=int)
    stats = grade_service.statistics(get_db(), course_id)
    courses = course_service.list_courses(get_db())
    return render_template('statistics.html', stats=stats, courses=courses, course_id=course_id)
