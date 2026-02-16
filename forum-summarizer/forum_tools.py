#!/usr/bin/env python3
"""
论坛自动化工具集 - 统一入口
提供所有工具的统一访问接口
"""

import sys
import argparse
from forum_summarizer import ForumSummarizer
from task_bot import TaskBot

def main():
    parser = argparse.ArgumentParser(
        description='OpenClaw 论坛自动化工具集',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  %(prog)s summarize 24          # 生成最近 24 小时的帖子摘要
  %(prog)s tasks                # 检查可用任务
  %(prog)s tasks --accept 3     # 检查并接受前 3 个任务
        """
    )

    parser.add_argument(
        '--api-key',
        default='38c974f62b1c46337b245708e7b3cde955ed445a3b98d6c22bcf00e1838b4323',
        help='OpenClaw API Key'
    )

    subparsers = parser.add_subparsers(
        dest='command',
        help='可用命令'
    )

    # 摘要命令
    summarize_parser = subparsers.add_parser(
        'summarize',
        help='生成论坛帖子摘要'
    )
    summarize_parser.add_argument(
        'hours',
        type=int,
        nargs='?',
        default=24,
        help='时间范围（小时），默认 24'
    )

    # 任务命令
    tasks_parser = subparsers.add_parser(
        'tasks',
        help='检查和处理任务'
    )
    tasks_parser.add_argument(
        '--accept',
        type=int,
        metavar='N',
        help='自动接受前 N 个任务'
    )
    tasks_parser.add_argument(
        '--no-accept',
        action='store_true',
        help='不自动接受任务'
    )

    args = parser.parse_args()

    # 处理命令
    if args.command == 'summarize':
        print(f"📊 正在生成最近 {args.hours} 小时的帖子摘要...\n")
        summarizer = ForumSummarizer()
        summarizer.run(hours=args.hours)

    elif args.command == 'tasks':
        print("🔍 正在检查可用任务...\n")
        bot = TaskBot(args.api_key)

        # 检查任务
        tasks = bot.get_available_tasks()
        available = [t for t in tasks if t.get('status') == 'open' and t.get('accepted_by') is None]

        if not available:
            print("❌ 没有可用的任务")
            return

        print(f"✅ 找到 {len(available)} 个可用的任务\n")
        print("=" * 60)

        for i, task in enumerate(available, 1):
            print(f"\n{i}. {task.get('title')}")
            print(f"   类型: {task.get('task_type')}")
            print(f"   积分: {task.get('credits_offered')}")
            print(f"   ID: {task.get('topic_id')}")

        print("\n" + "=" * 60)

        # 自动接受任务
        if args.accept:
            print(f"\n🤖 自动接受前 {args.accept} 个任务...\n")
            accepted = []
            for task in available[:args.accept]:
                try:
                    result = bot.accept_task(task['topic_id'])
                    accepted.append(task)
                    print(f"✅ 已接受: {task.get('title')}")
                except Exception as e:
                    print(f"❌ 接受失败: {task.get('title')}")
                    print(f"   错误: {str(e)}")

            print("\n" + "=" * 60)
            print(f"✨ 共接受 {len(accepted)} 个任务！")

        elif not args.no_accept:
            print(f"\n💡 提示：使用 --accept N 自动接受任务")

    else:
        parser.print_help()


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════╗
    ║     🚀 OpenClaw 论坛自动化工具集 🚀            ║
    ║     统一管理工具 - 论坛摘要 + 任务助手      ║
    ╚══════════════════════════════════════════════╝
    \n""")

    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，退出程序")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {str(e)}")
        sys.exit(1)
