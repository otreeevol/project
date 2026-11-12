# 学生信息管理系统（Student Information Management System）

> 软件工程与方法学课程后实践 —— 软件工程项目实践

本仓库为《软件工程与方法学》课程的课后实践作业，从零开发一个 **学生信息管理系统**，完整走完软件工程生命周期：需求分析 → 总体设计 → 详细设计 → 编码实现 → 测试 → 部署 → 项目管理，产出全套软件工程文档、UML 模型与可运行源码。

---

## 一、项目简介

- **软件名称**：学生信息管理系统（Student Information Management System，简称 SMS）
- **项目背景**：面向学校教务部门、教师与学生的信息化管理需求，提供学生、班级、课程、成绩的统一管理与统计。
- **主要用户**：教务管理员、教师。
- **核心功能**：用户登录、学生/班级/课程信息管理、成绩录入与统计。
- **运行平台**：Windows / Linux（Python 3.8+）+ 现代浏览器。
- **技术栈**：Python Flask + SQLite + HTML/CSS/JavaScript，三层架构。

---

## 二、仓库结构

```
project/
├── README.md                         # 项目总览（本文件）
├── docs/                             # 全部软件工程文档
│   ├── 01-课程学习总结.md             # 一、课程学习总结
│   ├── 02-软件需求规格说明书.md        # 二、需求分析（SRS）
│   ├── 03-软件总体设计方案.md          # 三、体系结构设计（总体设计）
│   ├── 04-软件设计规格说明书.md        # 四、详细设计（SDS）
│   ├── 05-软件测试报告.md              # 六、测试
│   ├── 06-部署与项目管理.md            # 七、部署 + 八、项目管理
│   └── diagrams/                     # UML 图（PlantUML 源文件 + PNG 图片）
└── src/                              # 系统源码（三层架构）
    ├── app.py                        # 应用入口
    ├── config.py                     # 配置
    ├── init_db.py                    # 数据库初始化脚本
    ├── schema.sql                    # 数据库表结构
    ├── requirements.txt              # 依赖清单
    ├── controllers/                  # 表示层：路由控制器
    ├── services/                     # 业务逻辑层
    ├── models/                       # 数据访问层（DAO）
    ├── templates/                    # 表示层：HTML 模板
    ├── static/                       # 表示层：CSS/JS
    └── tests/                        # 单元测试 / 集成测试
```

---

## 三、软件工程交付物清单

| 阶段 | 交付物 | 位置 |
| --- | --- | --- |
| 概述 | 项目简介、团队分工 | `docs/02`、`docs/06` |
| 需求分析 | 需求规格说明书（SRS）、用例图、顺序图、状态图 | `docs/02` |
| 总体设计 | 总体设计方案、包图、构件图、部署图 | `docs/03` |
| 详细设计 | 设计规格说明书（SDS）、类图、顺序图、活动图 | `docs/04` |
| 编码实现 | Flask 三层架构源码 | `src/` |
| 测试 | 测试计划、测试用例、测试报告 | `docs/05`、`src/tests/` |
| 部署 | 实例部署图、部署说明 | `docs/06` |
| 项目管理 | Git 版本控制、ISSUE 任务分配 | 本仓库 / `docs/06` |

---

## 四、技术选型

| 层次 | 技术 |
| --- | --- |
| 前端/表示层 | HTML5 + CSS3 + JavaScript + Jinja2 模板 |
| 后端/业务逻辑 | Python 3.8+ / Flask |
| 数据库 | SQLite（可替换为 MySQL） |
| 数据访问 | sqlite3 标准库 + DAO 封装 |
| 会话/安全 | Werkzeug 密码哈希 + Flask session |
| 运行平台 | Windows / Linux + 现代浏览器 |

---

## 五、快速开始

```bash
# 1. 安装依赖
pip install -r src/requirements.txt

# 2. 初始化数据库（建表 + 默认账号 + 示例数据）
cd src
python init_db.py

# 3. 启动应用
python app.py
# 浏览器访问 http://127.0.0.1:5000
```

**默认账号**：`admin` / `admin123`

## 六、运行测试

```bash
cd src
python -m unittest discover -s tests -v
```

> 实测 19 个单元/集成测试用例全部通过。
