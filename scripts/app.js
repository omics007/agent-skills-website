/**
 * Agent Skills - Main Application
 * Single Page Application with Hash-based Routing
 */

// ==========================================================================
// Mock Data
// ==========================================================================

const SKILLS_DATA = [
    {
        id: 'skill-001',
        name: '智能邮件助手',
        description: '自动化邮件处理、分类、优先级排序和快速回复建议。整合GPT-4能力，智能理解邮件意图并生成专业回复。',
        icon: '📧',
        category: 'productivity',
        tags: ['AI', '效率', '自动化'],
        source: 'Coze官方',
        installCount: 156234,
        rating: 4.9,
        features: [
            '智能邮件分类与标签管理',
            '一键生成专业回复',
            '重要邮件提醒与跟进',
            '批量邮件处理自动化'
        ],
        usage: '安装后在邮件客户端启用插件即可使用。支持Gmail、Outlook、企业邮箱。'
    },
    {
        id: 'skill-002',
        name: '数据分析可视化',
        description: '上传CSV/Excel数据，自动生成交互式图表和数据洞察报告。支持折线图、柱状图、饼图、热力图等多种可视化类型。',
        icon: '📊',
        category: 'data',
        tags: ['数据', '可视化', 'AI'],
        source: 'DataMind Lab',
        installCount: 89345,
        rating: 4.7,
        features: [
            '自动识别数据类型',
            '智能选择最佳图表类型',
            '一键生成数据报告',
            '支持导出PNG/SVG/PDF'
        ],
        usage: '拖拽上传数据文件或粘贴数据文本，系统自动分析并生成可视化。'
    },
    {
        id: 'skill-003',
        name: '代码审查助手',
        description: '自动化代码审查工具，支持Python、JavaScript、TypeScript、Go等主流语言。检测Bug、安全漏洞和代码规范问题。',
        icon: '🔍',
        category: 'development',
        tags: ['开发', '代码审查', '安全'],
        source: 'DevOps Pro',
        installCount: 67289,
        rating: 4.8,
        features: [
            '多语言代码分析',
            '安全漏洞检测',
            '性能问题诊断',
            '代码风格建议'
        ],
        usage: '集成到CI/CD流程或作为本地CLI工具使用。'
    },
    {
        id: 'skill-004',
        name: '创意图像生成',
        description: '基于Stable Diffusion的AI图像生成工具，支持文生图、图生图、局部重绘等高级功能。',
        icon: '🎨',
        category: 'creative',
        tags: ['创意', '图像', 'AI'],
        source: 'ArtFlow Studio',
        installCount: 234567,
        rating: 4.6,
        features: [
            '多种风格预设',
            '高清图像输出',
            '批量生成模式',
            '自定义模型加载'
        ],
        usage: '输入描述文本，选择风格和参数，点击生成。支持中英文描述。'
    },
    {
        id: 'skill-005',
        name: '会议纪要助手',
        description: '自动转录会议内容，提取关键决策、待办事项和行动项。支持多语言实时翻译。',
        icon: '📝',
        category: 'productivity',
        tags: ['效率', '协作', 'AI'],
        source: 'TeamSync',
        installCount: 45678,
        rating: 4.5,
        features: [
            '语音转文字实时转录',
            '智能提取关键信息',
            '自动生成会议摘要',
            '任务分配与提醒'
        ],
        usage: '导入会议录音或连接实时会议，系统自动处理并生成纪要。'
    },
    {
        id: 'skill-006',
        name: 'Prompt工程助手',
        description: '优化你的AI Prompt，提升ChatGPT、Claude等模型的输出质量。提供模板库和最佳实践指南。',
        icon: '💡',
        category: 'ai-research',
        tags: ['AI', 'Prompt', '效率'],
        source: 'PromptLab',
        installCount: 189432,
        rating: 4.9,
        features: [
            'Prompt优化建议',
            '模板库与分类',
            '链式思考模板',
            '角色扮演预设'
        ],
        usage: '输入你的原始Prompt，系统分析并提供优化建议。'
    },
    {
        id: 'skill-007',
        name: '社交媒体管理器',
        description: '一键发布内容到多个平台，智能分析数据表现，生成内容策略建议。',
        icon: '📱',
        category: 'productivity',
        tags: ['社交', '运营', '自动化'],
        source: 'SocialBoost',
        installCount: 34567,
        rating: 4.4,
        features: [
            '多平台一键发布',
            '内容日历管理',
            '数据分析仪表板',
            '粉丝互动分析'
        ],
        usage: '连接社交账号，创建内容，设置发布时间，自动化发布。'
    },
    {
        id: 'skill-008',
        name: '简历优化器',
        description: '分析简历内容，提供ATS友好度评分和改进建议。自动匹配热门职位要求。',
        icon: '📄',
        category: 'productivity',
        tags: ['求职', '效率', 'AI'],
        source: 'CareerPro',
        installCount: 78923,
        rating: 4.7,
        features: [
            'ATS评分分析',
            '关键词优化',
            '职位匹配推荐',
            '面试问题预测'
        ],
        usage: '上传简历或粘贴内容，系统分析并提供优化报告。'
    },
    {
        id: 'skill-009',
        name: 'API文档生成器',
        description: '自动从代码注释和接口定义生成标准API文档。支持Swagger、OpenAPI格式。',
        icon: '📚',
        category: 'development',
        tags: ['开发', '文档', '自动化'],
        source: 'DocuGen',
        installCount: 23456,
        rating: 4.6,
        features: [
            '多语言支持',
            '标准格式输出',
            '交互式预览',
            '团队协作功能'
        ],
        usage: '上传代码仓库或指定文件路径，自动生成文档。'
    },
    {
        id: 'skill-010',
        name: '法律文书助手',
        description: '辅助起草合同、协议、法律意见书等法律文书。提供条款库和风险提示。',
        icon: '⚖️',
        category: 'ai-research',
        tags: ['法律', '文档', 'AI'],
        source: 'LegalTech AI',
        installCount: 12345,
        rating: 4.5,
        features: [
            '合同模板库',
            '条款风险评估',
            '合规性检查',
            '多语言支持'
        ],
        usage: '选择文书类型，填写基本信息，系统生成初稿供审核。'
    },
    {
        id: 'skill-011',
        name: '视频剪辑助手',
        description: 'AI驱动的视频剪辑工具，支持自动剪辑、字幕生成、特效添加等功能。',
        icon: '🎬',
        category: 'creative',
        tags: ['视频', '创意', 'AI'],
        source: 'ClipMaster',
        installCount: 56789,
        rating: 4.6,
        features: [
            '自动剪辑精彩片段',
            '智能字幕生成',
            '背景音乐推荐',
            '多平台尺寸适配'
        ],
        usage: '上传视频素材，描述需求，AI自动剪辑生成成品。'
    },
    {
        id: 'skill-012',
        name: '竞争对手分析',
        description: '深度分析竞争对手的产品、营销、用户评价等维度，提供战略建议。',
        icon: '🔎',
        category: 'data',
        tags: ['商业', '分析', '战略'],
        source: 'BizInsight',
        installCount: 34567,
        rating: 4.5,
        features: [
            '多维度对比分析',
            '市场趋势洞察',
            'SWOT分析生成',
            '竞品动态追踪'
        ],
        usage: '输入竞品信息或选择行业，系统自动收集数据并分析。'
    },
    {
        id: 'skill-013',
        name: '代码翻译器',
        description: '在多种编程语言之间转换代码，保持逻辑和注释的一致性。',
        icon: '🔄',
        category: 'development',
        tags: ['开发', '代码', '效率'],
        source: 'CodeTrans',
        installCount: 45678,
        rating: 4.7,
        features: [
            '主流语言覆盖',
            '注释智能翻译',
            '语法检查修正',
            '最佳实践适配'
        ],
        usage: '粘贴源代码，选择目标语言，获取翻译后的代码。'
    },
    {
        id: 'skill-014',
        name: '品牌文案生成',
        description: '为品牌生成slogan、广告语、产品描述等营销内容。多种风格可选。',
        icon: '✍️',
        category: 'creative',
        tags: ['文案', '营销', '创意'],
        source: 'CopyGenius',
        installCount: 98765,
        rating: 4.8,
        features: [
            '多风格文案生成',
            'A/B测试版本',
            'SEO优化建议',
            '品牌调性学习'
        ],
        usage: '描述品牌信息和需求，选择文案风格，生成多种方案。'
    },
    {
        id: 'skill-015',
        name: '模型微调助手',
        description: '简化大语言模型微调流程，自动处理数据、训练、评估和部署。',
        icon: '🧠',
        category: 'ai-research',
        tags: ['AI', '机器学习', '开发'],
        source: 'MLOps Pro',
        installCount: 23456,
        rating: 4.6,
        features: [
            '数据预处理自动化',
            '超参数调优',
            '训练过程监控',
            '一键部署上线'
        ],
        usage: '上传训练数据和基础模型，配置参数，启动自动化训练流程。'
    },
    {
        id: 'skill-016',
        name: '知识库问答',
        description: '基于私有知识库构建智能问答系统，支持文档检索和多轮对话。',
        icon: '🤖',
        category: 'ai-research',
        tags: ['AI', '知识库', 'RAG'],
        source: 'KnowledgeBase AI',
        installCount: 67890,
        rating: 4.7,
        features: [
            '多格式文档支持',
            '语义检索增强',
            '上下文理解',
            '私有化部署'
        ],
        usage: '上传文档构建知识库，即可开始智能问答。'
    }
];

