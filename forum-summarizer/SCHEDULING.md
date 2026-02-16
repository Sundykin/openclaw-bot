# OpenClaw 论坛自动化工具 - 定时任务配置示例

## Cron 任务示例

### 每 10 分钟检查一次新任务

```bash
# 编辑 crontab
crontab -e

# 添加以下行
*/10 * * * * cd /path/to/forum-summarizer && /usr/bin/python3 task_bot.py >> /var/log/forum-bot.log 2>&1
```

### 每天 8:00 生成论坛摘要（最近 24 小时）

```bash
# 编辑 crontab
crontab -e

# 添加以下行
0 8 * * * cd /path/to/forum-summarizer && /usr/bin/python3 forum_summarizer.py 24 >> /var/log/forum-summary.log 2>&1
```

### 每小时检查一次新任务并生成摘要

```bash
0 * * * * cd /path/to/forum-summarizer && /usr/bin/python3 task_bot.py >> /var/log/forum-bot.log 2>&1
5 * * * * cd /path/to/forum-summarizer && /usr/bin/python3 forum_summarizer.py 1 >> /var/log/forum-summary.log 2>&1
```

## Systemd 服务配置

### 创建服务文件

创建 `/etc/systemd/system/forum-bot.service`：

```ini
[Unit]
Description=OpenClaw Forum Automation Bot
After=network.target

[Service]
Type=oneshot
User=your-username
WorkingDirectory=/path/to/forum-summarizer
ExecStart=/usr/bin/python3 task_bot.py
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### 创建定时器

创建 `/etc/systemd/system/forum-bot.timer`：

```ini
[Unit]
Description=Run forum bot every 15 minutes

[Timer]
OnBootSec=15min
OnUnitActiveSec=15min
AccuracySec=1s

[Install]
WantedBy=timers.target
```

### 启用和启动服务

```bash
# 重载 systemd 配置
sudo systemctl daemon-reload

# 启用定时器
sudo systemctl enable forum-bot.timer

# 启动定时器
sudo systemctl start forum-bot.timer

# 查看定时器状态
sudo systemctl status forum-bot.timer

# 查看日志
sudo journalctl -u forum-bot -f
```

## Docker 定时任务（可选）

如果使用 Docker，可以结合 cron：

```dockerfile
# Dockerfile 示例
FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

# 安装 cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# 添加 cron 任务
RUN echo "*/10 * * * * cd /app && python3 task_bot.py >> /var/log/bot.log 2>&1" | crontab -

# 启动 cron
CMD cron -f
```

## 日志管理

### 日志轮转配置

创建 `/etc/logrotate.d/forum-bot`：

```
/var/log/forum-bot.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0644 your-username your-username
}
```

## 注意事项

1. **绝对路径**：在 cron 中使用绝对路径
2. **环境变量**：cron 环境与用户 shell 不同，注意环境变量
3. **权限问题**：确保运行用户有读写权限
4. **日志路径**：确保日志目录存在且有写权限
5. **Python 路径**：使用 `which python3` 确认 Python 路径

## 测试定时任务

```bash
# 测试命令是否能正常运行
cd /path/to/forum-summarizer && python3 task_bot.py

# 手动触发 cron 任务（测试用）
# 编辑 crontab，临时设置为当前时间后 1 分钟
# 等待 1 分钟，检查日志

# 查看系统日志
tail -f /var/log/forum-bot.log
```
