#!/usr/bin/env python3
"""
论坛帖子搜索工具 - 搜索论坛中的特定帖子
"""

import requests
import json
from typing import List, Dict
import re

class ForumSearcher:
    def __init__(self, base_url: str = "https://chiclaude.com"):
        self.base_url = base_url
        self.session = requests.Session()

    def search_posts(self, query: str, limit: int = 20) -> List[Dict]:
        """
        搜索帖子

        Args:
            query: 搜索关键词
            limit: 返回结果数量限制

        Returns:
            帖子列表
        """
        url = f"{self.base_url}/search.json"
        params = {
            "q": query,
            "per_page": limit
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        topics = data.get('topics', [])
        posts = data.get('posts', [])

        results = []

        # 添加话题结果
        for topic in topics:
            results.append({
                'type': 'topic',
                'id': topic.get('id'),
                'title': topic.get('title'),
                'slug': topic.get('slug'),
                'category': topic.get('category_name'),
                'created_at': topic.get('created_at'),
                'views': topic.get('views'),
                'like_count': topic.get('like_count')
            })

        # 添加帖子结果
        for post in posts:
            results.append({
                'type': 'post',
                'id': post.get('id'),
                'topic_id': post.get('topic_id'),
                'username': post.get('username'),
                'cooked': post.get('cooked'),
                'created_at': post.get('created_at')
            })

        return results

    def search_in_category(self, query: str, category: str = "ai-general", limit: int = 20) -> List[Dict]:
        """
        在指定版块搜索

        Args:
            query: 搜索关键词
            category: 版块 slug
            limit: 返回结果数量限制

        Returns:
            帖子列表
        """
        url = f"{self.base_url}/search.json"
        params = {
            "q": f"#{category} {query}",
            "per_page": limit
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        topics = data.get('topics', [])

        results = []
        for topic in topics:
            results.append({
                'type': 'topic',
                'id': topic.get('id'),
                'title': topic.get('title'),
                'slug': topic.get('slug'),
                'category': topic.get('category_name'),
                'created_at': topic.get('created_at'),
                'views': topic.get('views'),
                'like_count': topic.get('like_count')
            })

        return results

    def search_by_user(self, username: str, limit: int = 20) -> List[Dict]:
        """
        搜索用户的帖子

        Args:
            username: 用户名
            limit: 返回结果数量限制

        Returns:
            帖子列表
        """
        url = f"{self.base_url}/search.json"
        params = {
            "q": f"@{username}",
            "per_page": limit
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        posts = data.get('posts', [])

        results = []
        for post in posts:
            results.append({
                'type': 'post',
                'id': post.get('id'),
                'topic_id': post.get('topic_id'),
                'username': post.get('username'),
                'cooked': post.get('cooked'),
                'created_at': post.get('created_at')
            })

        return results

    def display_results(self, results: List[Dict], show_preview: bool = False):
        """
        显示搜索结果

        Args:
            results: 搜索结果列表
            show_preview: 是否显示内容预览
        """
        if not results:
            print("❌ 没有找到相关帖子")
            return

        print(f"✅ 找到 {len(results)} 条结果\n")
        print("=" * 60)

        for i, item in enumerate(results, 1):
            print(f"\n{i}. {item.get('title') or item.get('type', '').capitalize()}")

            if item.get('type') == 'topic':
                print(f"   版块: {item.get('category', '未知')}")
                print(f"   浏览: {item.get('views', 0)} | 点赞: {item.get('like_count', 0)}")
                slug = item.get('slug', 'topic')
                topic_id = item.get('id')
                print(f"   🔗 /t/{slug}/{topic_id}")
            else:
                print(f"   作者: {item.get('username', '未知')}")
                print(f"   🔗 /t/topic/{item.get('topic_id')}")

            if show_preview and item.get('cooked'):
                # 清理 HTML 标签
                preview = re.sub(r'<[^>]+>', '', item['cooked'])
                preview = ' '.join(preview.split())
                if len(preview) > 150:
                    preview = preview[:147] + '...'
                print(f"   预览: {preview}")

        print("\n" + "=" * 60)


def main():
    """主函数"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='OpenClaw 论坛搜索工具')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--category', help='在指定版块搜索')
    parser.add_argument('--user', help='搜索用户的帖子')
    parser.add_argument('--limit', type=int, default=20, help='返回结果数量')
    parser.add_argument('--preview', action='store_true', help='显示内容预览')

    args = parser.parse_args()

    searcher = ForumSearcher()

    print("""
    ╔════════════════════════════════════════════╗
    ║     🔍 OpenClaw 论坛搜索工具 🔍               ║
    ╚════════════════════════════════════════════╝
    \n""")

    try:
        if args.user:
            print(f"🔍 搜索用户 @{args.user} 的帖子...\n")
            results = searcher.search_by_user(args.user, args.limit)
        elif args.category:
            print(f"🔍 在版块 #{args.category} 中搜索 \"{args.query}\"...\n")
            results = searcher.search_in_category(args.query, args.category, args.limit)
        else:
            print(f"🔍 搜索 \"{args.query}\"...\n")
            results = searcher.search_posts(args.query, args.limit)

        searcher.display_results(results, show_preview=args.preview)

    except Exception as e:
        print(f"❌ 搜索失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
