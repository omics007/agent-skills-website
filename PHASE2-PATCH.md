# Phase 2 SEO & Accessibility (a11y) 补丁文档

> 目标文件: `./AgentSkills网站-v3/index.html`
> 文件总行数: 5536
> 创建日期: 2024年
> 状态: 待合并（等待Phase 1完成后执行）

---

## 修改 1: SEO - 添加 Open Graph 标签

**位置**: `<title>` 标签之后，Line 7-8 之间

**锚点**: 在 `<title>Agent Skills | 探索前沿Agent技能市场</title>` 之后

**添加内容**:
```html
<!-- Open Graph -->
<meta property="og:title" content="AgentSkills | 探索前沿Agent技能市场">
<meta property="og:description" content="发现、探索、使用前沿AI Agent技能。从全球最大的技能市场获取最新资源">
<meta property="og:type" content="website">
<meta property="og:url" content="https://omics007.github.io/agent-skills-website/">
<meta property="og:image" content="https://omics007.github.io/agent-skills-website/og-image.png">
<meta property="og:locale" content="zh_CN">
<meta property="og:site_name" content="AgentSkills">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="AgentSkills | 探索前沿Agent技能市场">
<meta name="twitter:description" content="发现、探索、使用前沿AI Agent技能">
<meta name="twitter:image" content="https://omics007.github.io/agent-skills-website/og-image.png">
```

---

## 修改 2: SEO - 添加 Favicon

**位置**: `<head>` 标签内，Line 12-13 之间（Google Fonts之后）

**锚点**: 在 `<!-- QRCode.js CDN -->` 之前

**添加内容**:
```html
<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><circle cx='20' cy='20' r='18' fill='none' stroke='%23e31937' stroke-width='2'/><path d='M14 20L18 24L26 16' fill='none' stroke='%230057d9' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>">
```

---

## 修改 3: SEO - 添加 Canonical URL

**位置**: `</head>` 标签之前，Line 3212-3213 之间

**锚点**: 在 `</style>` 和 `</head>` 之间

**添加内容**:
```html
<!-- Canonical URL -->
<link rel="canonical" href="https://omics007.github.io/agent-skills-website/">
```

---

## 修改 4: SEO - 添加 Web App Manifest (内联为 data URI)

**位置**: `</head>` 标签之前，与修改3相邻

**锚点**: 在 canonical URL 之后

**添加内容**:
```html
<!-- Web App Manifest -->
<link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiQWdlbnRTa2lsbHMiLCJzaG9ydF9uYW1lIjoiQWdlbnRTa2lsbHMiLCJzdGFydF91cmwiOiIuLy8iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsImJhY2tncm91bmRfY29sb3IiOiIjMGEwYTBhIiwidGhlbWVfY29sb3IiOiIjZTMxOTM3In0=">
```

---

## 修改 5: SEO - 添加 Structured Data (JSON-LD)

**位置**: `</head>` 标签之前，与修改3、4相邻

**锚点**: 在 manifest link 之后

**添加内容**:
```html
<!-- Structured Data -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "AgentSkills",
    "description": "发现、探索、使用前沿AI Agent技能市场",
    "url": "https://omics007.github.io/agent-skills-website/"
}
</script>
```

---

## 修改 6: a11y - 添加 Skip-to-Content 链接

**位置**: `<body>` 标签之后，Line 3214-3215 之间

**锚点**: 在 `<body>` 和 `<!-- Cyberpunk Scanlines Overlay -->` 之间

**添加内容**:
```html
<!-- Skip to Main Content (a11y) -->
<a href="#mainContent" class="skip-to-content" style="position:fixed;top:-100%;left:50%;transform:translateX(-50%);z-index:10000;padding:12px 24px;background:var(--accent-tesla);color:white;border-radius:0 0 8px 8px;font-size:14px;font-weight:600;text-decoration:none;transition:top 0.2s;" onfocus="this.style.top='0'" onblur="this.style.top='-100%'">跳转到主要内容</a>
```

---

## 修改 7: a11y - 增强 Modal Focus Trap

**位置**: `initModals()` 函数内，Line 5490-5499

**锚点**: 完整替换现有的 `function initModals()` 函数

**替换内容**:
```javascript
function initModals() {
    // Close modals on overlay click
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('open');
            }
        });
        
        // Focus trap for accessibility
        overlay.addEventListener('keydown', (e) => {
            if (e.key !== 'Tab') return;
            const focusable = overlay.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
            if (focusable.length === 0) return;
            const first = focusable[0];
            const last = focusable[focusable.length - 1];
            if (e.shiftKey) {
                if (document.activeElement === first) {
                    e.preventDefault();
                    last.focus();
                }
            } else {
                if (document.activeElement === last) {
                    e.preventDefault();
                    first.focus();
                }
            }
        });
    });
}
```

