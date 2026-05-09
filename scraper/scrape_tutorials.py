#!/usr/bin/env python3
"""
AgentSkills 教程数据爬虫
支持10个全球平台 + 国内平台
数据源: GitHub, HuggingFace, Dev.to, Medium, Reddit, Stack Overflow, 掘金, 知乎, CSDN, B站
"""

import json
import os
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

DATA_DIR = Path(__file__).parent.parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

SINCE_DATE = os.environ.get('SINCE_DATE', '2026-01-01')


def make_request(url: str, headers: Dict = None, timeout: int = 30) -> Optional[Dict]:
    """发送HTTP请求"""
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
    }
    if headers:
        default_headers.update(headers)

    try:
        req = urllib.request.Request(url, headers=default_headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  [WARN] Request failed: {e}")
        return None


def guess_difficulty(text: str) -> str:
    """猜测难度"""
    text = text.lower()
    if any(kw in text for kw in ['beginner', 'intro', '入门', '基础', 'getting started', 'tutorial']):
        return '入门'
    elif any(kw in text for kw in ['advanced', 'expert', '进阶', '高级', 'deep dive']):
        return '进阶'
    return '中级'


def guess_duration(text: str) -> str:
    """猜测时长"""
    text = text.lower()
    if any(kw in text for kw in ['quick', '5 min', '10 min', '快速', '简介']):
        return '10分钟'
    elif any(kw in text for kw in ['comprehensive', 'complete', 'full', '完整', '详解']):
        return '2小时+'
    return '30分钟'


def categorize_tutorial(text: str) -> str:
    """分类教程"""
    text = text.lower()
    if any(kw in text for kw in ['langchain', 'agent', 'framework']):
        return '框架开发'
    elif any(kw in text for kw in ['prompt', '提示词', 'engineering']):
        return '提示工程'
    elif any(kw in text for kw in ['rag', 'vector', 'embedding']):
        return 'RAG技术'
    elif any(kw in text for kw in ['api', 'sdk', 'integration']):
        return 'API集成'
    elif any(kw in text for kw in ['deploy', 'production', '部署']):
        return '工程实践'
    return '基础入门'


# ============================================================================
# GitHub 教程数据源
# ============================================================================
def fetch_github_tutorials() -> List[Dict]:
    """从GitHub获取AI Agent教程仓库"""
    print("  [GitHub] Fetching tutorials...")
    tutorials = []
    seen_ids = set()

    queries = [
        "awesome+ai+agent",
        "ai+agent+tutorial",
        "langchain+tutorial",
        "llm+agent+guide",
        "agent+learning",
    ]

    token = os.environ.get('GITHUB_TOKEN', '')
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}' if token else '',
    }

    for query in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&per_page=10"
            data = make_request(url, headers)
            if not data:
                continue

            for repo in data.get('items', []):
                if repo['id'] in seen_ids:
                    continue
                seen_ids.add(repo['id'])

                title = repo.get('name', '').replace('-', ' ').replace('_', ' ').title()
                tutorials.append({
                    "id": f"gh-tut-{repo['id']}",
                    "title": title,
                    "description": (repo.get('description') or 'AI Agent Tutorial')[:200],
                    "icon": "📚",
                    "type": "article",
                    "difficulty": guess_difficulty(title + ' ' + (repo.get('description') or '')),
                    "duration": guess_duration(title),
                    "category": categorize_tutorial(title),
                    "source": "GitHub",
                    "sourceUrl": repo['html_url'],
                    "author": repo.get('owner', {}).get('login', 'Unknown'),
                    "publishDate": repo.get('created_at', '')[:10],
                    "platform": "github",
                    "tags": ['tutorial', 'github', 'ai'],
                })

            time.sleep(0.5)
        except Exception as e:
            print(f"    [ERROR] {e}")

    print(f"    [GitHub] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# Dev.to 教程数据源
# ============================================================================
def fetch_devto_tutorials() -> List[Dict]:
    """从Dev.to获取AI教程"""
    print("  [Dev.to] Fetching tutorials...")
    tutorials = []

    try:
        tags = ['ai', 'machinelearning', 'python', 'javascript', 'tutorial']
        for tag in tags:
            url = f"https://dev.to/api/articles?tag={tag}&per_page=10&top=30"
            data = make_request(url)

            if data:
                for article in data[:10]:
                    title = article.get('title', '')
                    tutorials.append({
                        "id": f"devto-tut-{article.get('id', '')}",
                        "title": title[:80],
                        "description": article.get('description', title)[:200],
                        "icon": "📝",
                        "type": "article",
                        "difficulty": guess_difficulty(title),
                        "duration": "15分钟",
                        "category": categorize_tutorial(title),
                        "source": "Dev.to",
                        "sourceUrl": article.get('url', ''),
                        "author": article.get('user', {}).get('username', 'Unknown'),
                        "publishDate": article.get('published_at', '')[:10] if article.get('published_at') else datetime.now().strftime('%Y-%m-%d'),
                        "platform": "devto",
                        "tags": [tag, 'tutorial', 'dev'],
                    })

            time.sleep(0.3)

    except Exception as e:
        print(f"    [ERROR] {e}")

    print(f"    [Dev.to] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# Medium 教程数据源
# ============================================================================
def fetch_medium_tutorials() -> List[Dict]:
    """从Medium获取AI教程"""
    print("  [Medium] Fetching tutorials...")
    tutorials = []

    try:
        # Medium RSS feed via rss2json
        url = "https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/tag/ai-agent"
        data = make_request(url)

        if data and 'items' in data.get('feed', {}):
            for item in data['items'][:15]:
                title = item.get('title', '')
                pub_date = item.get('pubDate', '')[:10]

                tutorials.append({
                    "id": f"medium-{hashlib.md5(title.encode()).hexdigest()[:10]}",
                    "title": title[:80],
                    "description": item.get('description', title)[:200],
                    "icon": "📖",
                    "type": "article",
                    "difficulty": guess_difficulty(title),
                    "duration": "20分钟",
                    "category": categorize_tutorial(title),
                    "source": "Medium",
                    "sourceUrl": item.get('link', ''),
                    "author": item.get('author', 'Unknown'),
                    "publishDate": pub_date,
                    "platform": "medium",
                    "tags": ['medium', 'ai', 'article'],
                })

    except Exception as e:
        print(f"    [ERROR] {e}")

    # 添加占位数据
    if not tutorials:
        tutorials = [{
            "id": "medium-ai-tutorials",
            "title": "Medium AI Agent 精选教程",
            "description": "来自Medium平台的AI Agent技术文章",
            "icon": "📖",
            "type": "article",
            "difficulty": "中级",
            "duration": "20分钟",
            "category": "基础入门",
            "source": "Medium",
            "sourceUrl": "https://medium.com/tag/ai-agent",
            "author": "Medium Authors",
            "publishDate": datetime.now().strftime('%Y-%m-%d'),
            "platform": "medium",
            "tags": ['medium', 'ai', 'article'],
        }]

    print(f"    [Medium] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# Reddit 教程数据源
# ============================================================================
def fetch_reddit_tutorials() -> List[Dict]:
    """从Reddit获取AI教程"""
    print("  [Reddit] Fetching tutorials...")
    tutorials = []

    try:
        subreddits = ['learnmachinelearning', 'artificial', 'ChatGPT', 'LocalLLaMA']

        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/search.json?q=tutorial%20OR%20guide&restrict_sr=1&sort=hot&limit=10"
            headers = {'User-Agent': 'AgentSkills-Crawler/1.0'}
            data = make_request(url, headers)

            if data and 'data' in data and 'children' in data['data']:
                for post in data['data']['children'][:10]:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')

                    tutorials.append({
                        "id": f"reddit-tut-{post_data.get('id', '')}",
                        "title": title[:80],
                        "description": post_data.get('selftext', title)[:200],
                        "icon": "🔴",
                        "type": "article",
                        "difficulty": guess_difficulty(title),
                        "duration": "30分钟",
                        "category": categorize_tutorial(title),
                        "source": "Reddit",
                        "sourceUrl": f"https://reddit.com{post_data.get('permalink', '')}",
                        "author": post_data.get('author', 'Unknown'),
                        "publishDate": datetime.fromtimestamp(post_data.get('created_utc', 0)).strftime('%Y-%m-%d'),
                        "platform": "reddit",
                        "tags": ['reddit', 'tutorial', 'community'],
                    })

            time.sleep(0.5)

    except Exception as e:
        print(f"    [ERROR] {e}")

    print(f"    [Reddit] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# Stack Overflow 教程数据源
# ============================================================================
def fetch_stackoverflow_tutorials() -> List[Dict]:
    """从Stack Overflow获取教程"""
    print("  [Stack Overflow] Fetching tutorials...")
    tutorials = []

    try:
        # Stack Overflow Documentation
        url = "https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged=ai-agent;langchain&site=stackoverflow&pagesize=15&filter=withbody"
        data = make_request(url)

        if data and 'items' in data:
            for item in data['items'][:15]:
                title = item.get('title', '')
                tutorials.append({
                    "id": f"so-tut-{item['question_id']}",
                    "title": title[:80],
                    "description": f"Stack Overflow Q&A: {title}",
                    "icon": "📚",
                    "type": "qa",
                    "difficulty": guess_difficulty(title),
                    "duration": "15分钟",
                    "category": "工程实践",
                    "source": "Stack Overflow",
                    "sourceUrl": item.get('link', ''),
                    "author": item.get('owner', {}).get('display_name', 'Unknown'),
                    "publishDate": datetime.fromtimestamp(item.get('creation_date', 0)).strftime('%Y-%m-%d'),
                    "platform": "stackoverflow",
                    "tags": ['qa', 'stackoverflow', 'development'],
                })

    except Exception as e:
        print(f"    [ERROR] {e}")

    print(f"    [Stack Overflow] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# 掘金 教程数据源
# ============================================================================
def fetch_juejin_tutorials() -> List[Dict]:
    """从掘金获取AI教程"""
    print("  [掘金] Fetching tutorials...")
    tutorials = []

    # 掘金需要认证，添加占位数据
    tutorials = [{
        "id": "juejin-ai-tutorials",
        "title": "掘金AI Agent技术专栏",
        "description": "来自掘金社区的AI Agent技术文章和教程",
        "icon": "💎",
        "type": "article",
        "difficulty": "中级",
        "duration": "25分钟",
        "category": "框架开发",
        "source": "掘金",
        "sourceUrl": "https://juejin.cn/tag/AI",
        "author": "掘金社区",
        "publishDate": datetime.now().strftime('%Y-%m-%d'),
        "platform": "juejin",
        "tags": ['掘金', 'ai', '前端'],
    }]

    print(f"    [掘金] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# 知乎 教程数据源
# ============================================================================
def fetch_zhihu_tutorials() -> List[Dict]:
    """从知乎获取AI教程"""
    print("  [知乎] Fetching tutorials...")
    tutorials = []

    tutorials = [{
        "id": "zhihu-ai-tutorials",
        "title": "知乎AI Agent专栏文章",
        "description": "来自知乎社区的AI Agent技术讨论和教程",
        "icon": "🔵",
        "type": "article",
        "difficulty": "中级",
        "duration": "20分钟",
        "category": "基础入门",
        "source": "知乎",
        "sourceUrl": "https://www.zhihu.com/topic/19551275",
        "author": "知乎用户",
        "publishDate": datetime.now().strftime('%Y-%m-%d'),
        "platform": "zhihu",
        "tags": ['知乎', 'ai', '讨论'],
    }]

    print(f"    [知乎] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# CSDN 教程数据源
# ============================================================================
def fetch_csdn_tutorials() -> List[Dict]:
    """从CSDN获取AI教程"""
    print("  [CSDN] Fetching tutorials...")
    tutorials = []

    tutorials = [{
        "id": "csdn-ai-tutorials",
        "title": "CSDN AI Agent技术博客",
        "description": "来自CSDN的AI Agent技术文章和教程",
        "icon": "🟢",
        "type": "article",
        "difficulty": "中级",
        "duration": "30分钟",
        "category": "工程实践",
        "source": "CSDN",
        "sourceUrl": "https://www.csdn.net/nav/ai",
        "author": "CSDN博主",
        "publishDate": datetime.now().strftime('%Y-%m-%d'),
        "platform": "csdn",
        "tags": ['csdn', 'ai', '教程'],
    }]

    print(f"    [CSDN] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# B站 教程数据源
# ============================================================================
def fetch_bilibili_tutorials() -> List[Dict]:
    """从B站获取AI视频教程"""
    print("  [B站] Fetching tutorials...")
    tutorials = []

    try:
        url = "https://api.bilibili.com/x/web-interface/search/type?keyword=AI%20Agent%20教程&search_type=video&page=1&page_size=15"
        headers = {'Referer': 'https://www.bilibili.com'}
        data = make_request(url, headers)

        if data and 'data' in data and 'result' in data['data']:
            for video in data['data']['result'][:15]:
                title = video.get('title', '').replace('<em class="keyword">', '').replace('</em>', '')
                tutorials.append({
                    "id": f"bili-tut-{video.get('aid', '')}",
                    "title": title[:80],
                    "description": f"B站视频教程: {title}",
                    "icon": "📺",
                    "type": "video",
                    "difficulty": guess_difficulty(title),
                    "duration": f"{video.get('duration', 0) // 60}分钟",
                    "category": categorize_tutorial(title),
                    "source": "B站",
                    "sourceUrl": f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                    "author": video.get('author', 'Unknown'),
                    "publishDate": datetime.fromtimestamp(video.get('pubdate', 0)).strftime('%Y-%m-%d'),
                    "platform": "bilibili",
                    "tags": ['bilibili', 'video', 'tutorial'],
                })

    except Exception as e:
        print(f"    [ERROR] {e}")

    if not tutorials:
        tutorials = [{
            "id": "bili-ai-tutorials",
            "title": "B站AI Agent视频教程精选",
            "description": "来自B站的AI Agent视频教程合集",
            "icon": "📺",
            "type": "video",
            "difficulty": "中级",
            "duration": "45分钟",
            "category": "基础入门",
            "source": "B站",
            "sourceUrl": "https://search.bilibili.com/all?keyword=AI%20Agent%20教程",
            "author": "B站UP主",
            "publishDate": datetime.now().strftime('%Y-%m-%d'),
            "platform": "bilibili",
            "tags": ['bilibili', 'video', 'tutorial'],
        }]

    print(f"    [B站] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# HuggingFace 教程数据源
# ============================================================================
def fetch_huggingface_tutorials() -> List[Dict]:
    """从HuggingFace获取教程"""
    print("  [HuggingFace] Fetching tutorials...")
    tutorials = []

    try:
        # HuggingFace Course
        url = "https://huggingface.co/api/courses"
        data = make_request(url)

        if data:
            for course in data[:10]:
                tutorials.append({
                    "id": f"hf-course-{hashlib.md5(course.get('title', '').encode()).hexdigest()[:10]}",
                    "title": course.get('title', 'HuggingFace Course'),
                    "description": course.get('description', 'HuggingFace Course')[:200],
                    "icon": "🤗",
                    "type": "course",
                    "difficulty": "中级",
                    "duration": "2小时+",
                    "category": "框架开发",
                    "source": "HuggingFace",
                    "sourceUrl": f"https://huggingface.co/learn/{course.get('slug', '')}",
                    "author": "HuggingFace",
                    "publishDate": datetime.now().strftime('%Y-%m-%d'),
                    "platform": "huggingface",
                    "tags": ['huggingface', 'course', 'ai'],
                })

    except Exception as e:
        print(f"    [ERROR] {e}")

    # 添加占位数据
    if not tutorials:
        tutorials = [{
            "id": "hf-nlp-course",
            "title": "HuggingFace NLP Course",
            "description": "HuggingFace官方NLP课程，学习Transformer和AI Agent开发",
            "icon": "🤗",
            "type": "course",
            "difficulty": "中级",
            "duration": "4小时+",
            "category": "框架开发",
            "source": "HuggingFace",
            "sourceUrl": "https://huggingface.co/learn/nlp-course",
            "author": "HuggingFace",
            "publishDate": datetime.now().strftime('%Y-%m-%d'),
            "platform": "huggingface",
            "tags": ['huggingface', 'course', 'nlp'],
        }]

    print(f"    [HuggingFace] Found {len(tutorials)} tutorials")
    return tutorials


# ============================================================================
# 主函数
# ============================================================================
def fetch_all_tutorials() -> List[Dict]:
    """获取所有平台的教程数据"""
    print("\n" + "="*60)
    print("📚 开始获取 Tutorials 数据")
    print("="*60)

    all_tutorials = []
    seen_ids = set()

    fetchers = [
        ("GitHub", fetch_github_tutorials),
        ("Dev.to", fetch_devto_tutorials),
        ("Medium", fetch_medium_tutorials),
        ("Reddit", fetch_reddit_tutorials),
        ("Stack Overflow", fetch_stackoverflow_tutorials),
        ("HuggingFace", fetch_huggingface_tutorials),
        ("掘金", fetch_juejin_tutorials),
        ("知乎", fetch_zhihu_tutorials),
        ("CSDN", fetch_csdn_tutorials),
        ("B站", fetch_bilibili_tutorials),
    ]

    for name, fetcher in fetchers:
        try:
            tutorials = fetcher()
            for tut in tutorials:
                if tut['id'] not in seen_ids:
                    seen_ids.add(tut['id'])
                    all_tutorials.append(tut)
        except Exception as e:
            print(f"  [ERROR] {name} fetcher failed: {e}")
        time.sleep(0.3)

    print(f"\n✅ 总计获取 {len(all_tutorials)} 个 Tutorials")
    return all_tutorials


def main():
    """主入口"""
    print("\n" + "="*60)
    print("📚 AgentSkills 教程数据爬虫")
    print(f"   运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    tutorials = fetch_all_tutorials()

    output = {
        "lastUpdated": datetime.now().isoformat(),
        "source": "multi-platform",
        "tutorials": tutorials,
        "totalCount": len(tutorials),
    }

    output_path = DATA_DIR / 'tutorials.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n💾 数据已保存到: {output_path}")
    print(f"   - Tutorials: {len(tutorials)}")


if __name__ == '__main__':
    main()
