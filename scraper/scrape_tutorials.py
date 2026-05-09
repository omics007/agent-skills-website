#!/usr/bin/env python3
"""
Tutorials Data Scraper
从多个平台抓取 AI Agent 教程数据
"""

import json
import re
import time
import random
import hashlib
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请先安装依赖: pip install -r requirements.txt")
    raise

# 配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

REQUEST_TIMEOUT = 30
RETRY_TIMES = 3
RETRY_DELAY = 5

@dataclass
class Tutorial:
    id: str
    title: str
    description: str
    icon: str
    type: str  # article | video
    difficulty: str  # beginner | intermediate | advanced
    duration: str
    category: str
    source: str
    sourceUrl: str
    author: str = ""
    publishDate: str = ""
    platform: str = ""

def generate_id(text: str) -> str:
    """生成唯一ID"""
    return hashlib.md5(text.encode()).hexdigest()[:12]

def safe_request(url: str, retries: int = RETRY_TIMES) -> Optional[requests.Response]:
    """安全的HTTP请求"""
    for i in range(retries):
        try:
            response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response
        except Exception as e:
            if i < retries - 1:
                time.sleep(RETRY_DELAY * (i + 1))
            else:
                print(f"请求失败 {url}: {e}")
    return None

def scrape_juejin(keywords: List[str] = None) -> List[Tutorial]:
    """从掘金抓取教程"""
    tutorials = []
    
    if keywords is None:
        keywords = ['AI Agent', '大模型应用', 'Prompt工程', 'LangChain']
    
    for keyword in keywords[:2]:
        try:
            search_url = f"https://search.juejin.cn/?query={keyword}&type=title"
            print(f"正在抓取掘金: {keyword}")
            
            response = safe_request(search_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('.item, .article-item, [class*="list-item"]')
            
            for item in items[:8]:
                try:
                    title_elem = item.select_one('h3, h4, .title')
                    desc_elem = item.select_one('p, .desc, .description')
                    author_elem = item.select_one('.author, .user-name')
                    link_elem = item.select_one('a')
                    time_elem = item.select_one('.time, .date, time')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        description = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                        author = author_elem.get_text(strip=True) if author_elem else ""
                        source_url = link_elem.get('href', '') if link_elem else ''
                        date = time_elem.get_text(strip=True) if time_elem else ""
                        
                        if source_url and not source_url.startswith('http'):
                            source_url = 'https://juejin.cn' + source_url
                        
                        tutorials.append(Tutorial(
                            id=f"juejin-{generate_id(title)}",
                            title=title[:150] if title else "未命名教程",
                            description=description,
                            icon='📝',
                            type='article',
                            difficulty=determine_difficulty(title + description),
                            duration=estimate_duration(description),
                            category=determine_category(keyword),
                            source='掘金',
                            sourceUrl=source_url or 'https://juejin.cn',
                            author=author,
                            publishDate=date,
                            platform='juejin'
                        ))
                except Exception:
                    continue
                
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"掘金 抓取错误: {e}")
    
    return tutorials

def scrape_csdn(keywords: List[str] = None) -> List[Tutorial]:
    """从CSDN抓取教程"""
    tutorials = []
    
    if keywords is None:
        keywords = ['AI Agent', 'ChatGPT开发', '智能助手']
    
    for keyword in keywords[:2]:
        try:
            search_url = f"https://so.csdn.net/search?q={keyword}&t=blog&type="
            print(f"正在抓取CSDN: {keyword}")
            
            response = safe_request(search_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('.search-list-item, .article-item, .blog-item')
            
            for item in items[:6]:
                try:
                    title_elem = item.select_one('h3, h4, .title')
                    desc_elem = item.select_one('p, .description, .abstract')
                    author_elem = item.select_one('.author, .user-info')
                    link_elem = item.select_one('a')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        description = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                        author = author_elem.get_text(strip=True) if author_elem else ""
                        source_url = link_elem.get('href', '') if link_elem else ''
                        
                        tutorials.append(Tutorial(
                            id=f"csdn-{generate_id(title)}",
                            title=title[:150] if title else "未命名教程",
                            description=description,
                            icon='📝',
                            type='article',
                            difficulty=determine_difficulty(title + description),
                            duration=estimate_duration(description),
                            category=determine_category(keyword),
                            source='CSDN',
                            sourceUrl=source_url or 'https://www.csdn.net',
                            author=author,
                            platform='csdn'
                        ))
                except Exception:
                    continue
                
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"CSDN 抓取错误: {e}")
    
    return tutorials

