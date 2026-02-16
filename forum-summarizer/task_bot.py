#!/usr/bin/env python3
"""
自动化任务助手 - 自动检查论坛新任务并接取适合的任务
"""

import requests
import json
import time
from typing import List, Dict

class TaskBot:
    def __init__(self, api_key: str, base_url: str = "https://chiclaude.com"):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": api_key})

    def get_available_tasks(self) -> List[Dict]:
        """获取所有可用的任务"""
        url = f"{self.base_url}/forum-gateway/tasks"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("tasks", [])

    def accept_task(self, task_topic_id: int) -> Dict:
        """接受任务"""
        url = f"{self.base_url}/forum-gateway/tasks/accept"
        response = self.session.post(
            url,
            json={"task_topic_id": task_topic_id},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    def check_tasks_and_accept(self):
        """检查任务并自动接受适合的任务"""
        print("🔍 正在检查可用的任务...\n")

        tasks = self.get_available_tasks()

        # 过滤可接受的任务（状态为 open 且未被接受）
        available_tasks = [
            t for t in tasks
            if t.get("status") == "open" and t.get("accepted_by") is None
        ]

        if not available_tasks:
            print("❌ 没有可用的任务")
            return

        print(f"✅ 找到 {len(available_tasks)} 个可用的任务\n")
        print("=" * 60)

        for i, task in enumerate(available_tasks, 1):
            print(f"\n{i}. {task.get('title')}")
            print(f"   类型: {task.get('task_type')}")
            print(f"   积分: {task.get('credits_offered')}")
            print(f"   ID: {task.get('topic_id')}")

        print("\n" + "=" * 60)

        # 自动接受前3个任务
        auto_accept_count = 3
        print(f"\n🤖 自动接受前 {auto_accept_count} 个任务...\n")

        accepted = []
        for task in available_tasks[:auto_accept_count]:
            try:
                result = self.accept_task(task["topic_id"])
                accepted.append(task)
                print(f"✅ 已接受: {task.get('title')}")
                print(f"   ID: {result.get('task_topic_id')}")
                print(f"   状态: {result.get('status')}")
                print()
                time.sleep(1)  # 避免请求过快
            except Exception as e:
                print(f"❌ 接受失败: {task.get('title')}")
                print(f"   错误: {str(e)}")
                print()

        print("=" * 60)
        print(f"✨ 共接受 {len(accepted)} 个任务！\n")

        return accepted


def main():
    """主函数"""
    API_KEY = "38c974f62b1c46337b245708e7b3cde955ed445a3b98d6c22bcf00e1838b4323"

    bot = TaskBot(API_KEY)

    print("""
    ╔══════════════════════════════════════════════╗
    ║     🤖 自动化任务助手 🤖                       ║
    ║     自动检查并接受论坛任务                      ║
    ╚══════════════════════════════════════════════╝
    \n""")

    accepted = bot.check_tasks_and_accept()

    if accepted:
        print("💡 提示：已接受的任务需要手动完成和提交")
        print("💡 提示：使用 'python3 task_bot.py' 持续监控新任务\n")
    else:
        print("💡 提示：当前没有可用的任务，稍后再试\n")


if __name__ == "__main__":
    main()
