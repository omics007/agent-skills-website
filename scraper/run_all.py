#!/usr/bin/env python3
"""
AgentSkills 多平台数据爬虫 - 主入口
运行所有爬虫脚本，聚合数据到 data/ 目录
"""

import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# 数据目录
DATA_DIR = Path(__file__).parent.parent / 'data'


def run_scraper(script_name: str, description: str) -> bool:
    """运行单个爬虫脚本"""
    print(f"\n{'='*60}")
    print(f"🔄 运行: {description}")
    print(f"{'='*60}")

    start_time = time.time()

    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=Path(__file__).parent,
            capture_output=False,
            timeout=300  # 5分钟超时
        )

        elapsed = time.time() - start_time

        if result.returncode == 0:
            print(f"✅ {description} 完成 (耗时: {elapsed:.1f}s)")
            return True
        else:
            print(f"❌ {description} 失败 (退出码: {result.returncode})")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏰ {description} 超时")
        return False
    except Exception as e:
        print(f"❌ {description} 异常: {e}")
        return False


def main():
    """主入口"""
    print("\n" + "="*60)
    print("🚀 AgentSkills 多平台数据爬虫")
    print(f"   启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   数据目录: {DATA_DIR}")
    print("="*60)

    # 确保数据目录存在
    DATA_DIR.mkdir(exist_ok=True)

    # 运行所有爬虫
    scrapers = [
        ("scrape_skills.py", "Skills 数据爬虫"),
        ("scrape_tutorials.py", "教程数据爬虫"),
        ("scrape_news.py", "资讯数据爬虫"),
    ]

    results = {}
    for script, desc in scrapers:
        results[desc] = run_scraper(script, desc)
        time.sleep(1)  # 爬虫间隔

    # 汇总结果
    print("\n" + "="*60)
    print("📊 运行结果汇总")
    print("="*60)

    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    for desc, success in results.items():
        status = "✅ 成功" if success else "❌ 失败"
        print(f"  {desc}: {status}")

    print(f"\n总计: {success_count}/{total_count} 成功")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 返回退出码
    sys.exit(0 if success_count == total_count else 1)


if __name__ == '__main__':
    main()