def scrape_zhihu(keywords: List[str] = None) -> List[Tutorial]:
    """从知乎抓取教程"""
    tutorials = []
    
    if keywords is None:
        keywords = ['AI Agent', '大模型', '人工智能']
    
    for keyword in keywords[:2]:
        try:
            search_url = f"https://www.zhihu.com/search?type=content&q={keyword}"
            print(f"正在抓取知乎: {keyword}")
            
            response = safe_request(search_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('.List-item, .ContentItem, [class*="item"]')
            
            for item in items[:6]:
                try:
                    title_elem = item.select_one('h2, h3, .Title')
                    desc_elem = item.select_one('p, . excerpt, .RichText')
                    author_elem = item.select_one('.Author, .name')
                    link_elem = item.select_one('a')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        description = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                        author = author_elem.get_text(strip=True) if author_elem else ""
                        source_url = link_elem.get('href', '') if link_elem else ''
                        
                        if source_url and not source_url.startswith('http'):
                            source_url = 'https://www.zhihu.com' + source_url
                        
                        tutorials.append(Tutorial(
                            id=f"zhihu-{generate_id(title)}",
                            title=title[:150] if title else "未命名教程",
                            description=description,
                            icon='📝',
                            type='article',
                            difficulty=determine_difficulty(title + description),
                            duration=estimate_duration(description),
                            category=determine_category(keyword),
                            source='知乎',
                            sourceUrl=source_url or 'https://www.zhihu.com',
                            author=author,
                            platform='zhihu'
                        ))
                except Exception:
                    continue
                
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"知乎 抓取错误: {e}")
    
    return tutorials

def scrape_bilibili(keywords: List[str] = None) -> List[Tutorial]:
    """从B站抓取视频教程"""
    tutorials = []
    
    if keywords is None:
        keywords = ['AI Agent教程', '大模型应用开发', 'LangChain教程']
    
    for keyword in keywords[:2]:
        try:
            search_url = f"https://search.bilibili.com/all?keyword={keyword}&spm_id_from=333.1007.0.0"
            print(f"正在抓取B站: {keyword}")
            
            response = safe_request(search_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('.video-item, .bili-video-card, [class*="video"]')
            
            for item in items[:8]:
                try:
                    title_elem = item.select_one('.title, h3, a')
                    desc_elem = item.select_one('.desc, .description')
                    author_elem = item.select_one('.up, .author, .up-name')
                    link_elem = item.select_one('a')
                    duration_elem = item.select_one('.duration, .time')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        description = desc_elem.get_text(strip=True)[:150] if desc_elem else ""
                        author = author_elem.get_text(strip=True) if author_elem else ""
                        source_url = link_elem.get('href', '') if link_elem else ''
                        duration = duration_elem.get_text(strip=True) if duration_elem else ""
                        
                        if source_url and not source_url.startswith('http'):
                            source_url = 'https://bilibili.com' + source_url
                        
                        tutorials.append(Tutorial(
                            id=f"bilibili-{generate_id(title)}",
                            title=title[:150] if title else "未命名视频",
                            description=description,
                            icon='🎬',
                            type='video',
                            difficulty=determine_difficulty(title + description),
                            duration=duration or "20分钟",
                            category=determine_category(keyword),
                            source='B站',
                            sourceUrl=source_url or 'https://bilibili.com',
                            author=author,
                            platform='bilibili'
                        ))
                except Exception:
                    continue
                
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"B站 抓取错误: {e}")
    
    return tutorials