const NEWS_DATA = [
    {
        id: 'news-001',
        title: 'OpenAI发布GPT-5：Agent能力全面升级，自主执行能力提升300%',
        summary: 'OpenAI在今日凌晨的发布会上展示了GPT-5的多项突破性能力，特别是在Agent领域的应用。新模型支持多步骤任务分解、工具调用和持续学习。',
        source: 'AI科技前沿',
        date: '2024-01-15',
        category: '行业动态',
        url: '#'
    },
    {
        id: 'news-002',
        title: 'Anthropic推出Claude 3.5 Agent SDK，支持复杂任务自动化',
        summary: 'Anthropic发布了全新的Agent开发工具包，使开发者能够更轻松地构建基于Claude的智能代理应用。新SDK提供了完善的工具调用和记忆管理能力。',
        source: '机器之心',
        date: '2024-01-12',
        category: '技术发布',
        url: '#'
    },
    {
        id: 'news-003',
        title: '微软Copilot全面升级：Windows系统级Agent即将到来',
        summary: '微软在Build大会上宣布，Copilot将深度集成到Windows系统中，用户可通过自然语言控制整个操作系统。这意味着AI Agent将真正成为用户的数字助手。',
        source: '36氪',
        date: '2024-01-10',
        category: '企业动态',
        url: '#'
    },
    {
        id: 'news-004',
        title: '全球AI Agent市场规模预计2025年突破500亿美元',
        summary: '据市场研究机构最新报告，AI Agent市场正经历爆发式增长。企业级应用成为主要驱动力，自动化办公、智能客服、数据分析等领域需求旺盛。',
        source: '第一财经',
        date: '2024-01-08',
        category: '市场分析',
        url: '#'
    },
    {
        id: 'news-005',
        title: '斯坦福发布AI Agent安全评估框架，15项核心能力标准化',
        summary: '斯坦福大学HAI研究院发布了首个AI Agent安全与能力评估框架，为行业提供了统一的评测标准。框架涵盖规划、推理、工具使用、记忆等核心能力。',
        source: '学术前沿',
        date: '2024-01-05',
        category: '学术研究',
        url: '#'
    },
    {
        id: 'news-006',
        title: 'Google DeepMind展示Gemini 2.0 Agent：多模态交互新时代',
        summary: 'DeepMind展示了基于Gemini 2.0的多模态Agent原型，能够同时理解和处理文本、图像、音频和视频内容，并在复杂任务中展现出卓越的推理能力。',
        source: 'AI深度观察',
        date: '2024-01-03',
        category: '技术发布',
        url: '#'
    }
];

