# Luke's Wiki

> 个人知识库，基于 MkDocs + Simple Blog 主题构建的现代化静态文档网站。

[![GitHub Stars](https://img.shields.io/github/stars/fomalhaut-m/wike.svg?style=flat-square)](https://github.com/fomalhaut-m/wike)
[![GitHub Issues](https://img.shields.io/github/issues/fomalhaut-m/wike.svg?style=flat-square)](https://github.com/fomalhaut-m/wike/issues)
[![GitHub License](https://img.shields.io/github/license/fomalhaut-m/wike.svg?style=flat-square)](https://github.com/fomalhaut-m/wike/blob/main/LICENSE)
[![Deploy Status](https://img.shields.io/github/actions/workflow/status/fomalhaut-m/wike/deploy-aliyun-oss.yml?style=flat-square)](https://github.com/fomalhaut-m/wike/actions)

---

## 🌟 功能特性

| 功能 | 说明 |
|------|------|
| ✅ **自动更新日志** | 提交代码时自动生成智能更新日志 |
| ✅ **PDF 支持** | 支持 PDF 文档在线预览和下载 |
| ✅ **CI/CD 部署** | GitHub Actions 自动部署到阿里云 OSS |
| ✅ **AI 辅助** | 使用 Minimax AI 生成智能日志描述 |
| ✅ **响应式设计** | Material 主题，支持深色/浅色模式 |
| ✅ **全文搜索** | 内置搜索功能，支持中文分词 |

---

## 🛠️ 技术栈

| 分类 | 组件 | 版本 |
|------|------|------|
| **文档框架** | MkDocs | 1.6+ |
| **主题** | MkDocs Simple Blog | 0.4.1+ |
| **部署** | 阿里云 ECS | - |
| **CI/CD** | GitHub Actions | - |
| **AI 服务** | Minimax API | - |

---

## 📁 项目结构

```
wike/                              # 项目根目录
├── .github/                       # GitHub 配置
│   └── workflows/                 # GitHub Actions 工作流
│       └── deploy-aliyun-oss.yml  # 阿里云 OSS 部署配置
├── .trae/                         # Trae IDE 配置
│   └── rules/                     # 项目规则
├── docs/                          # 文档源文件 (Markdown)
│   ├── 3D建模/                    # 3D建模相关
│   ├── 产品经理/                  # 产品经理知识体系
│   ├── 数据库/                    # 数据库知识
│   ├── 软件/                      # 软件技术文档
│   ├── 运维技术/                  # 运维技术
│   ├── 阅读/                      # 阅读笔记
│   ├── 项目管理/                  # 项目管理 (PMP/ACP)
│   └── log/                       # 自动更新日志
├── public/                        # 静态资源 (图片、PDF等)
├── scripts/                       # 构建和自动化脚本
│   └── push-with-log.sh           # 推送并更新日志脚本
├── site/                          # 生成的静态网站 (自动生成)
├── .gitconfig                     # Git 配置
├── .gitignore                     # Git 忽略配置
├── README.md                      # 项目说明文档
├── mkdocs.yml                     # MkDocs 核心配置文件
└── mkdocs.yml.md                  # MkDocs 配置指南
```

---

## 🚀 快速开始

### 前置条件

- Python 3.12.9
- Git

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/fomalhaut-m/wike.git
cd wike

# 2. 安装 python3-venv (Ubuntu/Debian)
sudo apt install python3-venv

# 3. 创建虚拟环境
python3 -m venv venv

# 4. 激活虚拟环境
source venv/bin/activate

# 5. 安装 mkdocs 依赖
python -m pip install -r requirements.txt

# 6. 启动开发服务器
python -m mkdocs serve
```

> **提示**: 如果遇到 `externally-managed-environment` 错误，说明系统启用了 Python 环境保护机制，
> 请使用虚拟环境方式安装（推荐），或使用 `pip install --break-system-packages`（不推荐）。

### 常用命令

| 命令 | 说明 |
|------|------|
| `python -m mkdocs serve` | 启动本地开发服务器 (http://localhost:8000) |
| `mkdocs build` | 构建静态站点到 site/ 目录 |
| `mkdocs gh-deploy` | 部署到 GitHub Pages |
| `bash scripts/push-with-log.sh` | 推送代码并自动更新日志 |

---

## 📚 内容分类

| 分类 | 说明 | 状态 |
|------|------|------|
| 博客与阅读 | Blog、读书笔记与个人思考 | 📖 |
| 学习与职业 | 产品经理、项目管理与提示词工程 | 📖 |
| 工程技术 | 软件、数据库、运维与嵌入式 | 📖 |
| 创意设计 | Blender、AE 与视觉创作 | 📖 |
| 内容创作 | 小说创作体系与个人作品 | 📖 |

---

## 📝 自动更新日志

### 工作原理

项目使用 `scripts/push-with-log.sh` 脚本自动生成更新日志：

1. **检测变更**：检查工作目录和未推送提交
2. **AI 生成**：调用 Minimax API 生成智能描述
3. **更新日志**：写入 `docs/log/index.md`
4. **自动提交**：将日志变更提交并推送

### 日志格式

```log
2026-05-10 15:30: 新增用户登录功能文档
2026-05-10 14:20: 修复页面加载bug
2026-05-10 10:15: 更新文档内容
```

### 配置 AI API

```bash
# 设置 Minimax API Key
export MINIMAX_API_KEY=your_api_key_here

# 执行推送脚本
bash scripts/push-with-log.sh
```

---

## 🚢 部署流程

### GitHub Actions 自动部署

项目已配置自动部署工作流：

1. **触发条件**：推送到 `main` 分支或手动触发
2. **构建步骤**：使用 MkDocs 构建静态站点
3. **部署目标**：阿里云 OSS

### 配置 Secrets

在 GitHub 仓库设置中添加以下 Secrets：

| Secret 名称 | 说明 |
|-------------|------|
| `ALIYUN_ACCESS_KEY_ID` | 阿里云 Access Key ID |
| `ALIYUN_ACCESS_KEY_SECRET` | 阿里云 Access Key Secret |

---

## 📋 脚本说明

项目使用 Python 脚本进行自动化操作，位于 `scripts/` 目录：

| 脚本 | 说明 |
|------|------|
| `git-commit.py` | AI 生成 Git Commit 消息并提交 |
| `push_with_log.py` | 推送代码并自动生成更新日志 |
| `call_minimax_api.py` | 调用 Minimax API 的公共模块 |

### 前置条件

```bash
# 需要安装 Python 3
python --version

# 需要设置 MINIMAX_API_KEY 环境变量
export MINIMAX_API_KEY=your_api_key_here
```

### 使用方法

#### 1. AI 生成 Commit 消息

```bash
python scripts/git-commit.py
```

工作流程：
1. 检测 git 变更
2. 调用 AI 生成简洁的 commit 消息
3. 自动执行 `git add .` 和 `git commit`

#### 2. 推送代码并更新日志

```bash
python scripts/push_with_log.py
```

工作流程：
1. 检测未推送的提交
2. 调用 AI 生成简短的更新日志
3. 写入 `docs/log/index.md`
4. 自动提交并推送到远程

### 合并操作（推荐）

一次性完成 commit 和 push：

```bash
python scripts/git-commit.py && python scripts/push_with_log.py
```

或者分开执行：

```bash
# 1. 先提交代码
python scripts/git-commit.py

# 2. 再推送并更新日志
python scripts/push_with_log.py
```

### 配置 API Key

如果没有设置环境变量，脚本会报错退出。建议将 API Key 添加到 shell 配置文件中：

```bash
# ~/.bashrc 或 ~/.zshrc
export MINIMAX_API_KEY="your_api_key_here"
```

---

## 🎣 Git Hooks

如需使用 Git Hooks，执行以下命令：

```bash
git config core.hooksPath .githooks
```

---

## 📊 统计信息

| 指标 | 数值 |
|------|------|
| 文档数量 | ~200+ |
| 代码行数 | ~50K+ |
| 提交次数 | ~500+ |

---

## 🔗 参考链接

| 资源 | 链接 |
|------|------|
| MkDocs 官网 | https://www.mkdocs.org/ |
| Material 主题 | https://squidfunk.github.io/mkdocs-material/ |
| MkDocs 中文文档 | https://mkdocs.pythonlang.cn/ |
| Minimax API | https://api.minimax.chat/ |
| mkdocs-nav-weight | https://github.com/shu307/mkdocs-nav-weight/blob/main/README_CN.md | 
| 阿里云 OSS | https://www.aliyun.com/product/oss |


---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

*Built with ❤️ using MkDocs & Simple Blog Theme*