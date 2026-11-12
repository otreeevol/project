# 小米便签（MiCode Notes）信息管理系统

> 软件工程与方法学课程后实践 —— 软件工程项目实践

本仓库为《软件工程与方法学》课程的课后实践作业，以一个真实的开源软件 **小米便签（MiCode Notes）** 为载体，完整地走完软件工程生命周期：需求分析 → 总体设计 → 详细设计 → 编码实现 → 测试 → 部署 → 项目管理与质量保障，产出全套软件工程文档、UML 模型与可运行源码。

---

## 一、项目简介

- **软件名称**：小米便签（MiCode Notes）便签信息管理系统
- **项目背景**：小米便签是小米 MIUI 团队发起并贡献第一批代码的开源 Android 便签应用（Apache License 2.0），由 MiCode 开源社区（www.micode.net）维护。本实践以其作为研究对象，对其进行需求分析、架构设计与文档化。
- **主要用户**：需要随手记录、管理文字便签与通话记录的 Android 手机用户。
- **核心功能**：便签的新建 / 编辑 / 删除 / 查找、文件夹管理、闹钟提醒、桌面小组件、录音与图片附件、Google 任务同步等。
- **运行平台**：Android 4.0（API 14）及以上。
- **开发环境**：Java + Android SDK + SQLite。

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
│   └── diagrams/                     # UML 图（PlantUML 源文件）
│       ├── usecase.puml              # 用例图
│       ├── package.puml              # 包图
│       ├── component.puml            # 构件图
│       ├── deployment.puml           # 部署图
│       ├── class.puml                # 类图
│       ├── sequence-*.puml           # 顺序图
│       ├── state.puml                # 状态图
│       └── activity-*.puml           # 活动图
└── notes/                            # 小米便签（MiCode Notes）Android 源码
    ├── AndroidManifest.xml
    ├── src/net/micode/notes/         # Java 源码
    │   ├── data/                     # 数据层（ContentProvider、SQLite）
    │   ├── model/                    # 模型层
    │   ├── ui/                       # 表示层（Activity、Adapter）
    │   ├── tool/                     # 工具层
    │   ├── gtask/                    # Google 任务同步
    │   └── widget/                   # 桌面小组件
    └── res/                          # 资源文件
```

---

## 三、软件工程交付物清单

| 阶段 | 交付物 | 位置 |
| --- | --- | --- |
| 概述 | 项目简介、团队分工 | `docs/02` |
| 需求分析 | 需求规格说明书（SRS）、用例图、顺序图、状态图 | `docs/02` |
| 总体设计 | 总体设计方案、包图、构件图、部署图 | `docs/03` |
| 详细设计 | 设计规格说明书（SDS）、类图、顺序图、活动图 | `docs/04` |
| 编码实现 | 小米便签源码（开源重用） | `notes/` |
| 测试 | 测试计划、测试用例、测试报告 | `docs/05` |
| 部署 | 实例部署图、部署说明 | `docs/06` |
| 项目管理 | Git 版本控制、ISSUE 任务分配 | 本仓库 / `docs/06` |

---

## 四、技术选型

| 层次 | 技术 |
| --- | --- |
| 表示层 | Android Activity / Adapter / Widget（Java） |
| 业务逻辑层 | Java（model、tool 包） |
| 数据访问层 | SQLite + ContentProvider（NotesProvider） |
| 外部接口 | Google Task 同步（gtask）、系统联系人、闹钟、桌面小部件 |
| 构建工具 | Ant / Gradle（Android SDK） |
| 开源许可 | Apache License 2.0 |

---

## 五、如何运行

1. 使用 Android Studio（或 Eclipse + ADT）导入 `notes/` 目录。
2. 配置 Android SDK（minSdkVersion 14）。
3. 编译并安装到 Android 设备或模拟器。
4. 运行 `net.micode.notes.ui.NotesListActivity`（应用入口）。

> 注：本项目源码来源于 MiCode 开源社区，遵循 Apache License 2.0，详见 `notes/NOTICE` 与 `notes/README`。