const TUTORIALS_DATA = [
    {
        id: 'tutorial-001',
        title: '从零构建你的第一个AI Agent',
        description: '本教程将手把手教你使用Python构建一个完整的AI Agent，包括任务规划、工具调用和记忆管理。适合零基础入门者。',
        icon: '🚀',
        difficulty: 'beginner',
        duration: '45分钟',
        category: '入门指南'
    },
    {
        id: 'tutorial-002',
        title: '深入理解ReAct范式：让Agent像人类一样思考',
        description: '详细讲解ReAct（Reasoning + Acting）推理框架的原理和实现，通过案例展示如何在Agent中应用这一范式提升任务完成率。',
        icon: '🧠',
        difficulty: 'intermediate',
        duration: '60分钟',
        category: '核心概念'
    },
    {
        id: 'tutorial-003',
        title: '构建多模态Agent：处理图像、音频和视频',
        description: '学习如何构建支持多模态输入的Agent系统，涵盖视觉理解、语音识别、视频分析等关键技术。',
        icon: '👁️',
        difficulty: 'advanced',
        duration: '90分钟',
        category: '高级特性'
    },
    {
        id: 'tutorial-004',
        title: 'Agent Memory System设计与实现',
        description: '深入探讨Agent的记忆系统设计，包括短期记忆、长期记忆、向量数据库集成和记忆检索策略。',
        icon: '💾',
        difficulty: 'intermediate',
        duration: '75分钟',
        category: '核心概念'
    },
    {
        id: 'tutorial-005',
        title: '企业级Agent架构设计与最佳实践',
        description: '分享构建生产级Agent系统的架构设计经验，涵盖可扩展性、安全性、监控和容错机制。',
        icon: '🏢',
        difficulty: 'advanced',
        duration: '120分钟',
        category: '工程实践'
    },
    {
        id: 'tutorial-006',
        title: 'Tool Learning：让Agent学会使用工具',
        description: '系统讲解如何让Agent学习使用各种工具，包括API调用、代码执行、文件操作等，以及工具选择策略。',
        icon: '🔧',
        difficulty: 'intermediate',
        duration: '60分钟',
        category: '核心概念'
    }
];

