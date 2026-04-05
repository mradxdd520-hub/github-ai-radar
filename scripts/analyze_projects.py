#!/usr/bin/env python3
"""
GitHub AI 雷达 - VC 视角项目分析器
每日扫描趋势榜，深度解读最具 Vibecoding 变现潜力的 AI 项目
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

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

def is_ai_project(project: dict) -> bool:
    """判断是否为 AI 相关项目"""
    # 检查 topics
    topics = [t.lower() for t in project.get('topics', [])]
    for keyword in AI_KEYWORDS['topics']:
        if keyword in topics:
            return True
    
    # 检查描述
    desc = (project.get('description') or '').lower()
    for keyword in AI_KEYWORDS['description']:
        if keyword in desc:
            return True
    
    return False

def calculate_vc_score(project: dict) -> dict:
    """
    VC 视角评分体系 (满分 100)
    
    维度：
    1. 市场热度 (25分) - stars, forks, 增长趋势
    2. 技术壁垒 (20分) - 原创性, 技术复杂度
    3. 商业潜力 (25分) - 变现场景, 企业级适用性
    4. 生态位置 (15分) - 是否处于 AI 基础设施/工具链关键位置
    5. Vibecoding 适配度 (15分) - 独立开发者/小团队能否快速上手变现
    """
    score = {
        'market_heat': 0,        # 市场热度
        'tech_barrier': 0,       # 技术壁垒
        'business_potential': 0, # 商业潜力
        'ecosystem_position': 0, # 生态位置
        'vibecoding_fit': 0,     # Vibecoding 适配度
        'total': 0,
        'highlights': [],
        'risks': []
    }
    
    stars = project.get('stars', 0)
    forks = project.get('forks', 0)
    topics = [t.lower() for t in project.get('topics', [])]
    desc = (project.get('description') or '').lower()
    lang = (project.get('language') or '').lower()
    
    # 1. 市场热度 (25分)
    if stars >= 100000:
        score['market_heat'] = 25
        score['highlights'].append('🔥 超级明星项目 (10万+ stars)')
    elif stars >= 50000:
        score['market_heat'] = 22
        score['highlights'].append('🌟 顶级热门项目')
    elif stars >= 20000:
        score['market_heat'] = 18
    elif stars >= 10000:
        score['market_heat'] = 15
    elif stars >= 5000:
        score['market_heat'] = 12
    else:
        score['market_heat'] = 8
    
    # fork/star 比例反映社区参与度
    if stars > 0 and forks / stars > 0.15:
        score['market_heat'] = min(25, score['market_heat'] + 2)
        score['highlights'].append('👥 高社区参与度')
    
    # 2. 技术壁垒 (20分)
    high_barrier_signals = ['framework', 'engine', 'runtime', 'compiler', 'infrastructure']
    medium_barrier_signals = ['sdk', 'library', 'api', 'platform']
    
    for signal in high_barrier_signals:
        if signal in desc or signal in topics:
            score['tech_barrier'] += 5
    for signal in medium_barrier_signals:
        if signal in desc or signal in topics:
            score['tech_barrier'] += 3
    
    # 语言复杂度加分
    if lang in ['rust', 'c++', 'c', 'go']:
        score['tech_barrier'] += 3
        score['highlights'].append(f'💪 高性能语言 ({lang})')
    
    score['tech_barrier'] = min(20, score['tech_barrier'])
    
    # 3. 商业潜力 (25分)
    b2b_signals = ['enterprise', 'business', 'production', 'deploy', 'scale', 'security']
    monetization_signals = ['api', 'saas', 'cloud', 'service', 'platform', 'self-hosted']
    
    for signal in b2b_signals:
        if signal in desc or signal in topics:
            score['business_potential'] += 4
            
    for signal in monetization_signals:
        if signal in desc or signal in topics:
            score['business_potential'] += 3
    
    # Agent 类项目商业潜力高
    if any(x in topics for x in ['agent', 'agents', 'ai-agents', 'autonomous-agents']):
        score['business_potential'] += 5
        score['highlights'].append('🤖 AI Agent 赛道 - 2024-2026 最热风口')
    
    # RAG 类项目商业潜力高
    if 'rag' in topics or 'retrieval' in desc:
        score['business_potential'] += 4
        score['highlights'].append('📚 RAG 应用 - 企业知识库刚需')
    
    score['business_potential'] = min(25, score['business_potential'])
    
    # 4. 生态位置 (15分)
    infra_signals = ['langchain', 'llamaindex', 'ollama', 'mcp', 'vector', 'embedding']
    tool_signals = ['cli', 'tool', 'utility', 'developer', 'devtool']
    
    for signal in infra_signals:
        if signal in desc.lower() or signal in topics:
            score['ecosystem_position'] += 5
            score['highlights'].append('🧱 AI 基础设施层')
            break
    
    for signal in tool_signals:
        if signal in desc.lower() or signal in topics:
            score['ecosystem_position'] += 3
    
    score['ecosystem_position'] = min(15, score['ecosystem_position'])
    
    # 5. Vibecoding 适配度 (15分) - 独立开发者能否快速变现
    vibecoding_positive = [
        'easy', 'simple', 'quick', 'fast', 'beginner', 'tutorial',
        'self-hosted', 'local', 'offline', 'privacy', 'free',
        'ui', 'interface', 'webui', 'dashboard', 'no-code', 'low-code'
    ]
    
    vibecoding_negative = [
        'enterprise-only', 'requires-gpu', 'distributed', 'kubernetes', 'cluster'
    ]
    
    for signal in vibecoding_positive:
        if signal in desc.lower() or signal in topics:
            score['vibecoding_fit'] += 2
    
    for signal in vibecoding_negative:
        if signal in desc.lower() or signal in topics:
            score['vibecoding_fit'] -= 2
            score['risks'].append(f'⚠️ 可能需要复杂部署 ({signal})')
    
    # Python/TypeScript/JavaScript 对独立开发者更友好
    if lang in ['python', 'typescript', 'javascript']:
        score['vibecoding_fit'] += 3
        score['highlights'].append(f'✅ 开发者友好语言 ({lang})')
    
    # 有 UI 的项目更容易包装成产品
    if any(x in topics for x in ['ui', 'webui', 'interface', 'dashboard', 'frontend']):
        score['vibecoding_fit'] += 3
        score['highlights'].append('🎨 自带 UI，可快速包装成产品')
    
    score['vibecoding_fit'] = max(0, min(15, score['vibecoding_fit']))
    
    # 总分
    score['total'] = (
        score['market_heat'] + 
        score['tech_barrier'] + 
        score['business_potential'] + 
        score['ecosystem_position'] + 
        score['vibecoding_fit']
    )
    
    return score

def analyze_project(project: dict) -> dict:
    """综合分析单个项目"""
    vc_score = calculate_vc_score(project)
    
    return {
        'name': project['name'],
        'url': project['url'],
        'description': project.get('description', ''),
        'stars': project.get('stars', 0),
        'forks': project.get('forks', 0),
        'language': project.get('language', 'Unknown'),
        'topics': project.get('topics', []),
        'vc_score': vc_score
    }

def generate_report(analyzed_projects: list, top_n: int = 5) -> str:
    """生成 Markdown 格式的每日报告"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 按总分排序，取 Top N
    sorted_projects = sorted(analyzed_projects, key=lambda x: x['vc_score']['total'], reverse=True)
    top_projects = sorted_projects[:top_n]
    
    report = f"""# 🤖 GitHub AI 雷达 - {today}

> 每日扫描趋势榜 · VC 视角深度解读 · Vibecoding 变现潜力分析

---

## 📊 今日 Top {top_n} AI 项目

"""
    
    for i, proj in enumerate(top_projects, 1):
        score = proj['vc_score']
        
        # 评级
        if score['total'] >= 80:
            rating = '⭐⭐⭐⭐⭐ 极力推荐'
        elif score['total'] >= 65:
            rating = '⭐⭐⭐⭐ 强烈推荐'
        elif score['total'] >= 50:
            rating = '⭐⭐⭐ 值得关注'
        else:
            rating = '⭐⭐ 持续观察'
        
        report += f"""### {i}. [{proj['name']}]({proj['url']})

**{rating}** | 综合评分：**{score['total']}/100**

> {proj['description']}

| 维度 | 得分 | 说明 |
|------|------|------|
| 🔥 市场热度 | {score['market_heat']}/25 | ⭐ {proj['stars']:,} · 🍴 {proj['forks']:,} |
| 🛡️ 技术壁垒 | {score['tech_barrier']}/20 | {proj['language'] or 'N/A'} |
| 💰 商业潜力 | {score['business_potential']}/25 | - |
| 🧱 生态位置 | {score['ecosystem_position']}/15 | - |
| 🎯 Vibecoding | {score['vibecoding_fit']}/15 | - |

**亮点：**
"""
        for highlight in score['highlights'][:5]:
            report += f"- {highlight}\n"
        
        if score['risks']:
            report += "\n**风险提示：**\n"
            for risk in score['risks'][:3]:
                report += f"- {risk}\n"
        
        report += "\n---\n\n"
    
    # 添加其他值得关注的项目
    other_notable = sorted_projects[top_n:top_n+5]
    if other_notable:
        report += """## 📌 其他值得关注

| 项目 | 评分 | Stars | 语言 |
|------|------|-------|------|
"""
        for proj in other_notable:
            report += f"| [{proj['name']}]({proj['url']}) | {proj['vc_score']['total']} | {proj['stars']:,} | {proj['language'] or 'N/A'} |\n"
    
    report += f"""

---

## 📈 评分体系说明

| 维度 | 权重 | 评估要点 |
|------|------|----------|
| 市场热度 | 25% | Stars、Forks、社区活跃度 |
| 技术壁垒 | 20% | 原创性、技术复杂度、语言选择 |
| 商业潜力 | 25% | B2B 适用性、变现场景、企业需求 |
| 生态位置 | 15% | 是否处于 AI 工具链关键位置 |
| Vibecoding | 15% | 独立开发者能否快速上手变现 |

---

*Generated by GitHub AI Radar · {today}*
"""
    
    return report

def main():
    # 读取 GitHub 趋势数据
    script_path = Path(__file__).parent.parent.parent / '..' / '.workbuddy' / 'skills' / 'GitHub热门项目' / 'scripts' / 'github_trending.py'
    
    # 如果直接传入 JSON 数据
    if len(sys.argv) > 1 and sys.argv[1] == '--input':
        with open(sys.argv[2], 'r') as f:
            projects = json.load(f)
    else:
        # 调用脚本获取数据
        result = subprocess.run(
            ['python3', str(script_path.resolve()), '--period', 'daily', '--limit', '30', '--json'],
            capture_output=True, text=True
        )
        projects = json.loads(result.stdout)
    
    # 筛选 AI 相关项目
    ai_projects = [p for p in projects if is_ai_project(p)]
    print(f"发现 {len(ai_projects)} 个 AI 相关项目", file=sys.stderr)
    
    # 分析每个项目
    analyzed = [analyze_project(p) for p in ai_projects]
    
    # 生成报告
    report = generate_report(analyzed)
    print(report)
    
    return analyzed

if __name__ == '__main__':
    main()
