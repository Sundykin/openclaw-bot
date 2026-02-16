#!/usr/bin/env python3
"""
用户活动监控器 - 监控特定用户或版块的活动
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict

class UserMonitor:
    def __init__(self, base_url: str = "https://chiclaude.com"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_user_activity(self, username: str, days: int = 7) -> Dict:
        """
        获取用户最近的活动

        Args:
            username: 用户名
            days: 查询最近几天的活动

        Returns:
            用户活动信息
        """
        # 获取用户信息
        url = f"{self.base_url}/u/{username}.json"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()

        user = data.get('user', {})
        activity = user.get('user_summary', {})

        # 统计信息
        stats = {
            'username': username,
            'created_at': user.get('created_at'),
            'likes_given': activity.get('likes_given', 0),
            'likes_received': activity.get('likes_received', 0),
            'posts_count': activity.get('post_count', 0),
            'topics_entered': activity.get('topics_entered', 0),
            'posts_read': activity.get('posts_read', 0),
            'days_visited_in_last_30_days': activity.get('days_visited', 0)
        }

        return stats

    def get_category_stats(self, category_id: int) -> Dict:
        """
        获取版块统计信息

        Args:
            category_id: 版块 ID

        Returns:
            版块统计信息
        """
        url = f"{self.base_url}/c/{category_id}.json"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()

        category = data.get('category', {})
        users = data.get('users', [])

        stats = {
            'id': category.get('id'),
            'name': category.get('name'),
            'slug': category.get('slug'),
            'topic_count': category.get('topic_count', 0),
            'post_count': category.get('post_count', 0),
            'user_count': len(users),
            'description': category.get('description_text', '')
        }

        return stats

    def get_recent_topics(self, category_slug: str = None, hours: int = 24) -> List[Dict]:
        """
        获取最近的帖子

        Args:
            category_slug: 版块 slug（可选，None 表示所有版块）
            hours: 查询最近几小时的帖子

        Returns:
            帖子列表
        """
        url = f"{self.base_url}/latest.json"
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()

        topics = data.get('topic_list', {}).get('topics', [])

        # 时间过滤
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        recent_topics = []

        for topic in topics:
            created_at_str = topic.get('created_at')
            if created_at_str:
                created_at = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                if created_at >= cutoff_time:
                    # 版块过滤
                    if category_slug is None or topic.get('category_slug') == category_slug:
                        recent_topics.append({
                            'id': topic.get('id'),
                            'title': topic.get('title'),
                            'slug': topic.get('slug'),
                            'category': topic.get('category_name'),
                            'category_slug': topic.get('category_slug'),
                            'created_at': created_at_str,
                            'views': topic.get('views'),
                            'like_count': topic.get('like_count'),
                            'post_count': topic.get('post_count')
                        })

        return recent_topics

    def generate_report(self, username: str = None, category_slug: str = None, hours: int = 24):
        """
        生成活动报告

        Args:
            username: 监控的用户名（可选）
            category_slug: 监控的版块（可选）
            hours: 时间范围
        """
        print("📊 生成活动报告\n")
        print("=" * 60)

        # 用户报告
        if username:
            print(f"\n👤 用户报告: @{username}\n")
            try:
                user_stats = self.get_user_activity(username)
                print(f"   创建时间: {user_stats.get('created_at', 'N/A')}")
                print(f"   发帖数: {user_stats.get('posts_count', 0)}")
                print(f"   点赞数: {user_stats.get('likes_given', 0)}")
                print(f"   获赞数: {user_stats.get('likes_received', 0)}")
                print(f"   阅读帖数: {user_stats.get('posts_read', 0)}")
                print(f"   访问天数: {user_stats.get('days_visited_in_last_30_days', 0)}/30")
            except Exception as e:
                print(f"   ❌ 获取用户信息失败: {str(e)}")

        # 版块报告
        if category_slug:
            print(f"\n📁 版块报告: #{category_slug}\n")
            try:
                topics = self.get_recent_topics(category_slug, hours)
                print(f"   最近 {hours} 小时的帖子数: {len(topics)}")

                if topics:
                    print("\n   最新帖子:")
                    for i, topic in enumerate(topics[:5], 1):
                        print(f"   {i}. {topic.get('title')}")
                        print(f"      浏览: {topic.get('views')} | 点赞: {topic.get('like_count')}")
            except Exception as e:
                print(f"   ❌ 获取版块信息失败: {str(e)}")

        # 总体报告
        print(f"\n🌐 最近 {hours} 小时的总体活动\n")
        try:
            all_topics = self.get_recent_topics(hours=hours)

            # 按版块统计
            category_stats = {}
            for topic in all_topics:
                cat = topic.get('category', '未知')
                category_stats[cat] = category_stats.get(cat, 0) + 1

            print(f"   总帖子数: {len(all_topics)}")
            print(f"\n   版块分布:")
            for cat, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {cat}: {count}")

            if all_topics:
                print("\n   热门帖子（浏览量排行）:")
                hot_topics = sorted(all_topics, key=lambda x: x.get('views', 0), reverse=True)[:5]
                for i, topic in enumerate(hot_topics, 1):
                    print(f"   {i}. {topic.get('title')}")
                    print(f"      浏览: {topic.get('views')} | 点赞: {topic.get('like_count')}")

        except Exception as e:
            print(f"   ❌ 获取总体信息失败: {str(e)}")

        print("\n" + "=" * 60)


def main():
    """主函数"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='用户活动监控器')
    parser.add_argument('--user', help='监控的用户名')
    parser.add_argument('--category', help='监控的版块 slug')
    parser.add_argument('--hours', type=int, default=24, help='时间范围（小时）')

    args = parser.parse_args()

    monitor = UserMonitor()

    print("""
    ╔════════════════════════════════════════════╗
    ║     📊 用户活动监控器 📊                     ║
    ║     监控用户和版块的活动统计               ║
    ╚════════════════════════════════════════════╝
    \n""")

    try:
        monitor.generate_report(
            username=args.user,
            category_slug=args.category,
            hours=args.hours
        )
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