const CATEGORIES = [
    { id: 'productivity', name: '办公效率', icon: '⚡', count: 156 },
    { id: 'data', name: '数据分析', icon: '📊', count: 89 },
    { id: 'development', name: '编程开发', icon: '💻', count: 234 },
    { id: 'creative', name: '创意设计', icon: '🎨', count: 167 },
    { id: 'ai-research', name: 'AI研究', icon: '🤖', count: 98 }
];

// ==========================================================================
// State Management
// ==========================================================================

const state = {
    currentPage: 'home',
    currentSkillId: null,
    selectedCategory: null,
    searchQuery: '',
    skills: SKILLS_DATA,
    news: NEWS_DATA,
    tutorials: TUTORIALS_DATA,
    categories: CATEGORIES
};

// ==========================================================================
// Router
// ==========================================================================

function router() {
    const hash = window.location.hash || '#/';
    const path = hash.slice(1); // Remove #
    
    // Parse route
    if (path === '/' || path === '') {
        state.currentPage = 'home';
        state.currentSkillId = null;
        renderHome();
    } else if (path === '/skills') {
        state.currentPage = 'skills';
        state.currentSkillId = null;
        renderSkills();
    } else if (path === '/news') {
        state.currentPage = 'news';
        state.currentSkillId = null;
        renderNews();
    } else if (path === '/tutorials') {
        state.currentPage = 'tutorials';
        state.currentSkillId = null;
        renderTutorials();
    } else if (path.startsWith('/skill/')) {
        const skillId = path.replace('/skill/', '');
        state.currentPage = 'detail';
        state.currentSkillId = skillId;
        renderSkillDetail(skillId);
    } else {
        // 404 - redirect to home
        window.location.hash = '#/';
    }
    
    // Update active nav link
    updateActiveNav();
    
    // Scroll to top
    window.scrollTo(0, 0);
}

function updateActiveNav() {
    document.querySelectorAll('.nav-link, .mobile-link').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === state.currentPage) {
            link.classList.add('active');
        }
    });
}

// ==========================================================================
// Render Functions
// ==========================================================================

