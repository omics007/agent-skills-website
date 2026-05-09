#!/usr/bin/env python3
"""
AgentSkills 数据爬虫 - API方式
从公开API获取真实数据，替代BeautifulSoup静态抓取
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 确保data目录存在
DATA_DIR = Path(__file__).parent.parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

def fetch_coze_skills():
    """从 Coze 官方获取 Skills/Bots 数据"""
    import urllib.request
    
    skills = []
    try:
        # Coze Store 页面有公开的bot列表
        # 由于没有公开API，我们尝试通过GitHub搜索获取Coze相关项目
        url = "https://api.github.com/search/repositories?q=coze+bot+skill&sort=stars&per_page=10"
        req = urllib.request.Request(url, headers={
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'AgentSkills-Crawler/1.0'
        })
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for repo in data.get('items', []):
                skills.append({
                    "id": f"github-{repo['id']}",
                    "name": repo['name'].replace('-', ' ').replace('_', ' ').title(),
                    "description": (repo.get('description') or 'AI Agent Skill')[:200],
                    "icon": "🤖",
                    "category": categorize_repo(repo),
                    "tags": extract_tags(repo),
                    "source": "GitHub",
                    "sourceUrl": repo['html_url'],
                    "installCount": repo.get('stargazers_count', 0),
                    "rating": min(5.0, 3.5 + repo.get('stargazers_count', 0) / 1000),
                    "author": repo.get('owner', {}).get('login', 'Unknown'),
                    "lastUpdated": repo.get('updated_at', '')[:10]
                })
    except Exception as e:
        print(f"Warning: Failed to fetch Coze skills from GitHub: {e}")
    
    return skills


def fetch_agent_skills():
    """从GitHub搜索AI Agent相关项目"""
    import urllib.request
    
    skills = []
    queries = [
        "ai+agent+framework",
        "llm+agent+tool",
        "ai+agent+workflow",
        "langchain+agent"
    ]
    
    seen_ids = set()
    
    for query in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&per_page=8"
            req = urllib.request.Request(url, headers={
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'AgentSkills-Crawler/1.0'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for repo in data.get('items', []):
                    if repo['id'] in seen_ids:
                        continue
                    seen_ids.add(repo['id'])
                    skills.append({
                        "id": f"github-{repo['id']}",
                        "name": repo['name'].replace('-', ' ').replace('_', ' ').title(),
                        "description": (repo.get('description') or 'AI Agent Skill')[:200],
                        "icon": get_category_icon(categorize_repo(repo)),
                        "category": categorize_repo(repo),
                        "tags": extract_tags(repo),
                        "source": "GitHub",
                        "sourceUrl": repo['html_url'],
                        "installCount": repo.get('stargazers_count', 0),
                        "rating": min(5.0, 3.5 + repo.get('stargazers_count', 0) / 1000),
                        "author": repo.get('owner', {}).get('login', 'Unknown'),
                        "lastUpdated": repo.get('updated_at', '')[:10]
                    })
        except Exception as e:
            print(f"Warning: Failed to fetch for query '{query}': {e}")
    
    return skills


def fetch_tutorials():
    """获取教程数据 - 从GitHub搜索技术文章和视频"""
    import urllib.request
    
    tutorials = []
    seen_ids = set()
    
    # 搜索优质教程仓库
    queries = [
        "awesome+ai+agent+tutorial",
        "langchain+tutorial+chinese",
        "ai+agent+guide"
    ]
    
    for query in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&per_page=5"
            req = urllib.request.Request(url, headers={
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'AgentSkills-Crawler/1.0'
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for repo in data.get('items', []):
                    if repo['id'] in seen_ids:
                        continue
                    seen_ids.add(repo['id'])
                    desc = repo.get('description') or 'AI Agent 教程资源'
                    tutorials.append({
                        "id": f"tutorial-{repo['id']}",
                        "title": repo['name'].replace('-', ' ').replace('_', ' ').title(),
                        "description": desc[:200],
                        "icon": "📚",
                        "type": "article",
                        "difficulty": guess_difficulty(repo),
                        "duration": guess_duration(repo),
                        "category": "工程实践",
                        "source": "GitHub",
                        "sourceUrl": repo['html_url'],
                        "author": repo.get('owner', {}).get('login', 'Unknown'),
                        "publishDate": repo.get('created_at', '')[:10],
                        "platform": "devto"
                    })
        except Exception as e:
            print(f"Warning: Failed to fetch tutorials: {e}")
    
    return tutorials


def fetch_news():
    """获取新闻数据 - 从Hacker News API"""
    import urllib.request
    
    news_list = []
    max_retries = 3
    
    for retry in range(max_retries):
        try:
            # Hacker News Top Stories
            url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            req = urllib.request.Request(url, headers={'User-Agent': 'AgentSkills-Crawler/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                story_ids = json.loads(resp.read().decode('utf-8'))[:15]
            
            for sid in story_ids:
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                    req2 = urllib.request.Request(story_url, headers={'User-Agent': 'AgentSkills-Crawler/1.0'})
                    with urllib.request.urlopen(req2, timeout=10) as resp2:
                        story = json.loads(resp2.read().decode('utf-8'))
                        if story and story.get('type') == 'story':
                            title = story.get('title', '')
                            # 只保留AI相关的
                            if any(kw in title.lower() for kw in ['ai', 'agent', 'llm', 'gpt', 'claude', 'openai', 'model', 'chatbot', 'langchain', 'automation']):
                                news_list.append({
                                    "id": f"hn-{story['id']}",
                                    "title": title,
                                    "summary": (story.get('text') or title)[:200] if story.get('text') else title[:200],
                                    "source": "Hacker News",
                                    "sourceUrl": story.get('url', f"https://news.ycombinator.com/item?id={story['id']}"),
                                    "date": datetime.fromtimestamp(story.get('time', 0)).strftime('%Y-%m-%d'),
                                    "category": categorize_news(title)
                                })
                except Exception:
                    continue
            break  # 成功获取后退出重试循环
        except Exception as e:
            print(f"Warning: HN API attempt {retry+1}/{max_retries} failed: {e}")
            if retry < max_retries - 1:
                import time
                time.sleep(2)
    
    return news_list


def categorize_repo(repo):
    """根据仓库信息推断分类"""
    name = (repo.get('name', '') + ' ' + (repo.get('description', '') or '')).lower()
    topics = ' '.join(repo.get('topics', [])).lower()
    text = name + ' ' + topics
    
    if any(kw in text for kw in ['data', 'csv', 'excel', 'chart', 'visualization', 'analytics']):
        return 'data'
    if any(kw in text for kw in ['code', 'dev', 'review', 'debug', 'programming']):
        return 'development'
    if any(kw in text for kw in ['image', 'art', 'creative', 'generate', 'design']):
        return 'creative'
    if any(kw in text for kw in ['research', 'paper', 'study', 'rag', 'llm']):
        return 'ai-research'
    if any(kw in text for kw in ['email', 'meeting', 'productivity', 'automation']):
        return 'productivity'
    return 'productivity'


def get_category_icon(category):
    icons = {
        'data': '📊',
        'development': '🔍',
        'creative': '🎨',
        'ai-research': '💡',
        'productivity': '📧',
    }
    return icons.get(category, '🤖')


def extract_tags(repo):
    """提取标签"""
    tags = list(repo.get('topics', []))[:3]
    if not tags:
        name = repo.get('name', '').lower()
        desc = (repo.get('description') or '').lower()
        text = name + ' ' + desc
        if 'ai' in text: tags.append('AI')
        if 'agent' in text: tags.append('Agent')
        if 'llm' in text: tags.append('LLM')
        if 'tool' in text: tags.append('工具')
        if 'auto' in text: tags.append('自动化')
    return tags[:3] if tags else ['AI']


def guess_difficulty(repo):
    stars = repo.get('stargazers_count', 0)
    if stars > 5000:
        return 'advanced'
    elif stars > 500:
        return 'intermediate'
    return 'beginner'


def guess_duration(repo):
    stars = repo.get('stargazers_count', 0)
    if stars > 5000:
        return '120分钟'
    elif stars > 500:
        return '60分钟'
    return '30分钟'


def categorize_news(title):
    title = title.lower()
    if any(kw in title for kw in ['release', 'launch', 'announce', '发布']):
        return '技术发布'
    if any(kw in title for kw in ['funding', 'raise', '融资', '估值']):
        return '企业动态'
    if any(kw in title for kw in ['market', 'report', '市场', '报告']):
        return '市场分析'
    if any(kw in title for kw in ['research', 'paper', 'study', '研究']):
        return '学术研究'
    return '行业动态'


def generate_categories(skills):
    """根据skills数据生成分类"""
    cat_map = {}
    for s in skills:
        cat = s.get('category', 'productivity')
        if cat not in cat_map:
            cat_map[cat] = {'id': cat, 'name': get_category_name(cat), 'icon': get_category_icon(cat), 'count': 0}
        cat_map[cat]['count'] += 1
    return list(cat_map.values())


def get_category_name(cat):
    names = {
        'productivity': '效率工具',
        'data': '数据分析',
        'development': '开发工具',
        'creative': '创意设计',
        'ai-research': 'AI研究',
    }
    return names.get(cat, cat)


def main():
    print("=" * 60)
    print("AgentSkills 数据爬虫 v2.0 (API模式)")
    print("=" * 60)
    
    # Fetch skills
    print("\n📡 获取 Skills 数据...")
    skills = fetch_agent_skills()
    coze_skills = fetch_coze_skills()
    skills = coze_skills + skills
    print(f"   获取到 {len(skills)} 个 Skills")
    
    # Fetch tutorials
    print("\n📡 获取教程数据...")
    tutorials = fetch_tutorials()
    print(f"   获取到 {len(tutorials)} 个教程")
    
    # Fetch news
    print("\n📡 获取资讯数据...")
    news = fetch_news()
    print(f"   获取到 {len(news)} 条资讯")
    
    # Generate categories
    categories = generate_categories(skills)
    
    # Save data
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+08:00')
    
    skills_data = {
        "lastUpdated": now,
        "categories": categories,
        "skills": skills,
        "totalCount": len(skills)
    }
    
    tutorials_data = {
        "lastUpdated": now,
        "tutorials": tutorials,
        "totalCount": len(tutorials)
    }
    
    news_data = {
        "lastUpdated": now,
        "news": news,
        "totalCount": len(news)
    }
    
    # Write files
    with open(DATA_DIR / 'skills.json', 'w', encoding='utf-8') as f:
        json.dump(skills_data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ skills.json 已保存 ({len(skills)} 条)")
    
    with open(DATA_DIR / 'tutorials.json', 'w', encoding='utf-8') as f:
        json.dump(tutorials_data, f, ensure_ascii=False, indent=2)
    print(f"✅ tutorials.json 已保存 ({len(tutorials)} 条)")
    
    with open(DATA_DIR / 'news.json', 'w', encoding='utf-8') as f:
        json.dump(news_data, f, ensure_ascii=False, indent=2)
    print(f"✅ news.json 已保存 ({len(news)} 条)")
    
    print(f"\n🎉 数据更新完成！时间: {now}")
    return True


if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 爬虫执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
