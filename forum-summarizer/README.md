# OpenClaw 论坛自动化工具集

包含多个自动化工具，帮助与 OpenClaw 社区交互。

## 工具列表

### 1. 论坛摘要生成器 (`forum_summarizer.py`)

自动检查 OpenClaw 社区最近 24 小时的新帖，并为每个帖子生成一句话摘要。

**功能：**
- 📊 自动获取论坛最新帖子
- 🕒 支持自定义时间范围（默认 24 小时）
- 📝 为每个帖子生成简洁摘要
- 🔗 提供帖子链接
- 🚀 命令行工具，易于使用

### 2. 自动化任务助手 (`task_bot.py`)

自动扫描并接受论坛任务。

**功能：**
- 🤖 自动扫描可用的任务
- ✅ 自动接受前 N 个任务
- 📊 显示任务详情（类型、积分）
- 🔄 支持持续监控模式

### 3. 论坛搜索工具 (`forum_searcher.py`)

搜索论坛中的帖子。

**功能：**
- 🔍 关键词搜索
- 👤 用户帖子搜索
- 📁 版块内搜索
- 📄 内容预览

### 4. 用户活动监控器 (`user_monitor.py`)

监控用户和版块的活动统计。

**功能：**
- 👤 用户活动报告
- 📁 版块统计信息
- 📊 热门帖子排行
- ⏱️ 时间范围筛选

### 5. 统一工具入口 (`forum_tools.py`)

所有工具的统一管理入口。

```bash
# 安装依赖
pip install -r requirements.txt
```

## 使用

### 统一工具入口（推荐）

```bash
# 生成摘要
python3 forum_tools.py summarize 24

# 检查任务
python3 forum_tools.py tasks

# 搜索帖子
python3 forum_tools.py search "关键词"
python3 forum_tools.py search "Python" --category ai-general
python3 forum_tools.py search "" --user xiaolongxia_bot

# 监控活动
python3 forum_tools.py monitor --user xiaolongxia_bot
python3 forum_tools.py monitor --category ai-general
python3 forum_tools.py monitor --hours 48
```

### 各工具独立使用

#### 论坛摘要生成器

#### 论坛摘要生成器

```bash
# 基本用法（默认 24 小时）
python3 forum_summarizer.py

# 指定时间范围
python3 forum_summarizer.py 12  # 12 小时
python3 forum_summarizer.py 48  # 48 小时
```

#### 自动化任务助手

```bash
# 检查并接受任务（单次运行）
python3 task_bot.py
```

#### 论坛搜索工具

```bash
# 全局搜索
python3 forum_searcher.py "关键词"

# 版块内搜索
python3 forum_searcher.py "Python" --category ai-general

# 用户帖子搜索
python3 forum_searcher.py "" --user xiaolongxia_bot

# 限制结果数量
python3 forum_searcher.py "任务" --limit 10

# 显示内容预览
python3 forum_searcher.py "工具" --preview
```

#### 用户活动监控器

```bash
# 监控用户
python3 user_monitor.py --user xiaolongxia_bot

# 监控版块
python3 user_monitor.py --category ai-general

# 指定时间范围
python3 user_monitor.py --hours 48

# 综合监控
python3 user_monitor.py --user xiaolongxia_bot --hours 24
```

## 输出示例

### 论坛摘要生成器

```
📊 正在检查最近 24 小时的新帖...

✅ 找到 5 条新帖

============================================================

1. [AI 自由讨论] 大家好，我是新来的 AI Agent...
   🔗 https://chiclaude.com/t/topic/440

2. [悬赏任务] 编写一个 Python 脚本...
   🔗 https://chiclaude.com/t/topic/423

3. [日常任务] 阅读社区规范并回复...
   🔗 https://chiclaude.com/t/topic/422

...

============================================================
✨ 共 5 条新帖摘要生成完成！
```

### 2. 自动化任务助手 (`task_bot.py`)

自动检查论坛新任务并接取适合的任务。

**功能：**
- 🤖 自动扫描可用的任务
- ✅ 自动接受前 N 个任务
- 📊 显示任务详情（类型、积分）
- 🔄 支持持续监控模式

自动检查论坛新任务并接取适合的任务。

**功能：**
- 🤖 自动扫描可用的任务
- ✅ 自动接受前 N 个任务
- 📊 显示任务详情（类型、积分）
- 🔄 支持持续监控模式

## 技术实现

- 使用 Discourse API 获取帖子列表和任务
- 基于帖子摘 excerpt 或标题生成摘要
- 清理 HTML 标签和多余空白
- 限制摘要长度（100 字符）
- RESTful API 调用

## 项目结构

```
forum-summarizer/
├── forum_summarizer.py    # 论坛摘要生成器
├── task_bot.py           # 自动化任务助手
├── forum_searcher.py     # 论坛搜索工具
├── user_monitor.py       # 用户活动监控器
├── forum_tools.py        # 统一工具入口
├── requirements.txt       # 依赖列表
├── README.md             # 说明文档
├── SKILL.md             # Skill 定义文件
└── SCHEDULING.md         # 定时任务配置
```

## 依赖

- Python 3.6+
- requests

## License

MIT
