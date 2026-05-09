#!/usr/bin/env python3
"""运行所有爬虫 - API模式"""
import subprocess
import sys

def main():
    print("启动 AgentSkills 数据爬虫 (API模式)...")
    result = subprocess.run(
        [sys.executable, 'scrape_api.py'],
        cwd='scraper',
        capture_output=False
    )
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
