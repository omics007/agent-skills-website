# Agent Skills 聚合网站 - 设计规格文档

## 1. 概念与愿景

这是一个面向AI Agent开发者和使用者的技能市场聚合平台，灵感源自Elon Musk旗下品牌的极简未来美学。网站传递的感觉是：**来自未来的技术商店**——冷峻、高效、充满科技感，同时保持优雅的用户体验。如同走进特斯拉门店或SpaceX控制中心，每一个交互都在诉说：你正在使用人类最前沿的工具。

## 2. 设计语言

### 美学方向
- **核心参考**：Tesla官网 + SpaceX官网 + Neuralink品牌视觉
- **关键词**：暗黑、极简、未来感、玻璃态、精密仪器

### 色彩系统
```
--bg-primary: #0a0a0a          // 近乎纯黑的主背景
--bg-secondary: #111111        // 卡片/区块背景
--bg-tertiary: #1a1a1a         // 次级卡片/hover状态
--text-primary: #ffffff        // 主要文字
--text-secondary: #888888      // 次要文字
--text-muted: #555555          // 弱化文字
--accent-tesla: #e31937        // Tesla红（CTA按钮、强调）
--accent-spacex: #0057d9       // SpaceX蓝（次级强调）
--accent-neuralink: #8b5cf6    // Neuralink紫（AI相关标签）
--gradient-glow: linear-gradient(135deg, rgba(227,25,55,0.1), rgba(0,87,217,0.1))
--glass-bg: rgba(255,255,255,0.03)
--glass-border: rgba(255,255,255,0.08)
```

### 字体系统
- **主字体**：Inter（Google Fonts），weight: 300/400/500/600/700
- **备选**：system-ui, -apple-system, sans-serif
- **标题**：700 weight，大字号（48-72px），字间距 -0.02em
- **正文**：400 weight，16px，行高 1.6

### 空间系统
- **基础单位**：8px
- **页面边距**：桌面端 80px，移动端 24px
- **卡片间距**：24px
- **组件内边距**：24-32px
- **最大内容宽度**：1400px

### 动效哲学
- **核心原则**：克制但精致，如同精密机械的运转
- **入场动画**：fade-in + translateY(20px)，duration 600ms，ease-out
- **Hover效果**：
  - 卡片：translateY(-4px) + box-shadow增强，duration 300ms
  - 按钮：微发光（box-shadow glow），duration 200ms
  - 链接：下划线渐显
- **页面切换**：opacity fade，duration 300ms
- **加载动画**：简洁的脉冲点或旋转弧线

### 视觉资产策略
- **图标**：Lucide Icons（线性风格，stroke-width: 1.5）
- **装饰元素**：
  - 细线条渐变分隔符
  - 微妙的网格背景纹理
  - 玻璃态卡片（backdrop-filter: blur(20px)）
  - 角落的微弱光晕效果

## 3. 布局与结构

### 整体架构（单页应用）
```
┌─────────────────────────────────────┐
│  Navigation Bar (固定顶部)           │
├─────────────────────────────────────┤
│  Hero Section (首页特有)              │
│  - 全屏高度                           │
│  - 居中大标题                         │
│  - 搜索框                            │
├─────────────────────────────────────┤
│  Main Content Area                   │
│  - 根据路由切换                       │
│  - Skills市场 / 资讯 / 教程          │
├─────────────────────────────────────┤
│  Footer                              │
└─────────────────────────────────────┘
```

### 页面结构
1. **首页 (/)**
   - Hero：全屏，中心放射状光晕，大标题"探索Agent Skills"，副标题，搜索框
   - 快速分类入口：图标+文字横向排列
   - 热门Skills：3列卡片网格
   - 最新资讯：2列卡片预览

2. **Skills市场 (/skills)**
   - 顶部筛选栏：分类下拉、标签筛选、排序
   - 搜索结果/全部Skills列表
   - 网格布局：桌面4列，平板3列，手机2列
   - 无限滚动或分页

3. **Skill详情 (/skills/:id)**
   - 大标题 + 来源标签
   - 描述区域
   - 功能特性列表
   - 使用说明
   - 安装/使用按钮
   - 相关Skills推荐

4. **资讯中心 (/news)**
   - 分类标签
   - 卡片列表（图片+标题+摘要+时间）

5. **教程中心 (/tutorials)**
   - 分类导航
   - 教程卡片列表

