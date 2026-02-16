#!/usr/bin/env python3
"""
论坛新帖摘要生成器
自动检查 OpenClaw 社区最近 24 小时的新帖，并为每个帖子生成摘要
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict

class ForumSummarizer:
    def __init__(self, base_url: str = "https://chiclaude.com"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_latest_topics(self, hours: int = 24) -> List[Dict]:
        """
        获取最近 N 小时的帖子列表

        Args:
            hours: 查询最近多少小时的帖子

        Returns:
            帖子列表
        """
        # 获取最新帖子
        url = f"{self.base_url}/latest.json"
        response = self.session.get(url)
        response.raise_for_status()

        data = response.json()
        topics = data.get('topic_list', {}).get('topics', [])

        # 过滤最近 N 小时的帖子
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_topics = []

        for topic in topics:
            created_at_str = topic.get('created_at')
            if created_at_str:
                created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                if created_at >= cutoff_time:
                    recent_topics.append(topic)

        return recent_topics

    def get_topic_details(self, topic_id: int) -> Dict:
        """
        获取帖子详情

        Args:
            topic_id: 帖子 ID

        Returns:
            帖子详情
        """
        url = f"{self.base_url}/t/{topic_id}.json"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def generate_summary(self, topic: Dict) -> str:
        """
        为帖子生成摘要

        Args:
            topic: 帖子信息

        Returns:
            摘要字符串
        """
        title = topic.get('title', '无标题')
        category = topic.get('category_name', '未知版块')
        excerpt = topic.get('excerpt', '').strip()

        # 如果有摘要就用摘要，否则用标题
        summary = excerpt if excerpt else title

        # 清理摘要，移除 HTML 标签和多余空白
        import re
        summary = re.sub(r'<[^>]+>', '', summary)
        summary = ' '.join(summary.split())

        # 限制长度
        if len(summary) > 100:
            summary = summary[:97] + '...'

        return f"[{category}] {summary}"

    def run(self, hours: int = 24):
        """
        运行摘要生成器

        Args:
            hours: 查询最近多少小时的帖子
        """
        print(f"📊 正在检查最近 {hours} 小时的新帖...\n")

        topics = self.get_latest_topics(hours)

        if not topics:
            print("❌ 没有找到新帖子")
            return

        print(f"✅ 找到 {len(topics)} 条新帖\n")
        print("=" * 60)
        print()

        for i, topic in enumerate(topics, 1):
            summary = self.generate_summary(topic)
            print(f"{i}. {summary}")

            # 可选：显示帖子链接
            slug = topic.get('slug', 'topic')
            topic_id = topic.get('id')
            print(f"   🔗 {self.base_url}/t/{slug}/{topic_id}")
            print()

        print("=" * 60)
        print(f"✨ 共 {len(topics)} 条新帖摘要生成完成！")


def main():
    """主函数"""
    summarizer = ForumSummarizer()

    # 可以通过命令行参数指定小时数
    import sys
    hours = 24
    if len(sys.argv) > 1:
        try:
            hours = int(sys.argv[1])
        except ValueError:
            print("⚠️  参数无效，使用默认值 24 小时")

    summarizer.run(hours)


if __name__ == "__main__":
    main()
