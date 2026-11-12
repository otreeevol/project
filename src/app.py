"""学生信息管理系统 —— 应用入口。

组装三层架构：
- 表示层：controllers（路由）+ templates / static（视图）
- 业务逻辑层：services
- 数据访问层：models（DAO）
"""
from flask import Flask

from config import DATABASE, HOST, PORT, SECRET_KEY
from models import db


def create_app():
    app = Flask(__name__)
    app.config['DATABASE'] = DATABASE
    app.config['SECRET_KEY'] = SECRET_KEY
    app.teardown_appcontext(db.close_db)

    # 注册各模块路由（表示层控制器）
    from controllers import auth, course, dashboard, grade, student
    from controllers import class_ctrl

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(student.bp)
    app.register_blueprint(class_ctrl.bp)
    app.register_blueprint(course.bp)
    app.register_blueprint(grade.bp)

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
