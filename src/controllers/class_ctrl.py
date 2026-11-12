"""表示层控制器 —— 班级管理。"""
from flask import Blueprint, flash, redirect, render_template, request, url_for

from controllers import login_required
from models.db import get_db
from services import class_service

bp = Blueprint('class', __name__, url_prefix='/classes')


@bp.route('/')
@login_required
def index():
    classes = class_service.list_classes(get_db())
    return render_template('classes.html', classes=classes)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            class_service.add_class(get_db(), request.form)
            flash('班级添加成功', 'success')
            return redirect(url_for('class.index'))
        except ValueError as exc:
            flash(str(exc), 'error')
    return render_template('class_form.html', cls=None)


@bp.route('/edit/<int:class_id>', methods=['GET', 'POST'])
@login_required
def edit(class_id):
    cls = class_service.get_class(get_db(), class_id)
    if cls is None:
        flash('班级不存在', 'error')
        return redirect(url_for('class.index'))
    if request.method == 'POST':
        try:
            class_service.update_class(get_db(), class_id, request.form)
            flash('班级更新成功', 'success')
            return redirect(url_for('class.index'))
        except ValueError as exc:
            flash(str(exc), 'error')
    return render_template('class_form.html', cls=cls)


@bp.route('/delete/<int:class_id>', methods=['POST'])
@login_required
def delete(class_id):
    class_service.delete_class(get_db(), class_id)
    flash('班级已删除', 'success')
    return redirect(url_for('class.index'))
