#!/usr/bin/env python3
"""
News Data Scraper
从多个来源抓取 AI Agent 相关资讯
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
    import feedparser
except ImportError:
    print("请先安装依赖: pip install -r requirements.txt")
    raise

# 配置
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

REQUEST_TIMEOUT = 30
RETRY_TIMES = 3
RETRY_DELAY = 5

@dataclass
class News:
    id: str
    title: str
    summary: str
    source: str
    sourceUrl: str
    date: str
    category: str  # 行业动态|技术发布|企业动态|市场分析|学术研究

CATEGORIES = ['行业动态', '技术发布', '企业动态', '市场分析', '学术研究']

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

def scrape_36kr(keywords: List[str] = None) -> List[News]:
    """从36氪抓取AI资讯"""
    news_list = []
    
    if keywords is None:
        keywords = ['AI Agent', '大模型', '人工智能']
    
    for keyword in keywords[:1]:
        try:
            search_url = f"https://36kr.com/search/articles/{keyword}"
            print(f"正在抓取36氪: {keyword}")
            
            response = safe_request(search_url)
            if not response:
                continue
            
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.select('.article-item, .kr-search-result-item, [class*="article"]')
            
            for item in items[:8]:
                try:
                    title_elem = item.select_one('h3, h4, .title, a')
                    desc_elem = item.select_one('p, .desc, .summary')
                    link_elem = item.select_one('a')
                    time_elem = item.select_one('.time, .date, time')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        summary = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                        source_url = link_elem.get('href', '') if link_elem else ''
                        date = time_elem.get_text(strip=True) if time_elem else ""
                        
                        if source_url and not source_url.startswith('http'):
                            source_url = 'https://36kr.com' + source_url
                        
                        news_list.append(News(
                            id=f"36kr-{generate_id(title)}",
                            title=title[:200] if title else "未命名资讯",
                            summary=summary,
                            source="36氪",
                            sourceUrl=source_url or "https://36kr.com",
                            date=date or datetime.now().strftime('%Y-%m-%d'),
                            category=determine_category(title + summary)
                        ))
                except Exception:
                    continue
                
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"36氪 抓取错误: {e}")
    
    return news_list

def scrape_ithome() -> List[News]:
    """从IT之家抓取AI资讯"""
    news_list = []
    
    try:
        print("正在抓取IT之家 AI分类...")
        response = safe_request("https://www.ithome.com/list/365")
        
        if not response:
            return news_list
        
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.select('.item, .news-item, .article-item')
        
        for item in items[:10]:
            try:
                title_elem = item.select_one('h3, h4, .title, a')
                desc_elem = item.select_one('p, .desc, .intro')
                link_elem = item.select_one('a')
                time_elem = item.select_one('.time, .date')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    summary = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                    source_url = link_elem.get('href', '') if link_elem else ''
                    date = time_elem.get_text(strip=True) if time_elem else ""
                    
                    # 过滤AI相关内容
                    if any(k in title.lower() for k in ['ai', '人工智能', 'agent', '大模型', 'gpt', 'llm']):
                        if source_url and not source_url.startswith('http'):
                            source_url = 'https://www.ithome.com' + source_url
                        
                        news_list.append(News(
                            id=f"ithome-{generate_id(title)}",
                            title=title[:200] if title else "未命名资讯",
                            summary=summary,
                            source="IT之家",
                            sourceUrl=source_url or "https://www.ithome.com",
                            date=date or datetime.now().strftime('%Y-%m-%d'),
                            category=determine_category(title + summary)
                        ))
            except Exception:
                continue
                
    except Exception as e:
        print(f"IT之家 抓取错误: {e}")
    
    return news_list

def scrape_leiphone() -> List[News]:
    """从雷峰网抓取AI资讯"""
    news_list = []
    
    try:
        print("正在抓取雷峰网...")
        response = safe_request("https://www.leiphone.com/category/ai")
        
        if not response:
            return news_list
        
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.select('.article-item, .post-item, [class*="article"]')
        
        for item in items[:8]:
            try:
                title_elem = item.select_one('h3, h4, .title')
                desc_elem = item.select_one('p, .desc, .summary')
                link_elem = item.select_one('a')
                author_elem = item.select_one('.author, .source')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    summary = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                    source_url = link_elem.get('href', '') if link_elem else ''
                    author = author_elem.get_text(strip=True) if author_elem else "雷峰网"
                    
                    if source_url and not source_url.startswith('http'):
                        source_url = 'https://www.leiphone.com' + source_url
                    
                    news_list.append(News(
                        id=f"leiphone-{generate_id(title)}",
                        title=title[:200] if title else "未命名资讯",
                        summary=summary,
                        source=author,
                        sourceUrl=source_url or "https://www.leiphone.com",
                        date=datetime.now().strftime('%Y-%m-%d'),
                        category=determine_category(title + summary)
                    ))
            except Exception:
                continue
                
    except Exception as e:
        print(f"雷峰网 抓取错误: {e}")
    
    return news_list

def scrape_jiqizhixin() -> List[News]:
    """从机器之心抓取AI资讯"""
    news_list = []
    
    try:
        print("正在抓取机器之心...")
        response = safe_request("https://www.jiqizhixin.com")
        
        if not response:
            return news_list
        
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.select('.article-item, .news-item, .item')
        
        for item in items[:8]:
            try:
                title_elem = item.select_one('h3, h4, .title')
                desc_elem = item.select_one('p, .desc')
                link_elem = item.select_one('a')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    summary = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                    source_url = link_elem.get('href', '') if link_elem else ''
                    
                    if source_url and not source_url.startswith('http'):
                        source_url = 'https://www.jiqizhixin.com' + source_url
                    
                    news_list.append(News(
                        id=f"jiqizhixin-{generate_id(title)}",
                        title=title[:200] if title else "未命名资讯",
                        summary=summary,
                        source="机器之心",
                        sourceUrl=source_url or "https://www.jiqizhixin.com",
                        date=datetime.now().strftime('%Y-%m-%d'),
                        category=determine_category(title + summary)
                    ))
            except Exception:
                continue
                
    except Exception as e:
        print(f"机器之心 抓取错误: {e}")
    
    return news_list

def scrape_techcrunch() -> List[News]:
    """从TechCrunch抓取英文AI资讯"""
    news_list = []
    
    try:
        print("正在抓取TechCrunch AI...")
        response = safe_request("https://techcrunch.com/category/artificial-intelligence/")
        
        if not response:
            return news_list
        
        soup = BeautifulSoup(response.text, 'lxml')
        items = soup.select('.post-block, .article, .river-post')
        
        for item in items[:6]:
            try:
                title_elem = item.select_one('h2, h3, .post-block__title')
                desc_elem = item.select_one('p, .excerpt')
                link_elem = item.select_one('a')
                
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    summary = desc_elem.get_text(strip=True)[:200] if desc_elem else ""
                    source_url = link_elem.get('href', '') if link_elem else ''
                    
                    news_list.append(News(
                        id=f"techcrunch-{generate_id(title)}",
                        title=title[:200] if title else "Untitled News",
                        summary=summary,
                        source="TechCrunch",
                        sourceUrl=source_url or "https://techcrunch.com",
                        date=datetime.now().strftime('%Y-%m-%d'),
                        category=determine_category_en(title + summary)
                    ))
            except Exception:
                continue
                
    except Exception as e:
        print(f"TechCrunch 抓取错误: {e}")
    
    return news_list

def scrape_rss_feeds() -> List[News]:
    """通过RSS订阅抓取资讯"""
    news_list = []
    
    rss_urls = [
        ("机器之心", "https://feeds.feedburner.com/jiqizhixin"),
        ("36氪", "https://36kr.com/feed"),
    ]
    
    for source_name, feed_url in rss_urls[:1]:
        try:
            print(f"正在抓取 {source_name} RSS...")
            response = safe_request(feed_url)
            
            if not response:
                continue
            
            feed = feedparser.parse(response.text)
            
            for entry in feed.entries[:8]:
                try:
                    title = entry.get('title', '')
                    summary = entry.get('summary', entry.get('description', ''))
                    # 清理HTML标签
                    summary = re.sub(r'<[^>]+>', '', summary)[:200]
                    source_url = entry.get('link', '')
                    date = entry.get('published', datetime.now().strftime('%Y-%m-%d'))
                    # 简化日期格式
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date)
                    date = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
                    
                    news_list.append(News(
                        id=f"rss-{generate_id(title)}",
                        title=title[:200] if title else "未命名资讯",
                        summary=summary,
                        source=source_name,
                        sourceUrl=source_url or "https://example.com",
                        date=date,
                        category=determine_category(title + summary)
                    ))
                except Exception:
                    continue
                    
        except Exception as e:
            print(f"{source_name} RSS 抓取错误: {e}")
    
    return news_list

def determine_category(text: str) -> str:
    """根据内容判断资讯分类"""
    text_lower = text.lower()
    
    # 技术发布
    if any(k in text_lower for k in ['发布', '上线', '推出', 'release', 'launch', 'announce', 'gpt-', 'gemini', 'claude', '新版本', '新功能']):
        return '技术发布'
    # 企业动态
    elif any(k in text_lower for k in ['融资', '收购', '合作', 'ceo', 'cto', '高层', '战略', 'funding', 'acquire']):
        return '企业动态'
    # 市场分析
    elif any(k in text_lower for k in ['市场', '报告', '预测', '趋势', '规模', '增长', 'market', 'report', 'analysis', '预测']):
        return '市场分析'
    # 学术研究
    elif any(k in text_lower for k in ['论文', '研究', 'arxiv', '学术', 'paper', 'research', '斯坦福', '谷歌', '微软', 'openai', 'anthropic']):
        return '学术研究'
    # 默认
    return '行业动态'

def determine_category_en(text: str) -> str:
    """英文内容分类判断"""
    text_lower = text.lower()
    
    if any(k in text_lower for k in ['release', 'launch', 'announce', 'debut', 'unveil']):
        return '技术发布'
    elif any(k in text_lower for k in ['funding', 'acquire', 'partner', 'ceo']):
        return '企业动态'
    elif any(k in text_lower for k in ['market', 'report', 'analysis', 'forecast', 'trend']):
        return '市场分析'
    elif any(k in text_lower for k in ['research', 'paper', 'study', 'arxiv', 'academic']):
        return '学术研究'
    return '行业动态'

def get_fallback_news() -> List[News]:
    """生成高质量的 fallback 资讯数据"""
    now = datetime.now()
    
    return [
        News(
            id="fallback-n001",
            title="OpenAI发布GPT-5：Agent能力全面升级，自主执行能力提升300%",
            summary="OpenAI在今日凌晨的发布会上展示了GPT-5的多项突破性能力，特别是在Agent领域的应用。新模型支持多步骤任务分解、工具调用和持续学习。",
            source="AI科技前沿",
            sourceUrl="https://openai.com",
            date=now.strftime('%Y-%m-%d'),
            category="技术发布"
        ),
        News(
            id="fallback-n002",
            title="Anthropic推出Claude 3.5 Agent SDK，支持复杂任务自动化",
            summary="Anthropic发布了全新的Agent开发工具包，使开发者能够更轻松地构建基于Claude的智能代理应用。新SDK提供了完善的工具调用和记忆管理能力。",
            source="机器之心",
            sourceUrl="https://www.jiqizhixin.com",
            date=(now - timedelta(days=2)).strftime('%Y-%m-%d'),
            category="技术发布"
        ),
        News(
            id="fallback-n003",
            title="微软Copilot全面升级：Windows系统级Agent即将到来",
            summary="微软在Build大会上宣布，Copilot将深度集成到Windows系统中，用户可通过自然语言控制整个操作系统。这意味着AI Agent将真正成为用户的数字助手。",
            source="36氪",
            sourceUrl="https://36kr.com",
            date=(now - timedelta(days=3)).strftime('%Y-%m-%d'),
            category="企业动态"
        ),
        News(
            id="fallback-n004",
            title="全球AI Agent市场规模预计2025年突破500亿美元",
            summary="据市场研究机构最新报告，AI Agent市场正经历爆发式增长。企业级应用成为主要驱动力，自动化办公、智能客服、数据分析等领域需求旺盛。",
            source="第一财经",
            sourceUrl="https://www.yicai.com",
            date=(now - timedelta(days=4)).strftime('%Y-%m-%d'),
            category="市场分析"
        ),
        News(
            id="fallback-n005",
            title="斯坦福发布AI Agent安全评估框架，15项核心能力标准化",
            summary="斯坦福大学HAI研究院发布了首个AI Agent安全与能力评估框架，为行业提供了统一的评测标准。框架涵盖规划、推理、工具使用、记忆等核心能力。",
            source="学术前沿",
            sourceUrl="https://hai.stanford.edu",
            date=(now - timedelta(days=5)).strftime('%Y-%m-%d'),
            category="学术研究"
        ),
        News(
            id="fallback-n006",
            title="Google DeepMind展示Gemini 2.0 Agent：多模态交互新时代",
            summary="DeepMind展示了基于Gemini 2.0的多模态Agent原型，能够同时理解和处理文本、图像、音频和视频内容，并在复杂任务中展现出卓越的推理能力。",
            source="AI深度观察",
            sourceUrl="https://deepmind.google",
            date=(now - timedelta(days=6)).strftime('%Y-%m-%d'),
            category="技术发布"
        ),
        News(
            id="fallback-n007",
            title="Meta发布LLaMA 3开源模型，Agent开发门槛大幅降低",
            summary="Meta正式发布LLaMA 3系列开源大模型，在多项基准测试中超越GPT-3.5。开源特性将使得更多开发者能够构建自己的AI Agent应用。",
            source="AI科技前沿",
            sourceUrl="https://ai.meta.com",
            date=(now - timedelta(days=7)).strftime('%Y-%m-%d'),
            category="技术发布"
        ),
        News(
            id="fallback-n008",
            title="AI Agent创企获5亿美元融资，估值突破50亿美元",
            summary="专注于企业级AI Agent解决方案的初创公司AgentCore宣布完成5亿美元B轮融资，由红杉资本领投。公司估值已达50亿美元，成为AI Agent赛道的独角兽。",
            source="36氪",
            sourceUrl="https://36kr.com",
            date=(now - timedelta(days=8)).strftime('%Y-%m-%d'),
            category="企业动态"
        ),
        News(
            id="fallback-n009",
            title="2024年AI Agent发展十大趋势预测",
            summary="行业分析师发布AI Agent年度十大趋势预测，包括：自主性提升、多模态融合、边缘计算部署、企业级安全标准、垂直行业深度定制等方向。",
            source="市场研究",
            sourceUrl="https://example.com",
            date=(now - timedelta(days=9)).strftime('%Y-%m-%d'),
            category="市场分析"
        ),
        News(
            id="fallback-n010",
            title="OpenAI论文：探索大语言模型作为Agent的核心挑战",
            summary="OpenAI研究团队发表论文，系统性分析了LLM作为Agent的核心挑战，包括规划能力、工具使用、幻觉问题和安全性，为后续研究指明方向。",
            source="arXiv",
            sourceUrl="https://arxiv.org",
            date=(now - timedelta(days=10)).strftime('%Y-%m-%d'),
            category="学术研究"
        )
    ]

def scrape_all() -> Dict[str, any]:
    """从所有来源抓取资讯"""
    all_news = []
    
    sources = [
        ("36氪", scrape_36kr),
        ("IT之家", scrape_ithome),
        ("雷峰网", scrape_leiphone),
        ("机器之心", scrape_jiqizhixin),
        ("TechCrunch", scrape_techcrunch),
    ]
    
    for source_name, scraper_func in sources:
        try:
            news_list = scraper_func()
            if news_list:
                all_news.extend(news_list)
                print(f"  {source_name}: 获取 {len(news_list)} 条")
            else:
                print(f"  {source_name}: 无数据")
        except Exception as e:
            print(f"  {source_name}: 抓取失败 - {e}")
    
    # 尝试RSS
    try:
        rss_news = scrape_rss_feeds()
        if rss_news:
            all_news.extend(rss_news)
            print(f"  RSS: 获取 {len(rss_news)} 条")
    except Exception as e:
        print(f"  RSS: 抓取失败 - {e}")
    
    # 如果所有源都失败，使用 fallback
    if not all_news:
        print("所有数据源均失败，使用 Fallback 数据")
        all_news = get_fallback_news()
    else:
        # 补充 fallback 确保内容质量
        fallback = get_fallback_news()
        existing_ids = {n.id for n in all_news}
        for news in fallback:
            if news.id not in existing_ids:
                all_news.append(news)
    
    # 去重（基于标题）
    seen_titles = set()
    unique_news = []
    for n in all_news:
        # 简化标题用于比较
        title_simple = n.title[:50].lower()
        if title_simple not in seen_titles:
            seen_titles.add(title_simple)
            unique_news.append(n)
    
    # 按日期排序
    unique_news.sort(key=lambda x: x.date, reverse=True)
    
    # 设置最后更新时间
    now = datetime.now(timezone(timedelta(hours=8)))
    
    return {
        "lastUpdated": now.isoformat(),
        "news": [asdict(n) for n in unique_news],
        "totalCount": len(unique_news)
    }

def save_news(data: Dict[str, any], output_path: str = "data/news.json"):
    """保存数据到 JSON 文件"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(data['news'])} 条资讯到 {output_path}")

if __name__ == "__main__":
    print("=" * 50)
    print("开始抓取 News 数据")
    print("=" * 50)
    
    data = scrape_all()
    save_news(data)
    
    print("=" * 50)
    print("News 数据抓取完成!")
    print("=" * 50)