def scrape_youtube(keywords: List[str] = None) -> List[Tutorial]:
    """从YouTube抓取英文教程"""
    tutorials = []
    
    if keywords is None:
        keywords = ['AI Agent tutorial', 'LangChain tutorial', 'LLM application']
    
    for keyword in keywords[:2]:
        try:
            search_url = f"https://www.youtube.com/results?search_query={keyword.replace(' ', '+')}"
            print(f"正在抓取YouTube: {keyword}")
            
            response = safe_request(search_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('#video-title, ytd-video-renderer, [class*="video"]')
            
            for item in items[:6]:
                try:
                    title_elem = item.select_one('#video-title, h3, a')
                    channel_elem = item.select_one('#channel-name, .ytd-channel-name, .author')
                    link_elem = item.select_one('a')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        channel = channel_elem.get_text(strip=True) if channel_elem else ""
                        source_url = link_elem.get('href', '') if link_elem else ''
                        
                        if source_url and not source_url.startswith('http'):
                            source_url = 'https://www.youtube.com' + source_url
                        
                        tutorials.append(Tutorial(
                            id=f"youtube-{generate_id(title)}",
                            title=title[:150] if title else "Untitled Video",
                            description=f"English tutorial about AI Agent development",
                            icon='🎬',
                            type='video',
                            difficulty=determine_difficulty(title),
                            duration="30分钟",
                            category="入门指南",
                            source='YouTube',
                            sourceUrl=source_url or 'https://youtube.com',
                            author=channel,
                            platform='youtube'
                        ))
                except Exception:
                    continue
                
            time.sleep(random.uniform(3, 5))
        except Exception as e:
            print(f"YouTube 抓取错误: {e}")
    
    return tutorials

def scrape_medium(keywords: List[str] = None) -> List[Tutorial]:
    """从Medium抓取英文教程"""
    tutorials = []
    
    if keywords is None:
        keywords = ['AI Agent', 'GPT-4 application', 'autonomous AI']
    
    for keyword in keywords[:2]:
        try:
            search_url = f"https://medium.com/search?q={keyword.replace(' ', '%20')}"
            print(f"正在抓取Medium: {keyword}")
            
            response = safe_request(search_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('article, .post-item, [class*="post"]')
            
            for item in items[:6]:
                try:
                    title_elem = item.select_one('h2, h3, h4')
                    desc_elem = item.select_one('p, .subtitle, .excerpt')
                    author_elem = item.select_one('.author, .name')
                    link_elem = item.select_one('a')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        description = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                        author = author_elem.get_text(strip=True) if author_elem else ""
                        source_url = link_elem.get('href', '') if link_elem else ''
                        
                        if source_url and not source_url.startswith('http'):
                            source_url = 'https://medium.com' + source_url
                        
                        tutorials.append(Tutorial(
                            id=f"medium-{generate_id(title)}",
                            title=title[:150] if title else "Untitled Article",
                            description=description,
                            icon='📝',
                            type='article',
                            difficulty=determine_difficulty(title + description),
                            duration=estimate_duration(description),
                            category="核心概念",
                            source='Medium',
                            sourceUrl=source_url or 'https://medium.com',
                            author=author,
                            platform='medium'
                        ))
                except Exception:
                    continue
                
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"Medium 抓取错误: {e}")
    
    return tutorials

def determine_difficulty(text: str) -> str:
    """根据内容判断难度"""
    text_lower = text.lower()
    
    advanced_keywords = ['高级', '深入', '进阶', '高级', 'complex', 'advanced', 'deep dive', 'expert']
    beginner_keywords = ['入门', '基础', '初学', 'beginner', 'basic', 'introduction', 'getting started', '从零', '小白']
    
    if any(k in text_lower for k in advanced_keywords):
        return 'advanced'
    elif any(k in text_lower for k in beginner_keywords):
        return 'beginner'
    return 'intermediate'

def estimate_duration(text: str) -> str:
    """估算学习时长"""
    if not text:
        return "30分钟"
    
    # 尝试从文本中提取时长信息
    duration_match = re.search(r'(\d+)\s*[分钟minhrs小时]', text)
    if duration_match:
        return f"{duration_match.group(1)}分钟"
    
    # 根据文本长度估算
    length = len(text)
    if length > 500:
        return "60分钟"
    elif length > 200:
        return "30分钟"
    return "20分钟"

def determine_category(keyword: str) -> str:
    """根据关键词确定分类"""
    keyword_lower = keyword.lower()
    
    if any(k in keyword_lower for k in ['入门', '基础', 'beginner', 'basic', '从零']):
        return "入门指南"
    elif any(k in keyword_lower for k in ['高级', '进阶', 'advanced', '实战', '项目']):
        return "高级特性"
    elif any(k in keyword_lower for k in ['架构', '设计', '最佳实践', 'architecture']):
        return "工程实践"
    return "核心概念"

def get_fallback_tutorials() -> List[Tutorial]:
    """生成高质量的 fallback 教程数据"""
    return [
        Tutorial(
            id="fallback-t001",
            title="从零构建你的第一个AI Agent",
            description="本教程将手把手教你使用Python构建一个完整的AI Agent，包括任务规划、工具调用和记忆管理。适合零基础入门者。",
            icon="🚀",
            type="article",
            difficulty="beginner",
            duration="45分钟",
            category="入门指南",
            source="掘金",
            sourceUrl="https://juejin.cn",
            author="AI开发者",
            platform="juejin"
        ),
        Tutorial(
            id="fallback-t002",
            title="深入理解ReAct范式：让Agent像人类一样思考",
            description="详细讲解ReAct（Reasoning + Acting）推理框架的原理和实现，通过案例展示如何在Agent中应用这一范式提升任务完成率。",
            icon="🧠",
            type="article",
            difficulty="intermediate",
            duration="60分钟",
            category="核心概念",
            source="知乎",
            sourceUrl="https://www.zhihu.com",
            author="技术专家",
            platform="zhihu"
        ),
        Tutorial(
            id="fallback-t003",
            title="构建多模态Agent：处理图像、音频和视频",
            description="学习如何构建支持多模态输入的Agent系统，涵盖视觉理解、语音识别、视频分析等关键技术。",
            icon="👁️",
            type="article",
            difficulty="advanced",
            duration="90分钟",
            category="高级特性",
            source="CSDN",
            sourceUrl="https://www.csdn.net",
            author="AI研究员",
            platform="csdn"
        ),
        Tutorial(
            id="fallback-t004",
            title="Agent Memory System设计与实现",
            description="深入探讨Agent的记忆系统设计，包括短期记忆、长期记忆、向量数据库集成和记忆检索策略。",
            icon="💾",
            type="article",
            difficulty="intermediate",
            duration="75分钟",
            category="核心概念",
            source="掘金",
            sourceUrl="https://juejin.cn",
            author="架构师",
            platform="juejin"
        ),
        Tutorial(
            id="fallback-t005",
            title="企业级Agent架构设计与最佳实践",
            description="分享构建生产级Agent系统的架构设计经验，涵盖可扩展性、安全性、监控和容错机制。",
            icon="🏢",
            type="article",
            difficulty="advanced",
            duration="120分钟",
            category="工程实践",
            source="知乎",
            sourceUrl="https://www.zhihu.com",
            author="技术总监",
            platform="zhihu"
        ),
        Tutorial(
            id="fallback-t006",
            title="Tool Learning：让Agent学会使用工具",
            description="系统讲解如何让Agent学习使用各种工具，包括API调用、代码执行、文件操作等，以及工具选择策略。",
            icon="🔧",
            type="article",
            difficulty="intermediate",
            duration="60分钟",
            category="核心概念",
            source="Medium",
            sourceUrl="https://medium.com",
            author="AI Engineer",
            platform="medium"
        ),
        Tutorial(
            id="fallback-t007",
            title="【视频】LangChain完整教程：从入门到实战",
            description="B站最完整的LangChain教程，手把手教你构建AI应用。包含多个实战项目。",
            icon="🎬",
            type="video",
            difficulty="beginner",
            duration="3小时",
            category="入门指南",
            source="B站",
            sourceUrl="https://bilibili.com",
            author="AI课堂",
            platform="bilibili"
        ),
        Tutorial(
            id="fallback-t008",
            title="【视频】Building AI Agents with LangChain - Full Course",
            description="Complete YouTube course on building AI agents using LangChain framework. English tutorial with code examples.",
            icon="🎬",
            type="video",
            difficulty="intermediate",
            duration="2小时",
            category="核心概念",
            source="YouTube",
            sourceUrl="https://youtube.com",
            author="DataScience DoJo",
            platform="youtube"
        ),
        Tutorial(
            id="fallback-t009",
            title="AutoGPT原理与实践：让AI自主完成任务",
            description="深入解析AutoGPT等自主Agent的技术原理，学习如何构建能够自我驱动完成复杂任务的AI系统。",
            icon="🤖",
            type="article",
            difficulty="advanced",
            duration="90分钟",
            category="高级特性",
            source="掘金",
            sourceUrl="https://juejin.cn",
            author="深度学习工程师",
            platform="juejin"
        ),
        Tutorial(
            id="fallback-t010",
            title="Coze工作流设计：从入门到精通",
            description="详细讲解扣子(Coze)平台的工作流设计方法，包括节点配置、条件分支、变量使用等核心功能。",
            icon="⚙️",
            type="article",
            difficulty="beginner",
            duration="45分钟",
            category="入门指南",
            source="CSDN",
            sourceUrl="https://www.csdn.net",
            author="Coze开发者",
            platform="csdn"
        )
    ]

def scrape_all() -> Dict[str, any]:
    """从所有平台抓取教程"""
    all_tutorials = []
    
    # 文章来源
    article_sources = [
        ("掘金", scrape_juejin),
        ("CSDN", scrape_csdn),
        ("知乎", scrape_zhihu),
        ("Medium", scrape_medium),
    ]
    
    # 视频来源
    video_sources = [
        ("B站", scrape_bilibili),
        ("YouTube", scrape_youtube),
    ]
    
    # 抓取文章
    for source_name, scraper_func in article_sources:
        try:
            tutorials = scraper_func()
            if tutorials:
                all_tutorials.extend(tutorials)
                print(f"  {source_name}: 获取 {len(tutorials)} 篇")
            else:
                print(f"  {source_name}: 无数据")
        except Exception as e:
            print(f"  {source_name}: 抓取失败 - {e}")
    
    # 抓取视频
    for source_name, scraper_func in video_sources:
        try:
            tutorials = scraper_func()
            if tutorials:
                all_tutorials.extend(tutorials)
                print(f"  {source_name}: 获取 {len(tutorials)} 个")
            else:
                print(f"  {source_name}: 无数据")
        except Exception as e:
            print(f"  {source_name}: 抓取失败 - {e}")
    
    # 如果所有源都失败，使用 fallback
    if not all_tutorials:
        print("所有数据源均失败，使用 Fallback 数据")
        all_tutorials = get_fallback_tutorials()
    else:
        # 补充 fallback 确保内容质量
        fallback = get_fallback_tutorials()
        existing_ids = {t.id for t in all_tutorials}
        for tut in fallback:
            if tut.id not in existing_ids:
                all_tutorials.append(tut)
    
    # 去重（基于标题）
    seen_titles = set()
    unique_tutorials = []
    for tut in all_tutorials:
        if tut.title not in seen_titles:
            seen_titles.add(tut.title)
            unique_tutorials.append(tut)
    
    # 设置最后更新时间
    now = datetime.now(timezone(timedelta(hours=8)))
    
    return {
        "lastUpdated": now.isoformat(),
        "tutorials": [asdict(t) for t in unique_tutorials],
        "totalCount": len(unique_tutorials)
    }

def save_tutorials(data: Dict[str, any], output_path: str = "data/tutorials.json"):
    """保存数据到 JSON 文件"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(data['tutorials'])} 条教程到 {output_path}")

if __name__ == "__main__":
    print("=" * 50)
    print("开始抓取 Tutorials 数据")
    print("=" * 50)
    
    data = scrape_all()
    save_tutorials(data)
    
    print("=" * 50)
    print("Tutorials 数据抓取完成!")
    print("=" * 50)
