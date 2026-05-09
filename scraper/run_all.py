#!/usr/bin/env python3
"""
Data Scraper Main Entry
执行所有数据抓取任务
"""

import sys
import os
from pathlib import Path

# 添加当前目录到 Python 路径
SCRIPT_DIR = Path(__file__).parent.absolute()
sys.path.insert(0, str(SCRIPT_DIR))

from datetime import datetime, timezone, timedelta

def print_banner():
    """打印横幅"""
    print("=" * 60)
    print("    Agent Skills Website - Data Scraper")
    print("    从多数据源抓取 Skills、教程、资讯数据")
    print("=" * 60)
    print()

def print_section(title: str):
    """打印分节标题"""
    print()
    print("-" * 60)
    print(f"  {title}")
    print("-" * 60)

def main():
    """主函数"""
    print_banner()
    
    start_time = datetime.now()
    
    # 确保输出目录存在
    data_dir = SCRIPT_DIR / "..data"
    if not data_dir.exists():
        data_dir.mkdir(parents=True, exist_ok=True)
    
    # 切换到脚本目录
    os.chdir(SCRIPT_DIR)
    
    success_count = 0
    total_count = 3
    
    # 1. 抓取 Skills 数据
    print_section("Step 1/3: 抓取 Skills 数据")
    try:
        from scrape_skills import scrape_all as scrape_skills_func, save_skills
        skills_data = scrape_skills_func()
        save_skills(skills_data, "../data/skills.json")
        success_count += 1
        print(f"✓ Skills 数据抓取成功: {skills_data['totalCount']} 条")
    except Exception as e:
        print(f"✗ Skills 数据抓取失败: {e}")
    
    # 2. 抓取 Tutorials 数据
    print_section("Step 2/3: 抓取 Tutorials 数据")
    try:
        from scrape_tutorials import scrape_all as scrape_tutorials_func, save_tutorials
        tutorials_data = scrape_tutorials_func()
        save_tutorials(tutorials_data, "../data/tutorials.json")
        success_count += 1
        print(f"✓ Tutorials 数据抓取成功: {tutorials_data['totalCount']} 条")
    except Exception as e:
        print(f"✗ Tutorials 数据抓取失败: {e}")
    
    # 3. 抓取 News 数据
    print_section("Step 3/3: 抓取 News 数据")
    try:
        from scrape_news import scrape_all as scrape_news_func, save_news
        news_data = scrape_news_func()
        save_news(news_data, "../data/news.json")
        success_count += 1
        print(f"✓ News 数据抓取成功: {news_data['totalCount']} 条")
    except Exception as e:
        print(f"✗ News 数据抓取失败: {e}")
    
    # 总结
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print()
    print("=" * 60)
    print("  执行完成!")
    print(f"  - 成功: {success_count}/{total_count}")
    print(f"  - 耗时: {duration:.2f} 秒")
    print(f"  - 时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())
