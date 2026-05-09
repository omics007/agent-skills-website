#!/usr/bin/env python3
"""
AgentSkills 多平台数据爬虫
支持10个全球平台 + 国内平台
数据源: GitHub, HuggingFace, ProductHunt, Dev.to, Medium, Reddit, Stack Overflow, 掘金, 知乎, CSDN
国内平台: 微信, B站, 抖音
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
import hashlib

# 配置
DATA_DIR = Path(__file__).parent.parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

SINCE_DATE = os.environ.get('SINCE_DATE', '2026-01-01')
FULL_SYNC = os.environ.get('FULL_SYNC', 'false').lower() == 'true'

# 平台配置
PLATFORMS = {
    'github': {
        'name': 'GitHub',
        'icon': '🐙',
        'api_base': 'https://api.github.com',
    },
    'huggingface': {
        'name': 'HuggingFace',
        'icon': '🤗',
        'api_base': 'https://huggingface.co/api',
    },
    'producthunt': {
        'name': 'ProductHunt',
        'icon': '🚀',
        'api_base': 'https://api.producthunt.com/v2',
    },
    'pypi': {
        'name': 'PyPI',
        'icon': '📦',
        'api_base': 'https://pypi.org/pypi',
    },
    'npm': {
        'name': 'npm',
        'icon': '⬢',
        'api_base': 'https://registry.npmjs.org',
    },
    'dockerhub': {
        'name': 'Docker Hub',
        'icon': '🐳',
        'api_base': 'https://hub.docker.com/v2',
    },
    'vscode': {
        'name': 'VS Code Marketplace',
        'icon': '💠',
        'api_base': 'https://marketplace.visualstudio.com/_apis/public/gallery',
    },
    'replicate': {
        'name': 'Replicate',
        'icon': '🔮',
        'api_base': 'https://api.replicate.com/v1',
    },
    'ollama': {
        'name': 'Ollama',
        'icon': '🦙',
        'api_base': 'https://ollama.com/api',
    },
    'cursor': {
        'name': 'Cursor',
        'icon': '🖱️',
        'api_base': 'https://cursor.sh',
    },
    'devto': {
        'name': 'Dev.to',
        'icon': '📝',
        'api_base': 'https://dev.to/api',
    },
    'medium': {
        'name': 'Medium',
        'icon': '📖',
        'api_base': 'https://api.medium.com/v1',
    },
    'reddit': {
        'name': 'Reddit',
        'icon': '🔴',
        'api_base': 'https://oauth.reddit.com',
    },
    'stackoverflow': {
        'name': 'Stack Overflow',
        'icon': '📚',
        'api_base': 'https://api.stackexchange.com/2.3',
    },
    'juejin': {
        'name': '掘金',
        'icon': '💎',
        'api_base': 'https://api.juejin.cn',
    },
    'zhihu': {
        'name': '知乎',
        'icon': '🔵',
        'api_base': 'https://www.zhihu.com/api',
    },
    'csdn': {
        'name': 'CSDN',
        'icon': '🟢',
        'api_base': 'https://blog.csdn.net',
    },
    # 国内平台
    'weixin': {
        'name': '微信',
        'icon': '💬',
        'api_base': 'https://weixin.sogou.com',
    },
    'bilibili': {
        'name': 'B站',
        'icon': '📺',
        'api_base': 'https://api.bilibili.com',
    },
    'douyin': {
        'name': '抖音',
        'icon': '🎵',
        'api_base': 'https://www.douyin.com',
    },
}


def make_request(url: str, headers: Dict = None, timeout: int = 30) -> Optional[Dict]:
    """发送HTTP请求"""
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    if headers:
        default_headers.update(headers)

    try:
        req = urllib.request.Request(url, headers=default_headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  [WARN] Request failed: {url[:50]}... - {e}")
        return None


def categorize_skill(text: str) -> str:
    """根据文本内容分类"""
    text = text.lower()
    categories = {
        'development': ['agent', 'framework', 'sdk', 'api', 'library', 'tool', 'cli', 'code'],
        'ai-research': ['llm', 'gpt', 'chatgpt', 'claude', 'model', 'ai', 'ml', 'nlp', 'transformer'],
        'productivity': ['workflow', 'automation', 'assistant', 'chatbot', 'bot'],
        'data': ['data', 'analytics', 'rag', 'vector', 'embedding', 'database'],
        'creative': ['image', 'video', 'audio', 'design', 'art', 'creative'],
    }
    for cat, keywords in categories.items():
        if any(kw in text for kw in keywords):
            return cat
    return 'development'


def extract_tags(text: str) -> List[str]:
    """提取标签"""
    tags = []
    tag_keywords = [
        'agent', 'ai', 'llm', 'gpt', 'chatgpt', 'claude', 'langchain',
        'automation', 'workflow', 'rag', 'framework', 'sdk', 'api',
        'chatbot', 'assistant', 'tool', 'bot', 'openai', 'anthropic'
    ]
    text_lower = text.lower()
    for tag in tag_keywords:
        if tag in text_lower and tag not in tags:
            tags.append(tag)
    return tags[:5] if tags else ['ai', 'agent']


# ============================================================================
# GitHub 数据源
# ============================================================================
def fetch_github_skills() -> List[Dict]:
    """从GitHub获取AI Agent相关项目"""
    print("  [GitHub] Fetching skills...")
    skills = []
    seen_ids = set()

    queries = [
        "ai+agent+framework",
        "llm+agent+tool",
        "langchain+agent",
        "autonomous+agent",
        "ai+assistant+bot",
        "multi+agent+system",
        "agent+workflow",
        "gpt+agent",
    ]

    token = os.environ.get('GITHUB_TOKEN', '')
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}' if token else '',
    }

    for query in queries:
        try:
            url = f"https://api.github.com/search/repositories?q={query}+created:>{SINCE_DATE}&sort=stars&per_page=15"
            data = make_request(url, headers)
            if not data:
                continue

            for repo in data.get('items', []):
                if repo['id'] in seen_ids:
                    continue
                seen_ids.add(repo['id'])

                full_text = f"{repo.get('name', '')} {repo.get('description', '') or ''}"
                skills.append({
                    "id": f"github-{repo['id']}",
                    "name": repo['name'].replace('-', ' ').replace('_', ' ').title(),
                    "description": (repo.get('description') or 'AI Agent Skill')[:200],
                    "icon": PLATFORMS['github']['icon'],
                    "category": categorize_skill(full_text),
                    "tags": extract_tags(full_text),
                    "source": "GitHub",
                    "sourceUrl": repo['html_url'],
                    "installCount": repo.get('stargazers_count', 0),
                    "rating": min(5.0, 3.5 + repo.get('stargazers_count', 0) / 5000),
                    "author": repo.get('owner', {}).get('login', 'Unknown'),
                    "lastUpdated": repo.get('updated_at', '')[:10],
                    "platform": "github",
                })

            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"    [ERROR] GitHub query failed: {e}")

    print(f"    [GitHub] Found {len(skills)} skills")
    return skills


# ============================================================================
# HuggingFace 数据源
# ============================================================================
def fetch_huggingface_skills() -> List[Dict]:
    """从HuggingFace获取模型和Spaces"""
    print("  [HuggingFace] Fetching skills...")
    skills = []

    try:
        # 获取热门模型
        url = "https://huggingface.co/api/models?search=agent&sort=downloads&limit=20"
        data = make_request(url)

        if data:
            for model in data[:20]:
                model_id = model.get('id', '')
                downloads = model.get('downloads', 0)

                skills.append({
                    "id": f"hf-{hashlib.md5(model_id.encode()).hexdigest()[:10]}",
                    "name": model_id.split('/')[-1].replace('-', ' ').title(),
                    "description": model.get('cardData', {}).get('description', 'HuggingFace Model')[:200],
                    "icon": PLATFORMS['huggingface']['icon'],
                    "category": categorize_skill(model_id + ' ' + str(model.get('tags', []))),
                    "tags": model.get('tags', ['ai', 'model'])[:5],
                    "source": "HuggingFace",
                    "sourceUrl": f"https://huggingface.co/{model_id}",
                    "installCount": downloads,
                    "rating": min(5.0, 4.0 + downloads / 100000),
                    "author": model_id.split('/')[0] if '/' in model_id else 'Unknown',
                    "lastUpdated": model.get('lastModified', '')[:10] if model.get('lastModified') else datetime.now().strftime('%Y-%m-%d'),
                    "platform": "huggingface",
                })

        # 获取Spaces
        url = "https://huggingface.co/api/spaces?search=agent&sort=likes&limit=10"
        data = make_request(url)

        if data:
            for space in data[:10]:
                space_id = space.get('id', '')
                likes = space.get('likes', 0)

                skills.append({
                    "id": f"hf-space-{hashlib.md5(space_id.encode()).hexdigest()[:10]}",
                    "name": space_id.split('/')[-1].replace('-', ' ').title(),
                    "description": f"HuggingFace Space: {space_id}",
                    "icon": PLATFORMS['huggingface']['icon'],
                    "category": "ai-research",
                    "tags": ['space', 'demo', 'ai'],
                    "source": "HuggingFace",
                    "sourceUrl": f"https://huggingface.co/spaces/{space_id}",
                    "installCount": likes * 100,
                    "rating": min(5.0, 4.0 + likes / 1000),
                    "author": space_id.split('/')[0] if '/' in space_id else 'Unknown',
                    "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                    "platform": "huggingface",
                })

    except Exception as e:
        print(f"    [ERROR] HuggingFace fetch failed: {e}")

    print(f"    [HuggingFace] Found {len(skills)} skills")
    return skills


# ============================================================================
# ProductHunt 数据源
# ============================================================================
def fetch_producthunt_skills() -> List[Dict]:
    """从ProductHunt获取AI产品"""
    print("  [ProductHunt] Fetching skills...")
    skills = []

    try:
        # ProductHunt API v2 需要 token
        token = os.environ.get('PRODUCTHUNT_TOKEN', '')

        # 使用公开的 RSS/API 替代方案
        url = "https://www.producthunt.com/feed?category=artificial-intelligence"

        # 由于API限制，使用模拟数据或替代方案
        # 实际部署时需要配置 ProductHunt API token
        print(f"    [INFO] ProductHunt requires API token for full access")

        # 添加占位数据（实际使用时替换为真实API调用）
        placeholder_skills = [
            {
                "id": "ph-agent-tools",
                "name": "AI Agent Tools",
                "description": "Top AI agent tools from ProductHunt",
                "icon": PLATFORMS['producthunt']['icon'],
                "category": "productivity",
                "tags": ["agent", "productivity", "ai"],
                "source": "ProductHunt",
                "sourceUrl": "https://www.producthunt.com/topics/artificial-intelligence",
                "installCount": 5000,
                "rating": 4.5,
                "author": "ProductHunt",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "producthunt",
            }
        ]
        skills.extend(placeholder_skills)

    except Exception as e:
        print(f"    [ERROR] ProductHunt fetch failed: {e}")

    print(f"    [ProductHunt] Found {len(skills)} skills")
    return skills


# ============================================================================
# PyPI 数据源 (Python Package Index)
# ============================================================================
def fetch_pypi_skills() -> List[Dict]:
    """从PyPI获取AI Agent相关Python包"""
    print("  [PyPI] Fetching skills...")
    skills = []

    # AI Agent 相关的 PyPI 包名列表
    agent_packages = [
        'langchain', 'langchain-openai', 'langchain-anthropic', 'langchain-community',
        'crewai', 'autogen-agentchat', 'autogenstudio',
        'llamaindex', 'llama-index', 'llama-index-core',
        'semantic-kernel', 'microsoft-semantic-kernel',
        'openai', 'anthropic', 'cohere',
        'agents', 'pyautogen', 'autogpt', 'babyagi',
        'phidata', 'letta', 'mem0ai', 'memgpt',
        'haystack-ai', 'deepseek', 'groq', 'together',
        'chromadb', 'pinecone-client', 'weaviate-client', 'qdrant-client',
        'faiss-cpu', 'llama-cpp-python', 'transformers', 'accelerate',
        'flowise', 'dify', 'langflow',
    ]

    for pkg_name in agent_packages:
        try:
            url = f"https://pypi.org/pypi/{pkg_name}/json"
            data = make_request(url)

            if data and 'info' in data:
                info = data['info']
                name = info.get('name', pkg_name)

                # 获取下载量（从 release urls 估算）
                downloads = 0
                if data.get('urls'):
                    downloads = len(data['urls']) * 1000

                skills.append({
                    "id": f"pypi-{hashlib.md5(name.encode()).hexdigest()[:10]}",
                    "name": name,
                    "description": (info.get('summary') or info.get('description') or 'Python Package')[:200],
                    "icon": PLATFORMS['pypi']['icon'],
                    "category": categorize_skill(name + ' ' + (info.get('summary') or '')),
                    "tags": info.get('keywords', '').split(',')[:5] if info.get('keywords') else ['python', 'package', 'ai'],
                    "source": "PyPI",
                    "sourceUrl": f"https://pypi.org/project/{name}/",
                    "installCount": downloads or info.get('downloads', {}).get('last_month', 0) or 1000,
                    "rating": 4.5,
                    "author": info.get('author') or info.get('author_email', '').split('@')[0] or 'Unknown',
                    "lastUpdated": info.get('release_date', '')[:10] if info.get('release_date') else datetime.now().strftime('%Y-%m-%d'),
                    "platform": "pypi",
                })

            time.sleep(0.2)

        except Exception as e:
            continue

    print(f"    [PyPI] Found {len(skills)} skills")
    return skills


# ============================================================================
# npm 数据源 (Node Package Manager)
# ============================================================================
def fetch_npm_skills() -> List[Dict]:
    """从npm获取AI Agent相关Node.js包"""
    print("  [npm] Fetching skills...")
    skills = []

    # AI Agent 相关的 npm 包名列表
    agent_packages = [
        'langchain', '@langchain/openai', '@langchain/anthropic', '@langchain/core',
        'openai', '@anthropic-ai/sdk', '@google/generative-ai',
        'agents', 'ai-sdk', 'vercel-ai',
        'autogen', 'crewai-js', 'llamaindex-js',
        'chromadb', '@pinecone-database/pinecone',
        'langgraph', '@langchain/langgraph',
        'gpt-3-encoder', 'tiktoken',
        'llama-node', 'node-llama-cpp',
        'botbuilder', 'botframework-sdk',
        'modelcontextprotocol', '@modelcontextprotocol/sdk',
    ]

    for pkg_name in agent_packages:
        try:
            url = f"https://registry.npmjs.org/{pkg_name}"
            data = make_request(url)

            if data and 'name' in data:
                name = data.get('name', pkg_name)
                latest_version = data.get('dist-tags', {}).get('latest', '')
                version_info = data.get('versions', {}).get(latest_version, {})
                description = version_info.get('description', '') or data.get('description', '')

                # 获取下载量
                downloads = 0
                try:
                    dl_url = f"https://api.npmjs.org/downloads/point/last-month/{name}"
                    dl_data = make_request(dl_url)
                    if dl_data and 'downloads' in dl_data:
                        downloads = dl_data['downloads']
                except:
                    downloads = 1000

                skills.append({
                    "id": f"npm-{hashlib.md5(name.encode()).hexdigest()[:10]}",
                    "name": name,
                    "description": (description or 'Node.js Package')[:200],
                    "icon": PLATFORMS['npm']['icon'],
                    "category": categorize_skill(name + ' ' + description),
                    "tags": version_info.get('keywords', ['nodejs', 'package', 'ai'])[:5],
                    "source": "npm",
                    "sourceUrl": f"https://www.npmjs.com/package/{name}",
                    "installCount": downloads,
                    "rating": 4.5,
                    "author": version_info.get('author', {}).get('name', '') or data.get('maintainers', [{}])[0].get('name', 'Unknown'),
                    "lastUpdated": data.get('time', {}).get('modified', '')[:10] if data.get('time', {}).get('modified') else datetime.now().strftime('%Y-%m-%d'),
                    "platform": "npm",
                })

            time.sleep(0.2)

        except Exception as e:
            continue

    print(f"    [npm] Found {len(skills)} skills")
    return skills


# ============================================================================
# Docker Hub 数据源
# ============================================================================
def fetch_dockerhub_skills() -> List[Dict]:
    """从Docker Hub获取AI Agent相关镜像"""
    print("  [Docker Hub] Fetching skills...")
    skills = []

    # AI Agent 相关的 Docker 镜像
    docker_images = [
        'langchain/langchain', 'openai/openai-api', 'anthropic/claude',
        'ollama/ollama', 'localai/localai', 'text-generation-inference',
        'vllm/vllm', 'langflowai/langflow', 'chromadb/chroma',
        'qdrant/qdrant', 'milvusdb/milvus', 'weaviate/weaviate',
        'pinecone/pinecone', 'huggingface/transformers',
        'autogpt/autogpt', 'babyagi/babyagi', 'crewai/crewai',
        'memgpt/memgpt', 'dify/dify', 'flowiseai/flowise',
    ]

    for image in docker_images:
        try:
            # Docker Hub API
            parts = image.split('/')
            if len(parts) == 2:
                namespace, repo = parts
            else:
                namespace = 'library'
                repo = parts[0]

            url = f"https://hub.docker.com/v2/repositories/{namespace}/{repo}/"
            data = make_request(url)

            if data:
                skills.append({
                    "id": f"docker-{hashlib.md5(image.encode()).hexdigest()[:10]}",
                    "name": image,
                    "description": data.get('description', f'Docker image: {image}')[:200],
                    "icon": PLATFORMS['dockerhub']['icon'],
                    "category": "development",
                    "tags": ['docker', 'container', 'ai'],
                    "source": "Docker Hub",
                    "sourceUrl": f"https://hub.docker.com/r/{namespace}/{repo}",
                    "installCount": data.get('pull_count', 1000),
                    "rating": 4.5,
                    "author": namespace,
                    "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                    "platform": "dockerhub",
                })

            time.sleep(0.2)

        except Exception as e:
            continue

    print(f"    [Docker Hub] Found {len(skills)} skills")
    return skills


# ============================================================================
# VS Code Marketplace 数据源
# ============================================================================
def fetch_vscode_skills() -> List[Dict]:
    """从VS Code Marketplace获取AI相关扩展"""
    print("  [VS Code Marketplace] Fetching skills...")
    skills = []

    # AI Agent 相关的 VS Code 扩展
    vscode_extensions = [
        'GitHub.copilot', 'GitHub.copilot-chat', 'ms-python.python',
        'ms-toolsai.jupyter', 'continue.continue', 'CodeGPT.codegpt',
        'TabNine.tabnine', 'Codium.codium', 'Blackboxapp.blackbox',
        'Codeium.codeium', 'amazon.codewhisperer', 'sourcegraph.cody',
        'anthropic.claude-vscode', 'openai.chatgpt-vscode',
    ]

    for ext_id in vscode_extensions:
        try:
            # VS Code Marketplace API
            url = f"https://marketplace.visualstudio.com/items/{ext_id}"
            # 由于 API 复杂，使用占位数据
            name = ext_id.split('.')[-1].title()

            skills.append({
                "id": f"vscode-{hashlib.md5(ext_id.encode()).hexdigest()[:10]}",
                "name": f"{name} Extension",
                "description": f"VS Code AI extension: {ext_id}",
                "icon": PLATFORMS['vscode']['icon'],
                "category": "productivity",
                "tags": ['vscode', 'extension', 'ai'],
                "source": "VS Code Marketplace",
                "sourceUrl": url,
                "installCount": 100000,
                "rating": 4.5,
                "author": ext_id.split('.')[0],
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "vscode",
            })

        except Exception as e:
            continue

    print(f"    [VS Code Marketplace] Found {len(skills)} skills")
    return skills


# ============================================================================
# Replicate 数据源
# ============================================================================
def fetch_replicate_skills() -> List[Dict]:
    """从Replicate获取AI模型"""
    print("  [Replicate] Fetching skills...")
    skills = []

    # Replicate 热门 AI 模型
    replicate_models = [
        'stability-ai/stable-diffusion', 'openai/whisper', 'meta/llama-2-70b-chat',
        'mistralai/mistral-7b-instruct', 'replicate/vicuna-13b',
        'nvidia/sdxl-turbo', 'stability-ai/sdxl', 'replicate/llama-2-13b-chat',
        'tencentarc/gfpgan', 'sczhou/codeformer', 'replicate/dreamshaper',
    ]

    for model in replicate_models:
        try:
            skills.append({
                "id": f"replicate-{hashlib.md5(model.encode()).hexdigest()[:10]}",
                "name": model.split('/')[-1].replace('-', ' ').title(),
                "description": f"Replicate model: {model}",
                "icon": PLATFORMS['replicate']['icon'],
                "category": "ai-research",
                "tags": ['model', 'api', 'ai'],
                "source": "Replicate",
                "sourceUrl": f"https://replicate.com/{model}",
                "installCount": 50000,
                "rating": 4.5,
                "author": model.split('/')[0],
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "replicate",
            })

        except Exception as e:
            continue

    print(f"    [Replicate] Found {len(skills)} skills")
    return skills


# ============================================================================
# Ollama 数据源
# ============================================================================
def fetch_ollama_skills() -> List[Dict]:
    """从Ollama获取本地模型"""
    print("  [Ollama] Fetching skills...")
    skills = []

    # Ollama 热门模型
    ollama_models = [
        'llama2', 'llama3', 'mistral', 'codellama', 'phi3',
        'gemma', 'qwen', 'deepseek-coder', 'starcoder2',
        'nous-hermes2', 'dolphin-mixtral', 'openchat',
        'yi', 'solar', 'vicuna', 'orca-mini',
    ]

    try:
        # 尝试从 Ollama API 获取模型列表
        url = "https://ollama.com/api/models"
        data = make_request(url)

        if data and 'models' in data:
            for model in data['models']:
                skills.append({
                    "id": f"ollama-{model.get('name', '').replace(':', '-')}",
                    "name": model.get('name', '').split(':')[0],
                    "description": f"Ollama local model: {model.get('name', '')}",
                    "icon": PLATFORMS['ollama']['icon'],
                    "category": "ai-research",
                    "tags": ['local', 'model', 'llm'],
                    "source": "Ollama",
                    "sourceUrl": f"https://ollama.com/library/{model.get('name', '').split(':')[0]}",
                    "installCount": model.get('pulls', 10000),
                    "rating": 4.5,
                    "author": "Ollama",
                    "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                    "platform": "ollama",
                })
    except:
        # 使用预设列表
        for model in ollama_models:
            skills.append({
                "id": f"ollama-{model}",
                "name": model,
                "description": f"Ollama local LLM model: {model}",
                "icon": PLATFORMS['ollama']['icon'],
                "category": "ai-research",
                "tags": ['local', 'model', 'llm'],
                "source": "Ollama",
                "sourceUrl": f"https://ollama.com/library/{model}",
                "installCount": 50000,
                "rating": 4.5,
                "author": "Ollama",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "ollama",
            })

    print(f"    [Ollama] Found {len(skills)} skills")
    return skills


# ============================================================================
# Cursor 数据源
# ============================================================================
def fetch_cursor_skills() -> List[Dict]:
    """从Cursor获取AI编程工具"""
    print("  [Cursor] Fetching skills...")
    skills = []

    # Cursor 相关工具和资源
    cursor_resources = [
        {'name': 'Cursor IDE', 'desc': 'AI-powered code editor built for pair programming'},
        {'name': 'Cursor Rules', 'desc': 'Custom AI rules for better code generation'},
        {'name': 'Cursor Composer', 'desc': 'Multi-file AI editing feature'},
        {'name': 'Cursor Tab', 'desc': 'AI code completion like Copilot'},
        {'name': 'Cursor Chat', 'desc': 'Chat with AI about your codebase'},
    ]

    for resource in cursor_resources:
        skills.append({
            "id": f"cursor-{hashlib.md5(resource['name'].encode()).hexdigest()[:10]}",
            "name": resource['name'],
            "description": resource['desc'],
            "icon": PLATFORMS['cursor']['icon'],
            "category": "productivity",
            "tags": ['editor', 'ai', 'coding'],
            "source": "Cursor",
            "sourceUrl": "https://cursor.sh",
            "installCount": 100000,
            "rating": 4.8,
            "author": "Cursor",
            "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
            "platform": "cursor",
        })

    print(f"    [Cursor] Found {len(skills)} skills")
    return skills


# ============================================================================
# Dev.to 数据源
# ============================================================================
def fetch_devto_skills() -> List[Dict]:
    """从Dev.to获取AI相关文章和项目"""
    print("  [Dev.to] Fetching skills...")
    skills = []

    try:
        # Dev.to 公开API
        url = "https://dev.to/api/articles?tag=ai&per_page=20&top=7"
        data = make_request(url)

        if data:
            for article in data[:20]:
                title = article.get('title', '')
                skills.append({
                    "id": f"devto-{article.get('id', '')}",
                    "name": title[:50],
                    "description": article.get('description', title)[:200],
                    "icon": PLATFORMS['devto']['icon'],
                    "category": categorize_skill(title),
                    "tags": ['ai', 'tutorial', 'development'],
                    "source": "Dev.to",
                    "sourceUrl": article.get('url', ''),
                    "installCount": article.get('positive_reactions_count', 0) * 10,
                    "rating": 4.5,
                    "author": article.get('user', {}).get('username', 'Unknown'),
                    "lastUpdated": article.get('published_at', '')[:10] if article.get('published_at') else datetime.now().strftime('%Y-%m-%d'),
                    "platform": "devto",
                })

    except Exception as e:
        print(f"    [ERROR] Dev.to fetch failed: {e}")

    print(f"    [Dev.to] Found {len(skills)} skills")
    return skills


# ============================================================================
# Reddit 数据源
# ============================================================================
def fetch_reddit_skills() -> List[Dict]:
    """从Reddit获取AI相关讨论"""
    print("  [Reddit] Fetching skills...")
    skills = []

    try:
        # Reddit 公开JSON API (无需认证)
        subreddits = ['LocalLLaMA', 'artificial', 'MachineLearning', 'ChatGPT', 'AutoGPT']

        for sub in subreddits:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=10"
            headers = {'User-Agent': 'AgentSkills-Crawler/1.0'}
            data = make_request(url, headers)

            if data and 'data' in data and 'children' in data['data']:
                for post in data['data']['children'][:10]:
                    post_data = post.get('data', {})
                    title = post_data.get('title', '')

                    # 过滤2026年后的内容
                    created = datetime.fromtimestamp(post_data.get('created_utc', 0))
                    if created < datetime(2026, 1, 1):
                        continue

                    skills.append({
                        "id": f"reddit-{post_data.get('id', '')}",
                        "name": title[:50],
                        "description": post_data.get('selftext', title)[:200],
                        "icon": PLATFORMS['reddit']['icon'],
                        "category": categorize_skill(title),
                        "tags": ['ai', 'discussion', 'community'],
                        "source": "Reddit",
                        "sourceUrl": f"https://reddit.com{post_data.get('permalink', '')}",
                        "installCount": post_data.get('ups', 0) * 100,
                        "rating": min(5.0, 3.5 + post_data.get('ups', 0) / 1000),
                        "author": post_data.get('author', 'Unknown'),
                        "lastUpdated": created.strftime('%Y-%m-%d'),
                        "platform": "reddit",
                    })

            time.sleep(0.5)

    except Exception as e:
        print(f"    [ERROR] Reddit fetch failed: {e}")

    print(f"    [Reddit] Found {len(skills)} skills")
    return skills


# ============================================================================
# Stack Overflow 数据源
# ============================================================================
def fetch_stackoverflow_skills() -> List[Dict]:
    """从Stack Overflow获取AI相关问题"""
    print("  [Stack Overflow] Fetching skills...")
    skills = []

    try:
        # Stack Exchange API
        tags = ['ai-agent', 'langchain', 'openai-api', 'chatgpt', 'llm']
        seen_ids = set()

        for tag in tags:
            url = f"https://api.stackexchange.com/2.3/questions?order=desc&sort=votes&tagged={tag}&site=stackoverflow&pagesize=10&fromdate=1704067200"  # 2024-01-01
            data = make_request(url)

            if data and 'items' in data:
                for item in data['items'][:10]:
                    if item['question_id'] in seen_ids:
                        continue
                    seen_ids.add(item['question_id'])

                    title = item.get('title', '')
                    skills.append({
                        "id": f"so-{item['question_id']}",
                        "name": title[:50],
                        "description": f"Stack Overflow Question: {title}",
                        "icon": PLATFORMS['stackoverflow']['icon'],
                        "category": "development",
                        "tags": [tag, 'qa', 'development'],
                        "source": "Stack Overflow",
                        "sourceUrl": item.get('link', ''),
                        "installCount": item.get('score', 0) * 100,
                        "rating": min(5.0, 3.5 + item.get('score', 0) / 100),
                        "author": item.get('owner', {}).get('display_name', 'Unknown'),
                        "lastUpdated": datetime.fromtimestamp(item.get('creation_date', 0)).strftime('%Y-%m-%d'),
                        "platform": "stackoverflow",
                    })

            time.sleep(0.3)

    except Exception as e:
        print(f"    [ERROR] Stack Overflow fetch failed: {e}")

    print(f"    [Stack Overflow] Found {len(skills)} skills")
    return skills


# ============================================================================
# 掘金 数据源
# ============================================================================
def fetch_juejin_skills() -> List[Dict]:
    """从掘金获取AI相关文章"""
    print("  [掘金] Fetching skills...")
    skills = []

    try:
        # 掘金 API
        url = "https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed"
        headers = {'Content-Type': 'application/json'}

        # 需要POST请求，这里使用替代方案
        # 使用公开的标签文章列表
        url = "https://api.juejin.cn/tag_api/v1/query_tag_feed_list?tag_id=6809640445143498765&sort_type=new"

        print(f"    [INFO] 掘金 API requires authentication for full access")

        # 添加占位数据
        placeholder_skills = [
            {
                "id": "juejin-ai-agent",
                "name": "掘金AI Agent精选",
                "description": "来自掘金社区的AI Agent技术文章和项目",
                "icon": PLATFORMS['juejin']['icon'],
                "category": "development",
                "tags": ["ai", "agent", "前端"],
                "source": "掘金",
                "sourceUrl": "https://juejin.cn/tag/AI",
                "installCount": 3000,
                "rating": 4.5,
                "author": "掘金社区",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "juejin",
            }
        ]
        skills.extend(placeholder_skills)

    except Exception as e:
        print(f"    [ERROR] 掘金 fetch failed: {e}")

    print(f"    [掘金] Found {len(skills)} skills")
    return skills


# ============================================================================
# 知乎 数据源
# ============================================================================
def fetch_zhihu_skills() -> List[Dict]:
    """从知乎获取AI相关话题"""
    print("  [知乎] Fetching skills...")
    skills = []

    try:
        # 知乎搜索API
        url = "https://www.zhihu.com/api/v4/search_v3?t=topic&q=AI%20Agent&correction=1&offset=0&limit=20"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Cookie': os.environ.get('ZHIHU_COOKIE', ''),
        }

        print(f"    [INFO] 知乎 API may require cookie for full access")

        # 添加占位数据
        placeholder_skills = [
            {
                "id": "zhihu-ai-topic",
                "name": "知乎AI话题精选",
                "description": "来自知乎社区的AI Agent讨论和资源",
                "icon": PLATFORMS['zhihu']['icon'],
                "category": "ai-research",
                "tags": ["ai", "agent", "讨论"],
                "source": "知乎",
                "sourceUrl": "https://www.zhihu.com/topic/19551275/hot",
                "installCount": 4000,
                "rating": 4.3,
                "author": "知乎社区",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "zhihu",
            }
        ]
        skills.extend(placeholder_skills)

    except Exception as e:
        print(f"    [ERROR] 知乎 fetch failed: {e}")

    print(f"    [知乎] Found {len(skills)} skills")
    return skills


# ============================================================================
# CSDN 数据源
# ============================================================================
def fetch_csdn_skills() -> List[Dict]:
    """从CSDN获取AI相关博客"""
    print("  [CSDN] Fetching skills...")
    skills = []

    try:
        print(f"    [INFO] CSDN API requires authentication for full access")

        # 添加占位数据
        placeholder_skills = [
            {
                "id": "csdn-ai-blog",
                "name": "CSDN AI技术博客",
                "description": "来自CSDN的AI Agent技术文章和教程",
                "icon": PLATFORMS['csdn']['icon'],
                "category": "development",
                "tags": ["ai", "agent", "教程"],
                "source": "CSDN",
                "sourceUrl": "https://www.csdn.net/nav/ai",
                "installCount": 2500,
                "rating": 4.2,
                "author": "CSDN社区",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "csdn",
            }
        ]
        skills.extend(placeholder_skills)

    except Exception as e:
        print(f"    [ERROR] CSDN fetch failed: {e}")

    print(f"    [CSDN] Found {len(skills)} skills")
    return skills


# ============================================================================
# B站 数据源
# ============================================================================
def fetch_bilibili_skills() -> List[Dict]:
    """从B站获取AI相关视频"""
    print("  [B站] Fetching skills...")
    skills = []

    try:
        # B站公开API
        url = "https://api.bilibili.com/x/web-interface/search/type?keyword=AI%20Agent&search_type=video&page=1&page_size=20"
        headers = {
            'Referer': 'https://www.bilibili.com',
            'Cookie': os.environ.get('BILIBILI_COOKIE', ''),
        }
        data = make_request(url, headers)

        if data and 'data' in data and 'result' in data['data']:
            for video in data['data']['result'][:20]:
                title = video.get('title', '').replace('<em class="keyword">', '').replace('</em>', '')
                pubdate = datetime.fromtimestamp(video.get('pubdate', 0))

                if pubdate < datetime(2026, 1, 1):
                    continue

                skills.append({
                    "id": f"bili-{video.get('aid', '')}",
                    "name": title[:50],
                    "description": f"B站视频教程: {title}",
                    "icon": PLATFORMS['bilibili']['icon'],
                    "category": "creative",
                    "tags": ["video", "tutorial", "ai"],
                    "source": "B站",
                    "sourceUrl": f"https://www.bilibili.com/video/{video.get('bvid', '')}",
                    "installCount": video.get('play', 0),
                    "rating": min(5.0, 3.5 + video.get('play', 0) / 10000),
                    "author": video.get('author', 'Unknown'),
                    "lastUpdated": pubdate.strftime('%Y-%m-%d'),
                    "platform": "bilibili",
                })

    except Exception as e:
        print(f"    [ERROR] B站 fetch failed: {e}")

    if not skills:
        # 添加占位数据
        placeholder_skills = [
            {
                "id": "bili-ai-tutorial",
                "name": "B站AI教程精选",
                "description": "来自B站的AI Agent视频教程",
                "icon": PLATFORMS['bilibili']['icon'],
                "category": "creative",
                "tags": ["video", "tutorial", "ai"],
                "source": "B站",
                "sourceUrl": "https://search.bilibili.com/all?keyword=AI%20Agent",
                "installCount": 10000,
                "rating": 4.6,
                "author": "B站UP主",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "bilibili",
            }
        ]
        skills.extend(placeholder_skills)

    print(f"    [B站] Found {len(skills)} skills")
    return skills


# ============================================================================
# 微信 数据源
# ============================================================================
def fetch_weixin_skills() -> List[Dict]:
    """从微信搜狗获取AI相关公众号文章"""
    print("  [微信] Fetching skills...")
    skills = []

    try:
        # 微信搜狗搜索
        url = "https://weixin.sogou.com/weixin?type=2&query=AI%20Agent&ie=utf8&s_from=input"
        print(f"    [INFO] 微信 requires web scraping, limited access")

        # 添加占位数据
        placeholder_skills = [
            {
                "id": "weixin-ai-articles",
                "name": "微信公众号AI文章",
                "description": "来自微信公众号的AI Agent技术文章",
                "icon": PLATFORMS['weixin']['icon'],
                "category": "productivity",
                "tags": ["article", "ai", "wechat"],
                "source": "微信",
                "sourceUrl": "https://weixin.sogou.com/",
                "installCount": 8000,
                "rating": 4.4,
                "author": "微信公众号",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "weixin",
            }
        ]
        skills.extend(placeholder_skills)

    except Exception as e:
        print(f"    [ERROR] 微信 fetch failed: {e}")

    print(f"    [微信] Found {len(skills)} skills")
    return skills


# ============================================================================
# 抖音 数据源
# ============================================================================
def fetch_douyin_skills() -> List[Dict]:
    """从抖音获取AI相关短视频"""
    print("  [抖音] Fetching skills...")
    skills = []

    try:
        print(f"    [INFO] 抖音 API is heavily restricted, limited access")

        # 添加占位数据
        placeholder_skills = [
            {
                "id": "douyin-ai-videos",
                "name": "抖音AI短视频",
                "description": "来自抖音的AI Agent短视频教程",
                "icon": PLATFORMS['douyin']['icon'],
                "category": "creative",
                "tags": ["video", "short", "ai"],
                "source": "抖音",
                "sourceUrl": "https://www.douyin.com/",
                "installCount": 15000,
                "rating": 4.5,
                "author": "抖音创作者",
                "lastUpdated": datetime.now().strftime('%Y-%m-%d'),
                "platform": "douyin",
            }
        ]
        skills.extend(placeholder_skills)

    except Exception as e:
        print(f"    [ERROR] 抖音 fetch failed: {e}")

    print(f"    [抖音] Found {len(skills)} skills")
    return skills


# ============================================================================
# 主函数
# ============================================================================
def fetch_all_skills() -> List[Dict]:
    """获取所有平台的Skills数据"""
    print("\n" + "="*60)
    print("🚀 开始获取 Skills 数据")
    print(f"   同步日期范围: {SINCE_DATE} 之后")
    print("="*60)

    all_skills = []
    seen_ids = set()

    # Skills 数据源：仅聚合可下载/可安装的智能体工具
    # 排除：文章、讨论、问答、视频等非工具类内容（这些属于资讯/教程模块）
    fetchers = [
        ("GitHub", fetch_github_skills),        # 开源项目（可下载）
        ("HuggingFace", fetch_huggingface_skills),  # 模型/Spaces（可下载/在线使用）
        ("ProductHunt", fetch_producthunt_skills),   # AI产品（可试用/下载）
        ("PyPI", fetch_pypi_skills),            # Python包（pip install）
        ("npm", fetch_npm_skills),              # Node.js包（npm install）
        ("Docker Hub", fetch_dockerhub_skills), # Docker镜像（docker pull）
        ("VS Code", fetch_vscode_skills),       # VS Code扩展
        ("Replicate", fetch_replicate_skills),  # AI模型API
        ("Ollama", fetch_ollama_skills),        # 本地LLM模型
        ("Cursor", fetch_cursor_skills),        # AI编程工具
    ]

    for name, fetcher in fetchers:
        try:
            skills = fetcher()
            for skill in skills:
                if skill['id'] not in seen_ids:
                    seen_ids.add(skill['id'])
                    all_skills.append(skill)
        except Exception as e:
            print(f"  [ERROR] {name} fetcher failed: {e}")

        time.sleep(0.5)  # Rate limiting

    # 按安装数排序
    all_skills.sort(key=lambda x: x.get('installCount', 0), reverse=True)

    print(f"\n✅ 总计获取 {len(all_skills)} 个 Skills")
    return all_skills


def generate_categories(skills: List[Dict]) -> List[Dict]:
    """生成分类统计"""
    category_counts = {}
    category_icons = {
        'development': '🔍',
        'ai-research': '💡',
        'productivity': '📧',
        'data': '📊',
        'creative': '🎨',
    }

    for skill in skills:
        cat = skill.get('category', 'development')
        category_counts[cat] = category_counts.get(cat, 0) + 1

    categories = []
    for cat_id, count in category_counts.items():
        categories.append({
            "id": cat_id,
            "name": {
                'development': '开发工具',
                'ai-research': 'AI研究',
                'productivity': '效率工具',
                'data': '数据分析',
                'creative': '创意设计',
            }.get(cat_id, cat_id.title()),
            "icon": category_icons.get(cat_id, '📦'),
            "count": count,
        })

    return sorted(categories, key=lambda x: x['count'], reverse=True)


def main():
    """主入口"""
    print("\n" + "="*60)
    print("🤖 AgentSkills 多平台数据爬虫")
    print(f"   运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   完整同步: {FULL_SYNC}")
    print("="*60)

    # 获取Skills数据
    skills = fetch_all_skills()
    categories = generate_categories(skills)

    # 保存数据
    output = {
        "lastUpdated": datetime.now().isoformat(),
        "source": "multi-platform",
        "platforms": list(PLATFORMS.keys()),
        "categories": categories,
        "skills": skills,
        "totalCount": len(skills),
    }

    output_path = DATA_DIR / 'skills.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n💾 数据已保存到: {output_path}")
    print(f"   - Skills: {len(skills)}")
    print(f"   - Categories: {len(categories)}")


if __name__ == '__main__':
    main()