function renderHome() {
    const main = document.getElementById('mainContent');
    
    // Hero Section
    const heroSection = `
        <section class="hero">
            <div class="hero-content">
                <div class="hero-badge">
                    <span class="hero-badge-dot"></span>
                    汇聚1000+优质Agent Skills
                </div>
                <h1 class="hero-title">
                    <span class="hero-title-gradient">探索Agent Skills</span>
                </h1>
                <p class="hero-subtitle">
                    发现、体验来自全球开发者的前沿AI技能。让AI成为你最强大的助手。
                </p>
                <div class="hero-search">
                    <svg class="hero-search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="11" cy="11" r="8"/>
                        <path d="m21 21-4.35-4.35"/>
                    </svg>
                    <input type="text" class="hero-search-input" id="heroSearchInput" placeholder="搜索 Skills、资讯、教程...">
                    <button class="hero-search-btn" onclick="performSearch()">搜索</button>
                </div>
            </div>
        </section>
    `;
    
    // Categories Section
    const categoriesSection = `
        <section class="categories">
            <div class="section-container">
                <div class="section-header">
                    <h2 class="section-title">快速分类</h2>
                    <a href="#/skills" class="section-link">
                        查看全部
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M5 12h14M12 5l7 7-7 7"/>
                        </svg>
                    </a>
                </div>
                <div class="categories-grid">
                    ${state.categories.map(cat => `
                        <a href="#/skills?category=${cat.id}" class="category-card">
                            <div class="category-icon">${cat.icon}</div>
                            <span class="category-name">${cat.name}</span>
                            <span class="category-count">${cat.count}个Skills</span>
                        </a>
                    `).join('')}
                </div>
            </div>
        </section>
    `;
    
    // Featured Skills
    const featuredSkills = state.skills.slice(0, 8);
    const featuredSection = `
        <section class="skills-section">
            <div class="section-container">
                <div class="section-header">
                    <h2 class="section-title">热门Skills</h2>
                    <a href="#/skills" class="section-link">
                        浏览更多
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M5 12h14M12 5l7 7-7 7"/>
                        </svg>
                    </a>
                </div>
                <div class="skills-grid">
                    ${featuredSkills.map(skill => renderSkillCard(skill)).join('')}
                </div>
            </div>
        </section>
    `;
    
    // News Section
    const newsSection = `
        <section class="news-section">
            <div class="section-container">
                <div class="section-header">
                    <h2 class="section-title">最新资讯</h2>
                    <a href="#/news" class="section-link">
                        查看全部
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M5 12h14M12 5l7 7-7 7"/>
                        </svg>
                    </a>
                </div>
                <div class="news-grid">
                    ${state.news.slice(0, 4).map(news => renderNewsCard(news)).join('')}
                </div>
            </div>
        </section>
    `;
    
    main.innerHTML = heroSection + categoriesSection + featuredSection + newsSection;
    
    // Add event listener for hero search
    const heroInput = document.getElementById('heroSearchInput');
    if (heroInput) {
        heroInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
}

function renderSkills() {
    const main = document.getElementById('mainContent');
    
    // Filter skills based on category
    let filteredSkills = state.skills;
    if (state.selectedCategory) {
        filteredSkills = filteredSkills.filter(s => s.category === state.selectedCategory);
    }
    
    const html = `
        <div class="page-header">
            <h1 class="page-title">Skills市场</h1>
            <p class="page-subtitle">探索来自全球开发者的优质Agent技能，发现AI的无限可能</p>
        </div>
        
        <div class="filters-bar">
            <div class="filters-container">
                <div class="filter-group">
                    <span class="filter-label">分类</span>
                    <select class="filter-select" id="categoryFilter" onchange="filterByCategory(this.value)">
                        <option value="">全部分类</option>
                        ${state.categories.map(cat => `
                            <option value="${cat.id}" ${state.selectedCategory === cat.id ? 'selected' : ''}>${cat.name}</option>
                        `).join('')}
                    </select>
                </div>
                <div class="filter-tags">
                    <button class="filter-tag ${!state.selectedCategory ? 'active' : ''}" onclick="filterByCategory('')">全部</button>
                    ${state.categories.map(cat => `
                        <button class="filter-tag ${state.selectedCategory === cat.id ? 'active' : ''}" onclick="filterByCategory('${cat.id}')">${cat.name}</button>
                    `).join('')}
                </div>
                <span class="results-count">${filteredSkills.length} 个结果</span>
            </div>
        </div>
        
        <div class="skills-market-content">
            <div class="skills-grid">
                ${filteredSkills.map(skill => renderSkillCard(skill)).join('')}
            </div>
        </div>
    `;
    
    main.innerHTML = html;
}

function renderNews() {
    const main = document.getElementById('mainContent');
    
    const html = `
        <div class="page-header">
            <h1 class="page-title">资讯中心</h1>
            <p class="page-subtitle">追踪Agent领域最新动态，了解行业趋势和技术进展</p>
        </div>
        
        <div class="news-list">
            <div class="news-grid">
                ${state.news.map(news => renderNewsCard(news, true)).join('')}
            </div>
        </div>
    `;
    
    main.innerHTML = html;
}

function renderTutorials() {
    const main = document.getElementById('mainContent');
    
    const html = `
        <div class="page-header">
            <h1 class="page-title">教程中心</h1>
            <p class="page-subtitle">从入门到精通，系统学习Agent开发技能</p>
        </div>
        
        <div class="tutorials-list">
            <div class="tutorials-grid">
                ${state.tutorials.map(tutorial => renderTutorialCard(tutorial)).join('')}
            </div>
        </div>
    `;
    
    main.innerHTML = html;
}

function renderSkillDetail(skillId) {
    const skill = state.skills.find(s => s.id === skillId);
    if (!skill) {
        window.location.hash = '#/skills';
        return;
    }
    
    const main = document.getElementById('mainContent');
    
    // Get related skills (same category, different skill)
    const relatedSkills = state.skills
        .filter(s => s.category === skill.category && s.id !== skill.id)
        .slice(0, 3);
    
    const getTagClass = (tag) => {
        if (tag === 'AI' || tag === '机器学习' || tag === 'RAG') return 'tag-ai';
        if (tag === '开发' || tag === '代码' || tag === '安全') return 'tag-dev';
        if (tag === '效率' || tag === '自动化' || tag === '协作') return 'tag-productivity';
        return '';
    };
    
    const html = `
        <div class="detail-page">
            <div class="detail-hero">
                <div class="detail-container">
                    <div class="detail-header">
                        <div class="detail-icon">${skill.icon}</div>
                        <div class="detail-info">
                            <h1 class="detail-title">${skill.name}</h1>
                            <div class="detail-source">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                                </svg>
                                ${skill.source}
                            </div>
                            <div class="detail-tags">
                                ${skill.tags.map(tag => `<span class="skill-tag ${getTagClass(tag)}">${tag}</span>`).join('')}
                            </div>
                        </div>
                    </div>
                    <p class="detail-description">${skill.description}</p>
                    <div class="detail-actions">
                        <button class="btn btn-primary">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                            </svg>
                            安装Skill
                        </button>
                        <button class="btn btn-secondary">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8M16 6l-4-4-4 4M12 2v13"/>
                            </svg>
                            立即使用
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="detail-content">
                <div class="detail-main">
                    <div class="detail-section">
                        <h3 class="detail-section-title">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                            </svg>
                            核心功能
                        </h3>
                        <div class="features-list">
                            ${skill.features.map(feature => `
                                <div class="feature-item">
                                    <div class="feature-icon">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <polyline points="20,6 9,17 4,12"/>
                                        </svg>
                                    </div>
                                    <span class="feature-text">${feature}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div class="detail-section">
                        <h3 class="detail-section-title">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                                <polyline points="14,2 14,8 20,8"/>
                                <line x1="16" y1="13" x2="8" y2="13"/>
                                <line x1="16" y1="17" x2="8" y2="17"/>
                            </svg>
                            使用说明
                        </h3>
                        <div class="usage-content">
                            <p>${skill.usage}</p>
                        </div>
                    </div>
                </div>
                
                <div class="detail-sidebar">
                    <div class="sidebar-card">
                        <h4 class="sidebar-card-title">数据统计</h4>
                        <div class="stats-grid">
                            <div class="stat-item">
                                <div class="stat-value">${(skill.installCount / 1000).toFixed(1)}k</div>
                                <div class="stat-label">安装次数</div>
                            </div>
                            <div class="stat-item">
                                <div class="stat-value">${skill.rating}</div>
                                <div class="stat-label">评分</div>
                            </div>
                        </div>
                    </div>
                    
                    ${relatedSkills.length > 0 ? `
                        <div class="sidebar-card">
                            <h4 class="sidebar-card-title">相关Skills</h4>
                            <div class="related-skills">
                                ${relatedSkills.map(related => `
                                    <a href="#/skill/${related.id}" class="related-skill">
                                        <div class="related-skill-icon">${related.icon}</div>
                                        <div class="related-skill-info">
                                            <div class="related-skill-name">${related.name}</div>
                                            <div class="related-skill-source">${related.source}</div>
                                        </div>
                                    </a>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
    
    main.innerHTML = html;
}

// ==========================================================================
// Component Renderers
// ==========================================================================

function renderSkillCard(skill) {
    const getTagClass = (tag) => {
        if (tag === 'AI' || tag === '机器学习' || tag === 'RAG') return 'tag-ai';
        if (tag === '开发' || tag === '代码' || tag === '安全') return 'tag-dev';
        if (tag === '效率' || tag === '自动化' || tag === '协作') return 'tag-productivity';
        return '';
    };
    
    return `
        <article class="skill-card" onclick="window.location.hash='#/skill/${skill.id}'">
            <div class="skill-header">
                <div class="skill-icon">${skill.icon}</div>
                <div class="skill-info">
                    <h3 class="skill-name">${skill.name}</h3>
                    <span class="skill-source">${skill.source}</span>
                </div>
            </div>
            <p class="skill-description">${skill.description}</p>
            <div class="skill-tags">
                ${skill.tags.map(tag => `<span class="skill-tag ${getTagClass(tag)}">${tag}</span>`).join('')}
            </div>
            <div class="skill-footer">
                <div class="skill-stats">
                    <span class="skill-stat">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>
                        </svg>
                        ${(skill.installCount / 1000).toFixed(1)}k
                    </span>
                    <span class="skill-stat">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                            <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
                        </svg>
                        ${skill.rating}
                    </span>
                </div>
                <span class="skill-action">查看详情</span>
            </div>
        </article>
    `;
}

function renderNewsCard(news, full = false) {
    return `
        <article class="${full ? 'news-full-card' : 'news-card'}">
            <div class="news-image">📰</div>
            <div class="news-content">
                <span class="news-category">${news.category}</span>
                <h3 class="news-title">${news.title}</h3>
                <p class="news-summary">${news.summary}</p>
                <div class="news-meta">
                    <span>${news.source}</span>
                    <span>${news.date}</span>
                </div>
            </div>
        </article>
    `;
}

function renderTutorialCard(tutorial) {
    const difficultyClass = {
        'beginner': 'difficulty-beginner',
        'intermediate': 'difficulty-intermediate',
        'advanced': 'difficulty-advanced'
    };
    
    const difficultyText = {
        'beginner': '入门',
        'intermediate': '进阶',
        'advanced': '高级'
    };
    
    return `
        <article class="tutorial-card">
            <div class="tutorial-header">
                <div class="tutorial-icon">${tutorial.icon}</div>
                <div class="tutorial-meta">
                    <span class="tutorial-badge ${difficultyClass[tutorial.difficulty]}">${difficultyText[tutorial.difficulty]}</span>
                </div>
            </div>
            <h3 class="tutorial-title">${tutorial.title}</h3>
            <p class="tutorial-description">${tutorial.description}</p>
            <div class="tutorial-footer">
                <span class="tutorial-duration">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12,6 12,12 16,14"/>
                    </svg>
                    ${tutorial.duration}
                </span>
                <span>${tutorial.category}</span>
            </div>
        </article>
    `;
}

// ==========================================================================
// Search Functions
// ==========================================================================

function performSearch() {
    const heroInput = document.getElementById('heroSearchInput');
    const query = heroInput ? heroInput.value.trim() : '';
    
    if (query) {
        state.searchQuery = query;
        window.location.hash = '#/skills';
    }
}

function performSearchOverlay() {
    const searchInput = document.getElementById('searchInput');
    const query = searchInput.value.trim();
    const resultsContainer = document.getElementById('searchResults');
    
    if (!query) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    // Search in skills
    const matchedSkills = state.skills.filter(skill => 
        skill.name.includes(query) || 
        skill.description.includes(query) ||
        skill.tags.some(tag => tag.includes(query))
    ).slice(0, 5);
    
    // Search in news
    const matchedNews = state.news.filter(news =>
        news.title.includes(query) ||
        news.summary.includes(query)
    ).slice(0, 3);
    
    let html = '';
    
    if (matchedSkills.length > 0) {
        html += `<div class="search-section">
            <h4 class="search-section-title">Skills</h4>
            ${matchedSkills.map(skill => `
                <a href="#/skill/${skill.id}" class="search-result-item">
                    <span class="search-result-icon">${skill.icon}</span>
                    <div class="search-result-info">
                        <span class="search-result-name">${skill.name}</span>
                        <span class="search-result-meta">${skill.source}</span>
                    </div>
                </a>
            `).join('')}
        </div>`;
    }
    
    if (matchedNews.length > 0) {
        html += `<div class="search-section">
            <h4 class="search-section-title">资讯</h4>
            ${matchedNews.map(news => `
                <a href="#/news" class="search-result-item">
                    <span class="search-result-icon">📰</span>
                    <div class="search-result-info">
                        <span class="search-result-name">${news.title}</span>
                        <span class="search-result-meta">${news.source}</span>
                    </div>
                </a>
            `).join('')}
        </div>`;
    }
    
    if (!matchedSkills.length && !matchedNews.length) {
        html = `<div class="empty-state">
            <p>未找到与"${query}"相关的结果</p>
        </div>`;
    }
    
    resultsContainer.innerHTML = html;
}

// ==========================================================================
// Filter Functions
// ==========================================================================

function filterByCategory(category) {
    state.selectedCategory = category || null;
    renderSkills();
}

// ==========================================================================
// UI Interactions
// ==========================================================================

function initNavbar() {
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

function initMobileMenu() {
    const menuBtn = document.getElementById('navMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    let isOpen = false;
    
    menuBtn.addEventListener('click', () => {
        isOpen = !isOpen;
        mobileMenu.classList.toggle('open', isOpen);
        document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    
    // Close on link click
    mobileMenu.querySelectorAll('.mobile-link').forEach(link => {
        link.addEventListener('click', () => {
            isOpen = false;
            mobileMenu.classList.remove('open');
            document.body.style.overflow = '';
        });
    });
}

function initSearch() {
    const searchOverlay = document.getElementById('searchOverlay');
    const searchBtn = document.getElementById('navSearchBtn');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.getElementById('searchInput');
    
    // Open search
    searchBtn.addEventListener('click', () => {
        searchOverlay.classList.add('open');
        setTimeout(() => searchInput.focus(), 100);
        document.body.style.overflow = 'hidden';
    });
    
    // Close search
    searchClose.addEventListener('click', closeSearch);
    searchOverlay.addEventListener('click', (e) => {
        if (e.target === searchOverlay) {
            closeSearch();
        }
    });
    
    // Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchOverlay.classList.contains('open')) {
            closeSearch();
        }
    });
    
    function closeSearch() {
        searchOverlay.classList.remove('open');
        searchInput.value = '';
        document.getElementById('searchResults').innerHTML = '';
        document.body.style.overflow = '';
    }
    
    // Search input
    let debounceTimer;
    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(performSearchOverlay, 300);
    });
}

// ==========================================================================
// Initialize App
// ==========================================================================

function init() {
    // Initialize UI
    initNavbar();
    initMobileMenu();
    initSearch();
    
    // Initialize router
    window.addEventListener('hashchange', router);
    router();
}

// Start app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
