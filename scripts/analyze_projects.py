#!/usr/bin/env python3
"""
GitHub AI 雷达 V2 - 独立开发者视角项目分析器
每日扫描趋势榜，发现最具 Vibecoding 变现潜力的项目

新评分体系（满分 10 分）:
- 🎯 Vibecoding 难度 (30%) - 技术实现难度，越低越好
- 🏰 逻辑护城河 (25%) - 竞争壁垒、技术门槛
- 📈 增长潜力 (25%) - Stars 增速、社区活跃度
- 💰 变现清晰度 (20%) - 商业模式是否清晰
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============ 配置 ============

# AI 相关关键词
AI_KEYWORDS = {
    'topics': [
        'ai', 'artificial-intelligence', 'machine-learning', 'ml', 'deep-learning',
        'llm', 'large-language-model', 'gpt', 'chatgpt', 'openai', 'anthropic',
        'agent', 'agents', 'ai-agents', 'autonomous-agents', 'agentic',
        'rag', 'retrieval-augmented-generation', 'embeddings', 'vector-database',
        'generative-ai', 'genai', 'text-generation', 'image-generation',
        'nlp', 'natural-language-processing', 'transformers', 'bert',
        'computer-vision', 'cv', 'image-recognition', 'object-detection',
        'speech-recognition', 'text-to-speech', 'tts', 'stt',
        'langchain', 'llamaindex', 'autogen', 'crewai',
        'prompt-engineering', 'fine-tuning', 'lora', 'qlora',
        'ollama', 'llama', 'mistral', 'claude', 'gemini',
        'mcp', 'model-context-protocol', 'function-calling', 'tool-use',
        'chatbot', 'assistant', 'copilot', 'coding-assistant'
    ],
    'description': [
        'ai', 'llm', 'gpt', 'agent', 'machine learning', 'deep learning',
        'language model', 'chatbot', 'assistant', 'neural', 'transformer',
        'embedding', 'vector', 'rag', 'generative', 'prompt', 'inference',
        'fine-tun', 'train', 'model', 'anthropic', 'openai', 'ollama'
    ]
}

# 赛道分类
TRACKS = {
    'agent': ['agent', 'agents', 'ai-agents', 'autonomous-agents', 'agentic', 'autogen', 'crewai'],
    'llm-infra': ['langchain', 'llamaindex', 'llm', 'large-language-model', 'mcp'],
    'rag': ['rag', 'retrieval-augmented-generation', 'embeddings', 'vector-database', 'vector'],
    'ai-ui': ['ui', 'webui', 'interface', 'dashboard', 'chat', 'chatbot'],
    'coding': ['copilot', 'coding-assistant', 'code', 'developer', 'devtool'],
    'image-gen': ['image-generation', 'stable-diffusion', 'midjourney', 'dall-e', 'comfyui'],
    'automation': ['automation', 'workflow', 'n8n', 'zapier', 'no-code', 'low-code'],
    'ml-framework': ['tensorflow', 'pytorch', 'keras', 'scikit-learn', 'machine-learning'],
}

# ============ 工具函数 ============

def is_ai_project(project: dict) -> bool:
    """判断是否为 AI 相关项目"""
    topics = [t.lower() for t in project.get('topics', [])]
    for keyword in AI_KEYWORDS['topics']:
        if keyword in topics:
            return True
    
    desc = (project.get('description') or '').lower()
    for keyword in AI_KEYWORDS['description']:
        if keyword in desc:
            return True
    
    return False

def detect_track(project: dict) -> str:
    """识别项目所属赛道"""
    topics = [t.lower() for t in project.get('topics', [])]
    desc = (project.get('description') or '').lower()
    name = project.get('name', '').lower()
    
    for track, keywords in TRACKS.items():
        for keyword in keywords:
            if keyword in topics or keyword in desc or keyword in name:
                return track
    
    return 'other'

def generate_project_id(name: str) -> str:
    """生成项目唯一 ID"""
    return name.lower().replace('/', '-').replace(' ', '-')

# ============ 新评分体系 ============

def calculate_score_v2(project: dict) -> dict:
    """
    V2 评分体系 (满分 10 分，贴合独立开发者视角)
    
    维度:
    1. 🎯 Vibecoding 难度 (30%) - 技术实现难度，越低越好 (1-5，5=最简单)
    2. 🏰 逻辑护城河 (25%) - 竞争壁垒、技术门槛 (1-5)
    3. 📈 增长潜力 (25%) - Stars 增速、社区活跃度 (1-5)
    4. 💰 变现清晰度 (20%) - 商业模式是否清晰 (1-5)
    """
    
    stars = project.get('stars', 0)
    forks = project.get('forks', 0)
    topics = [t.lower() for t in project.get('topics', [])]
    desc = (project.get('description') or '').lower()
    lang = (project.get('language') or '').lower()
    today_stars = project.get('today_stars', 0)
    
    score = {
        'vibe_difficulty': 3,      # Vibecoding 难度 (1-5, 5=最简单)
        'moat': 3,                 # 逻辑护城河 (1-5)
        'growth': 3,               # 增长潜力 (1-5)
        'monetization': 3,         # 变现清晰度 (1-5)
        'total': 0.0,              # 总分 (0-10)
        'featured': False,         # 是否精选
        'tags': [],                # 标签
        'verdict': '',             # 结论
    }
    
    # === 1. Vibecoding 难度 (越低越好，分数越高) ===
    vibe_score = 3  # 默认中等
    
    # 语言友好度
    if lang in ['python', 'javascript', 'typescript']:
        vibe_score += 1
        score['tags'].append('开发者友好')
    elif lang in ['rust', 'c++', 'c', 'go']:
        vibe_score -= 1
    
    # 有 UI 的项目更容易包装
    if any(x in topics for x in ['ui', 'webui', 'interface', 'dashboard', 'frontend']):
        vibe_score += 1
        score['tags'].append('自带UI')
    
    # 易用性信号
    easy_signals = ['easy', 'simple', 'quick', 'beginner', 'tutorial', 'no-code', 'low-code']
    if any(s in desc for s in easy_signals):
        vibe_score += 1
        score['tags'].append('易上手')
    
    # 复杂部署信号
    hard_signals = ['kubernetes', 'cluster', 'distributed', 'enterprise-only', 'requires-gpu']
    if any(s in desc or s in topics for s in hard_signals):
        vibe_score -= 1
        score['tags'].append('部署复杂')
    
    # Self-hosted 加分
    if 'self-hosted' in desc or 'self-hosted' in topics:
        vibe_score += 0.5
        score['tags'].append('可自托管')
    
    score['vibe_difficulty'] = max(1, min(5, vibe_score))
    
    # === 2. 逻辑护城河 ===
    moat_score = 3
    
    # 基础设施层护城河高
    infra_signals = ['framework', 'engine', 'runtime', 'compiler', 'infrastructure', 'sdk']
    if any(s in desc or s in topics for s in infra_signals):
        moat_score += 1
        score['tags'].append('基础设施')
    
    # 高性能语言通常意味着更高技术门槛
    if lang in ['rust', 'c++', 'c']:
        moat_score += 0.5
    
    # Agent/RAG 赛道竞争激烈，护城河相对较低
    if detect_track(project) in ['agent', 'rag']:
        moat_score -= 0.5
    
    # 大厂背书
    big_companies = ['google', 'microsoft', 'meta', 'openai', 'anthropic', 'nvidia']
    name_lower = project.get('name', '').lower()
    if any(c in name_lower for c in big_companies):
        moat_score += 1
        score['tags'].append('大厂背书')
    
    score['moat'] = max(1, min(5, moat_score))
    
    # === 3. 增长潜力 ===
    growth_score = 3
    
    # Stars 规模
    if stars >= 100000:
        growth_score += 1.5
        score['tags'].append('10万+Stars')
    elif stars >= 50000:
        growth_score += 1
        score['tags'].append('5万+Stars')
    elif stars >= 10000:
        growth_score += 0.5
    elif stars < 5000:
        growth_score -= 0.5
    
    # 社区参与度 (fork/star 比例)
    if stars > 0 and forks / stars > 0.15:
        growth_score += 0.5
        score['tags'].append('高参与度')
    
    # 今日新增 stars
    if today_stars >= 500:
        growth_score += 1
        score['tags'].append('今日爆发')
    elif today_stars >= 100:
        growth_score += 0.5
    
    score['growth'] = max(1, min(5, growth_score))
    
    # === 4. 变现清晰度 ===
    monetization_score = 3
    
    # 明确的商业模式信号
    biz_signals = ['saas', 'api', 'cloud', 'enterprise', 'business', 'commercial', 'pro', 'premium']
    if any(s in desc or s in topics for s in biz_signals):
        monetization_score += 1
        score['tags'].append('商业化路径清晰')
    
    # 赛道加成
    track = detect_track(project)
    if track == 'ai-ui':
        monetization_score += 1  # UI 类最容易变现
        score['tags'].append('AI UI')
    elif track == 'automation':
        monetization_score += 0.5
        score['tags'].append('自动化')
    elif track == 'agent':
        monetization_score += 0.5
        score['tags'].append('Agent')
    elif track == 'rag':
        monetization_score += 0.5
        score['tags'].append('RAG')
    elif track == 'coding':
        monetization_score += 0.5
        score['tags'].append('Coding')
    
    # Self-hosted 通常有付费托管版
    if 'self-hosted' in desc:
        monetization_score += 0.5
    
    score['monetization'] = max(1, min(5, monetization_score))
    
    # === 计算总分 (加权平均，满分 10) ===
    total = (
        score['vibe_difficulty'] * 0.30 +
        score['moat'] * 0.25 +
        score['growth'] * 0.25 +
        score['monetization'] * 0.20
    ) * 2  # 乘 2 转换为 10 分制
    
    score['total'] = round(total, 1)
    
    # === 精选判定 ===
    # 总分 >= 8 且 Vibecoding 难度 >= 4 (即简单)
    score['featured'] = score['total'] >= 7.5 and score['vibe_difficulty'] >= 4
    
    # === 结论 ===
    if score['total'] >= 8.5:
        score['verdict'] = '🏆 强烈推荐'
    elif score['total'] >= 7.5:
        score['verdict'] = '✅ 值得关注'
    elif score['total'] >= 6.5:
        score['verdict'] = '👀 可以观望'
    else:
        score['verdict'] = '⏸️ 暂不推荐'
    
    # 去重 tags
    score['tags'] = list(dict.fromkeys(score['tags']))
    
    return score

# ============ 项目分析 ============

def analyze_project(project: dict, date: str) -> dict:
    """分析单个项目，返回标准化数据结构"""
    score = calculate_score_v2(project)
    track = detect_track(project)
    
    return {
        'id': generate_project_id(project['name']),
        'name': project['name'],
        'url': project['url'],
        'description': project.get('description', ''),
        'stars': project.get('stars', 0),
        'forks': project.get('forks', 0),
        'language': project.get('language') or 'Unknown',
        'topics': project.get('topics', []),
        'today_stars': project.get('today_stars', 0),
        'track': track,
        'score': score,
        'first_seen': date,
        'last_seen': date,
        'peak_rank': project.get('rank', 0),
        'days_on_trending': 1,
    }

# ============ 归档数据库操作 ============

def load_archive(archive_path: Path) -> dict:
    """加载归档数据库"""
    if archive_path.exists():
        with open(archive_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'version': 2,
        'updated_at': '',
        'stats': {
            'total_projects': 0,
            'total_days': 0,
            'featured_count': 0,
        },
        'projects': {}
    }

def save_archive(archive: dict, archive_path: Path):
    """保存归档数据库"""
    archive['updated_at'] = datetime.now().isoformat()
    with open(archive_path, 'w', encoding='utf-8') as f:
        json.dump(archive, f, ensure_ascii=False, indent=2)

def update_archive(archive: dict, new_projects: list, date: str) -> dict:
    """更新归档数据库"""
    for proj in new_projects:
        proj_id = proj['id']
        
        if proj_id in archive['projects']:
            # 更新已存在的项目
            existing = archive['projects'][proj_id]
            existing['last_seen'] = date
            existing['days_on_trending'] += 1
            existing['stars'] = proj['stars']
            existing['forks'] = proj['forks']
            existing['today_stars'] = proj.get('today_stars', 0)
            existing['score'] = proj['score']
            # 更新峰值排名
            if proj.get('peak_rank', 0) > 0:
                if existing.get('peak_rank', 999) > proj['peak_rank']:
                    existing['peak_rank'] = proj['peak_rank']
        else:
            # 新项目
            archive['projects'][proj_id] = proj
            archive['stats']['total_projects'] += 1
    
    # 更新统计
    archive['stats']['featured_count'] = sum(
        1 for p in archive['projects'].values() if p['score']['featured']
    )
    
    return archive

# ============ 报告生成 ============

def generate_daily_snapshot(analyzed_projects: list, all_trending: list, date: str) -> dict:
    """生成每日快照数据"""
    sorted_projects = sorted(analyzed_projects, key=lambda x: x['score']['total'], reverse=True)
    
    return {
        'date': date,
        'generated_at': datetime.now().isoformat(),
        'stats': {
            'total_trending': len(all_trending),
            'ai_projects': len(analyzed_projects),
            'featured': sum(1 for p in analyzed_projects if p['score']['featured']),
        },
        'top5': [
            {
                'rank': i + 1,
                'id': p['id'],
                'name': p['name'],
                'url': p['url'],
                'description': p['description'],
                'stars': p['stars'],
                'language': p['language'],
                'track': p['track'],
                'score': p['score'],
            }
            for i, p in enumerate(sorted_projects[:5])
        ],
        'all_ai_projects': [
            {
                'id': p['id'],
                'name': p['name'],
                'score': p['score']['total'],
                'track': p['track'],
            }
            for p in sorted_projects
        ],
        'all_trending': [
            {
                'rank': p.get('rank', 0),
                'name': p['name'],
                'stars': p.get('stars', 0),
                'today_stars': p.get('today_stars', 0),
                'language': p.get('language'),
                'is_ai': is_ai_project(p),
            }
            for p in all_trending
        ]
    }

def generate_markdown_report(snapshot: dict) -> str:
    """生成 Markdown 格式报告"""
    date = snapshot['date']
    stats = snapshot['stats']
    top5 = snapshot['top5']
    
    report = f"""# 🤖 GitHub AI 雷达 - {date}