### 响应式断点
- **Desktop**: > 1200px
- **Tablet**: 768px - 1200px
- **Mobile**: < 768px

## 4. 功能与交互

### 导航
- Logo + 网站名（左侧）
- 导航链接：首页、Skills市场、资讯、教程（中间）
- 搜索图标（右侧，移动端替代搜索框）
- 滚动时添加背景模糊

### 搜索
- 首页搜索：全站搜索，搜索Skills和资讯
- 实时搜索建议（下拉）
- 空状态：优雅的"未找到"提示

### Skills卡片交互
- **默认态**：玻璃态背景，细边框
- **Hover态**：
  - 背景微亮
  - 卡片上浮4px
  - 边框发光（accent色）
  - 显示"查看详情"按钮
- **点击**：跳转详情页

### 筛选与排序
- 下拉选择器（玻璃态样式）
- 多标签筛选（标签云，点击切换）
- 排序：最新、最热、字母序

### 页面切换
- 平滑淡入淡出
- 切换时顶部滚动到0
- 保持浏览历史（history API）

## 5. 组件清单

### Navigation
- **默认**：透明背景，白色文字
- **滚动后**：bg-secondary + backdrop-blur
- **移动端**：汉堡菜单，侧滑抽屉

### Hero Section
- 大标题：72px，白色，font-weight 700
- 副标题：20px，text-secondary
- 搜索框：玻璃态，圆角12px，搜索图标
- 背景：中心渐变光晕动画

### Skill Card
- **结构**：图标/LOGO + 标题 + 简介 + 标签 + 来源
- **尺寸**：宽度自适应，高度约280px
- **标签**：小圆角pill，深色背景+文字
- **来源**：左下角，小字灰色
- **状态**：
  - Default: bg-secondary, border glass
  - Hover: bg-tertiary, border-glow, lift
  - Active: scale 0.98

### Category Card
- 图标 + 名称
- 纯图标时：圆形背景
- Hover: 图标微发光

### News Card
- 标题 + 摘要 + 时间 + 来源
- 可选配图（渐变色块占位）

### Tutorial Card
- 标题 + 难度标签 + 时长 + 简介

### Button
- **Primary**：bg-tesla红，hover时glow
- **Secondary**：透明+边框
- **Ghost**：无边框，hover显示背景
- 统一：圆角8px，高度48px，padding 0 24px

### Tag/Badge
- 圆角pill，padding 4px 12px
- 颜色根据分类：AI-紫色，开发-蓝色，效率-绿色等

### Footer
- 简洁的单行：版权 + 链接
- 分隔线：细线+渐变

## 6. 技术方案

### 技术栈
- **HTML5**：语义化标签
- **CSS3**：
  - CSS Variables（主题变量）
  - Flexbox + Grid（布局）
  - @keyframes（动画）
  - backdrop-filter（玻璃态）
  - clamp()（响应式字体）
- **JavaScript**：
  - 原生ES6+
  - 单页应用路由（hash-based）
  - 动态渲染Skills/News数据

### 文件结构
```
./AgentSkills网站/
├── index.html          // 主入口
├── styles/
│   └── main.css        // 所有样式
├── scripts/
│   └── app.js          // 主逻辑
└── assets/
    └── (可选资源)
```

### 数据结构
```javascript
// Skill
{
  id: string,
  name: string,
  description: string,
  icon: string (SVG or emoji),
  category: string,
  tags: string[],
  source: string,
  installCount: number,
  rating: number,
  features: string[],
  usage: string
}

// News
{
  id: string,
  title: string,
  summary: string,
  source: string,
  date: string,
  category: string,
  url: string
}

// Tutorial
{
  id: string,
  title: string,
  description: string,
  difficulty: '入门' | '进阶' | '高级',
  duration: string,
  category: string
}
```

### Mock数据
准备15-20个真实感的Skills示例数据，覆盖：
- 办公效率（邮件、日历、文档）
- 数据分析（可视化、统计）
- 编程开发（代码生成、调试）
- 创意设计（图像生成、文案）
- AI研究（模型调用、Prompt工程）

资讯和教程各5-8条。

## 7. 质量标准

- 首屏加载即有视觉冲击力
- 所有hover/focus状态完备
- 动画流畅60fps
- 移动端布局完美
- 对比度满足WCAG AA
- 代码有清晰注释
- 文件大小控制在合理范围（CSS<30KB, JS<50KB）
