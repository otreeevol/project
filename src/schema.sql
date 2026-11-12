-- 学生信息管理系统 数据库结构定义
-- 表：user / class / student / course / grade

-- 用户表
CREATE TABLE IF NOT EXISTS user (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,          -- 用户名
    password_hash TEXT    NOT NULL,                 -- 密码哈希
    role          TEXT    NOT NULL DEFAULT 'admin', -- 角色：admin / teacher / student
    created_at    TEXT    DEFAULT (datetime('now', 'localtime'))
);

-- 班级表
CREATE TABLE IF NOT EXISTS class (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT NOT NULL,                     -- 班级名称
    major        TEXT,                              -- 专业
    grade        TEXT,                              -- 年级
    head_teacher TEXT                               -- 班主任
);

-- 学生表
CREATE TABLE IF NOT EXISTS student (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_no TEXT NOT NULL UNIQUE,                -- 学号
    name       TEXT NOT NULL,                       -- 姓名
    gender     TEXT,                                -- 性别
    birth_date TEXT,                                -- 出生日期
    class_id   INTEGER,                             -- 所属班级
    phone      TEXT,                                -- 联系电话
    email      TEXT,                                -- 邮箱
    FOREIGN KEY (class_id) REFERENCES class(id) ON DELETE SET NULL
);

-- 课程表
CREATE TABLE IF NOT EXISTS course (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    course_no TEXT NOT NULL UNIQUE,                 -- 课程编号
    name      TEXT NOT NULL,                        -- 课程名称
    credit    REAL,                                 -- 学分
    hours     INTEGER,                              -- 学时
    teacher   TEXT                                  -- 任课教师
);

-- 成绩表
CREATE TABLE IF NOT EXISTS grade (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,                    -- 学生
    course_id  INTEGER NOT NULL,                    -- 课程
    score      REAL,                                -- 成绩（0~100）
    semester   TEXT,                                -- 学期，如 2025-2026-1
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id)  REFERENCES course(id)  ON DELETE CASCADE,
    UNIQUE (student_id, course_id, semester)
);

-- 索引：加速按班级查学生、按学生/课程查成绩
CREATE INDEX IF NOT EXISTS idx_student_class ON student(class_id);
CREATE INDEX IF NOT EXISTS idx_grade_student ON grade(student_id);
CREATE INDEX IF NOT EXISTS idx_grade_course  ON grade(course_id);