> 每日趋势精选 · Vibecoding 变现潜力分析

---

## 📊 今日数据

| 指标 | 数值 |
|------|------|
| GitHub Trending 总数 | {stats['total_trending']} |
| AI 相关项目 | {stats['ai_projects']} |
| 🏆 精选项目 | {stats['featured']} |

---

## 🚀 创业黑马榜 Top 5

"""
    
    for proj in top5:
        score = proj['score']
        tags_str = ' '.join([f'`{t}`' for t in score['tags'][:4]])
        
        report += f"""### {proj['rank']}. [{proj['name']}]({proj['url']})

**{score['verdict']}** | 总分：**{score['total']}/10** {'🏆' if score['featured'] else ''}

> {proj['description']}

| 维度 | 得分 | 说明 |
|------|:----:|------|
| 🎯 Vibecoding 难度 | {score['vibe_difficulty']}/5 | {'简单' if score['vibe_difficulty'] >= 4 else '中等' if score['vibe_difficulty'] >= 3 else '复杂'} |
| 🏰 逻辑护城河 | {score['moat']}/5 | - |
| 📈 增长潜力 | {score['growth']}/5 | ⭐ {proj['stars']:,} |
| 💰 变现清晰度 | {score['monetization']}/5 | - |

**标签**：{tags_str}