---

## 修改 8: a11y - 添加搜索输入框 aria-label

**位置**: Line 3347

**锚点**: `<input type="text" class="search-input" id="searchInput"`

**替换内容**:
```html
<input type="text" class="search-input" id="searchInput" placeholder="搜索 Skills、资讯、教程..." autocomplete="off" aria-label="搜索Skills、资讯和教程">
```

---

## 修改 9: a11y - 添加模态框关闭按钮 aria-label

**位置**: Line 3386-3388

**锚点**: `<button class="modal-close" onclick="closeLoginModal()">`

**替换内容**:
```html
<button class="modal-close" onclick="closeLoginModal()" aria-label="关闭">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
</button>
```

---

## 修改 10: a11y - 添加用户菜单 aria 属性

**位置**: Line 3246

**锚点**: `<button class="user-avatar-btn" onclick="toggleUserDropdown()">`

**替换内容**:
```html
<button class="user-avatar-btn" onclick="toggleUserDropdown()" aria-expanded="false" aria-haspopup="true" aria-label="用户菜单">
```

**注意**: 需要在 `toggleUserDropdown()` 函数中添加 `aria-expanded` 状态切换逻辑（根据 Phase 1 情况决定是否在此补丁中添加）

---

## 修改 11: a11y - 添加 aria-live 区域

**位置**: Toast div 之后，Line 3463 之后

**锚点**: `<div class="toast" id="toast"></div>` 之后，`</footer>` 之前

**添加内容**:
```html
<!-- ARIA Live Region for screen readers -->
<div aria-live="polite" aria-atomic="true" id="ariaLiveRegion" style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);"></div>
```

---

## 修改 12: a11y - 更新 showToast 函数以更新 aria-live

**位置**: Line 4104-4112

**锚点**: `function showToast(message, type = 'success')` 函数

**替换内容**:
```javascript
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    // Update aria-live region for screen readers
    const liveRegion = document.getElementById('ariaLiveRegion');
    if (liveRegion) liveRegion.textContent = message;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
```

---

## 修改 13: a11y - 移动端菜单添加搜索入口

**位置**: Line 3311-3315 之间

**锚点**: `<div class="mobile-menu-content">` 之后，第一个 `<a>` 之前

**添加内容**:
```html
<!-- Search button in mobile menu (a11y: ensures search access on mobile) -->
<a href="javascript:void(0)" class="mobile-link" onclick="document.getElementById('searchOverlay').classList.add('open'); document.getElementById('searchInput').focus(); document.getElementById('mobileMenu').classList.remove('open'); document.getElementById('mobileMenuOverlay').style.display='none'; document.body.style.overflow='';">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
    搜索
</a>
```

---

## 修改 14: a11y - 添加 Mobile Menu Overlay 和关闭按钮

### 14a: 添加 Overlay

**位置**: Line 3309-3310 之间

**锚点**: 在 `<div class="mobile-menu" id="mobileMenu">` 之前

**添加内容**:
```html
<!-- Mobile Menu Overlay (a11y) -->
<div class="mobile-menu-overlay" id="mobileMenuOverlay" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);z-index:998;display:none;" onclick="closeMobileMenu()"></div>
```

### 14b: 添加关闭按钮

**位置**: Line 3311

**锚点**: `<div class="mobile-menu-content">` 内部最前面

**添加内容**:
```html
<button class="mobile-menu-close" onclick="closeMobileMenu()" style="position:absolute;top:20px;right:20px;width:40px;height:40px;display:flex;align-items:center;justify-content:center;background:var(--bg-tertiary);border:none;border-radius:var(--radius-full);color:var(--text-secondary);cursor:pointer;" aria-label="关闭菜单">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
</button>
```

### 14c: 添加 closeMobileMenu 函数

**位置**: `initMobileMenu()` 函数之后，Line 5427 之后

**锚点**: 在 `function initSearch()` 之前

**添加内容**:
```javascript
// Close mobile menu function
function closeMobileMenu() {
    document.getElementById('mobileMenu').classList.remove('open');
    const overlay = document.getElementById('mobileMenuOverlay');
    if (overlay) overlay.style.display = 'none';
    document.body.style.overflow = '';
}
```

### 14d: 更新 initMobileMenu 函数

**位置**: Line 5408-5427

**锚点**: `function initMobileMenu()` 函数

