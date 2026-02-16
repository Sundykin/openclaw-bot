# 论坛新帖摘要生成器

自动检查 OpenClaw 社区最近 24 小时的新帖，并为每个帖子生成一句话摘要。

## 功能

- 📊 自动获取论坛最新帖子
- 🕒 支持自定义时间范围（默认 24 小时）
- 📝 为每个帖子生成简洁摘要
- 🔗 提供帖子链接
- 🚀 命令行工具，易于使用

## 安装

```bash
# 安装依赖
pip install -r requirements.txt
```

## 使用

### 基本用法（默认 24 小时）

```bash
python forum_summarizer.py
```

### 指定时间范围

```bash
# 检查最近 12 小时
python forum_summarizer.py 12

# 检查最近 48 小时
python forum_summarizer.py 48
```

## 输出示例

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

## 技术实现

- 使用 Discourse API 获取帖子列表
- 基于帖子摘 excerpt 或标题生成摘要
- 清理 HTML 标签和多余空白
- 限制摘要长度（100 字符）

## 项目结构

```
forum-summarizer/
├── forum_summarizer.py    # 主程序
├── requirements.txt       # 依赖列表
└── README.md             # 说明文档
```

## 依赖

- Python 3.6+
- requests

## License

MIT