---

"""
    
    # 其他 AI 项目
    other_projects = snapshot['all_ai_projects'][5:10]
    if other_projects:
        report += """## 📌 其他值得关注

| 项目 | 评分 | 赛道 |
|------|:----:|------|
"""
        for p in other_projects:
            report += f"| {p['name']} | {p['score']} | {p['track']} |\n"
    
    report += f"""

---

## 📈 评分体系 V2

| 维度 | 权重 | 说明 |
|------|:----:|------|
| 🎯 Vibecoding 难度 | 30% | 技术实现难度，越低越好 |
| 🏰 逻辑护城河 | 25% | 竞争壁垒、技术门槛 |
| 📈 增长潜力 | 25% | Stars 增速、社区活跃度 |
| 💰 变现清晰度 | 20% | 商业模式是否清晰 |

**精选标准**：总分 ≥ 7.5 且 Vibecoding 难度 ≥ 4

---

*Generated by GitHub AI Radar V2 · {date}*
"""
    
    return report

# ============ 主程序 ============

def main():
    """主程序入口"""
    # 路径配置
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / 'data'
    reports_dir = project_root / 'reports'
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 解析参数
    input_file = None
    output_mode = 'all'  # all, json, markdown
    
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == '--input' and i + 1 < len(args):
            input_file = args[i + 1]
            i += 2
        elif args[i] == '--output' and i + 1 < len(args):
            output_mode = args[i + 1]
            i += 2
        elif args[i] == '--date' and i + 1 < len(args):
            today = args[i + 1]
            i += 2
        else:
            i += 1
    
    # 加载趋势数据
    if input_file:
        with open(input_file, 'r', encoding='utf-8') as f:
            all_trending = json.load(f)
    else:
        # 尝试从默认位置加载
        default_input = data_dir / f'trending_{today}.json'
        if default_input.exists():
            with open(default_input, 'r', encoding='utf-8') as f:
                all_trending = json.load(f)
        else:
            print(f"错误: 找不到输入文件 {default_input}", file=sys.stderr)
            sys.exit(1)
    
    # 筛选 AI 项目
    ai_projects = [p for p in all_trending if is_ai_project(p)]
    print(f"发现 {len(ai_projects)} 个 AI 相关项目 (共 {len(all_trending)} 个)", file=sys.stderr)
    
    # 分析项目
    analyzed = [analyze_project(p, today) for p in ai_projects]
    
    # 生成每日快照
    snapshot = generate_daily_snapshot(analyzed, all_trending, today)
    
    # 更新归档数据库
    archive_path = data_dir / 'archive.json'
    archive = load_archive(archive_path)
    archive = update_archive(archive, analyzed, today)
    
    # 检查是否为新的一天
    snapshots_dir = data_dir / 'snapshots'
    snapshots_dir.mkdir(exist_ok=True)
    snapshot_path = snapshots_dir / f'{today}.json'
    if not snapshot_path.exists():
        archive['stats']['total_days'] += 1
    
    # 保存数据
    if output_mode in ['all', 'json']:
        # 保存快照
        with open(snapshot_path, 'w', encoding='utf-8') as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)
        print(f"快照已保存: {snapshot_path}", file=sys.stderr)
        
        # 保存归档
        save_archive(archive, archive_path)
        print(f"归档已更新: {archive_path}", file=sys.stderr)
    
    # 生成并输出 Markdown 报告
    if output_mode in ['all', 'markdown']:
        report = generate_markdown_report(snapshot)
        
        if output_mode == 'all':
            # 保存到文件
            report_path = reports_dir / f'{today}.md'
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"报告已保存: {report_path}", file=sys.stderr)
        else:
            # 输出到 stdout
            print(report)
    
    # 输出摘要
    top5 = sorted(analyzed, key=lambda x: x['score']['total'], reverse=True)[:5]
    print("\n=== Top 5 ===", file=sys.stderr)
    for i, p in enumerate(top5, 1):
        print(f"{i}. {p['name']} ({p['score']['total']}/10) - {p['score']['verdict']}", file=sys.stderr)
    
    return snapshot

if __name__ == '__main__':
    main()