**替换内容**:
```javascript
function initMobileMenu() {
    const menuBtn = document.getElementById('navMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('mobileMenuOverlay');
    let isOpen = false;
    
    menuBtn.addEventListener('click', () => {
        isOpen = !isOpen;
        mobileMenu.classList.toggle('open', isOpen);
        if (overlay) overlay.style.display = isOpen ? 'block' : 'none';
        document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    
    // Close on link click
    mobileMenu.querySelectorAll('.mobile-link').forEach(link => {
        link.addEventListener('click', () => {
            isOpen = false;
            mobileMenu.classList.remove('open');
            if (overlay) overlay.style.display = 'none';
            document.body.style.overflow = '';
        });
    });
}
```

---

## 修改 15: UX - 添加返回顶部按钮

### 15a: 添加按钮 HTML

**位置**: `</body>` 之前，Line 5534-5535 之间

**锚点**: 在 `<script>` 结束标签 `</script>` 和 `</body>` 之间

**添加内容**:
```html
<!-- Back to Top Button (UX) -->
<button class="back-to-top" id="backToTop" onclick="window.scrollTo({top:0,behavior:'smooth'})" aria-label="返回顶部" style="position:fixed;bottom:32px;right:32px;width:44px;height:44px;border-radius:50%;background:var(--accent-tesla);color:white;border:none;cursor:pointer;display:none;align-items:center;justify-content:center;z-index:100;box-shadow:0 4px 12px rgba(0,0,0,0.3);transition:all 0.3s;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 15l-6-6-6 6"/></svg>
</button>
```

### 15b: 更新 initNavbar 函数显示逻辑

**位置**: Line 5396-5406

**锚点**: `function initNavbar()` 函数

**替换内容**:
```javascript
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const backToTop = document.getElementById('backToTop');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Show/hide back to top button
        if (backToTop) {
            backToTop.style.display = window.scrollY > 500 ? 'flex' : 'none';
        }
    });
}
```

---

## 修改 16: UX - 添加面包屑导航

**位置**: detail-page 的 detail-hero 中，Line 4694-4696 之间

**锚点**: 在 `<div class="detail-page">` → `<div class="detail-hero">` → `<div class="detail-container">` 之后，`<div class="detail-header">` 之前

**添加内容**:
```html
<!-- Breadcrumb Navigation (UX) -->
<nav class="breadcrumb" aria-label="面包屑导航" style="margin-bottom:var(--space-lg);font-size:13px;color:var(--text-muted);">
    <a href="#/" style="color:var(--text-secondary);">首页</a>
    <span style="margin:0 8px;">/</span>
    <a href="#/skills" style="color:var(--text-secondary);">Skills市场</a>
    <span style="margin:0 8px;">/</span>
    <span style="color:var(--text-primary);">${escapeHTML(skill.name)}</span>
</nav>
```

---

## 修改摘要

| # | 类型 | 功能 | 位置 |
|---|------|------|------|
| 1 | SEO | Open Graph 标签 | Line 7-8 |
| 2 | SEO | Favicon | Line 12-13 |
| 3 | SEO | Canonical URL | Line 3212-3213 |
| 4 | SEO | Web App Manifest | Line 3212-3213 |
| 5 | SEO | JSON-LD Structured Data | Line 3212-3213 |
| 6 | a11y | Skip-to-Content 链接 | Line 3214-3215 |
| 7 | a11y | Modal Focus Trap | Line 5490-5499 |
| 8 | a11y | 搜索输入框 aria-label | Line 3347 |
| 9 | a11y | 关闭按钮 aria-label | Line 3386-3388 |
| 10 | a11y | 用户菜单 aria 属性 | Line 3246 |
| 11 | a11y | ARIA Live 区域 | Line 3463-3464 |
| 12 | a11y | showToast 更新 live region | Line 4104-4112 |
| 13 | a11y | 移动端搜索入口 | Line 3311-3312 |
| 14a | a11y | Mobile Menu Overlay | Line 3309-3310 |
| 14b | a11y | Mobile 关闭按钮 | Line 3311 |
| 14c | a11y | closeMobileMenu 函数 | Line 5428-5432 |
| 14d | a11y | 更新 initMobileMenu | Line 5408-5427 |
| 15a | UX | 返回顶部按钮 | Line 5534-5535 |
| 15b | UX | 更新 initNavbar | Line 5396-5406 |
| 16 | UX | 面包屑导航 | Line 4695-4696 |

---

## 合并说明

1. **执行顺序**: 所有修改可以按上述编号顺序执行
2. **Phase 1 兼容性**: 本补丁假设 Phase 1 不会修改以下区域：
   - `<head>` 区域 (修改 1-5)
   - `initModals` 函数 (修改 7)
   - `showToast` 函数 (修改 12)
   - `initNavbar` 函数 (修改 15b)
   - `initMobileMenu` 函数 (修改 14d)
3. **如有冲突**: 请优先保留 Phase 1 的修改，Phase 2 的代码增强型修改（如 focus trap、aria 属性）可后置执行
