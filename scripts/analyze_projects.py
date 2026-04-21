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

# ============ 项目详情生成 ============

# 项目知识库 (基于项目名/类型生成描述)
PROJECT_KNOWLEDGE = {
    'langchain': {
        'intro': 'LangChain 是当前最流行的 LLM 应用开发框架，由 Harrison Chase 于 2022 年创立。它提供了一套完整的工具链，帮助开发者快速构建基于大语言模型的应用，包括 RAG 系统、AI Agent、对话机器人等。项目采用模块化设计，支持 OpenAI、Anthropic、本地模型等多种 LLM 后端。',
        'highlights': ['模块化链式调用架构，灵活组合各类组件', '完善的 RAG 实现（文档加载、分割、向量存储、检索）', 'LangGraph 支持复杂的多 Agent 协作场景', '丰富的集成生态，400+ 工具和数据源连接器', '活跃社区支持，每周发布新版本'],
        'scenarios': ['企业知识库问答系统', 'AI 客服/智能助手', '文档分析与摘要工具', '代码生成与解释工具', '多轮对话应用'],
        'industries': ['金融科技', 'SaaS 企业', '教育培训', '法律服务', '医疗健康'],
    },
    'open-webui': {
        'intro': 'Open WebUI（原 Ollama WebUI）是一个功能丰富的自托管 AI 聊天界面，支持 Ollama 和 OpenAI 兼容 API。项目提供了媲美 ChatGPT 的用户体验，同时保持数据完全私有。内置 RAG 引擎、多模态支持、用户管理等企业级功能。',
        'highlights': ['开箱即用的精美 UI，用户体验媲美 ChatGPT', '内置 RAG 引擎，支持文档上传和知识库问答', '支持多模态（图片、语音）', '完善的用户/权限管理系统', 'Docker 一键部署，5 分钟上线'],
        'scenarios': ['私有化 ChatGPT 替代方案', '团队内部 AI 助手', '企业知识库问答入口', '本地模型体验平台', 'AI 能力快速封装'],
        'industries': ['中小企业 IT 部门', '咨询公司', '研究机构', '教育机构', '创业公司'],
    },
    'n8n': {
        'intro': 'n8n 是一个开源的工作流自动化平台，被称为"开源版 Zapier"。近年来深度集成 AI 能力，支持调用各类 LLM API、构建 AI Agent 工作流。项目采用可视化编排，即使非技术人员也能快速搭建复杂自动化流程。',
        'highlights': ['可视化工作流编排，拖拽式操作', '400+ 预置集成（CRM、数据库、SaaS 工具）', '原生 AI 节点支持 OpenAI/Anthropic/本地模型', '自托管部署，数据完全可控', '活跃社区，丰富的模板库'],
        'scenarios': ['营销自动化（邮件、社媒、CRM）', 'AI 驱动的数据处理管道', '客户服务自动化', '内部流程自动化', 'API 集成中间件'],
        'industries': ['电商', '营销机构', '运营团队', 'SaaS 公司', '中小企业'],
    },
    'dify': {
        'intro': 'Dify 是一个开源的 LLMOps 平台，定位为"AI 应用开发的操作系统"。它提供从 Prompt 编排、RAG 流水线到 Agent 开发的全链路工具，让企业能够快速将 AI 能力落地为产品。',
        'highlights': ['可视化 Prompt 编排和调试', '完整的 RAG 流水线（支持多种向量库）', 'AI Agent 和工具调用支持', '内置用量统计和成本控制', '企业级权限和审计'],
        'scenarios': ['企业 AI 中台建设', '快速原型验证', 'AI 应用工厂', 'Prompt 资产管理', '多租户 AI 服务'],
        'industries': ['大型企业 IT', '系统集成商', 'AI 解决方案商', '金融机构', '政企客户'],
    },
    'transformers': {
        'intro': 'Hugging Face Transformers 是机器学习领域最重要的开源库之一，提供了数千个预训练模型的统一接口。从 BERT、GPT 到 Llama、Mistral，几乎所有主流模型都可以通过几行代码加载使用。',
        'highlights': ['统一的模型加载和推理接口', '支持 PyTorch/TensorFlow/JAX 多框架', '10万+ 预训练模型可用', '完善的微调和训练工具链', 'Pipeline API 极简调用'],
        'scenarios': ['NLP 任务（分类、NER、问答）', '文本生成和摘要', '模型微调和训练', '模型研究和实验', '生产环境模型部署'],
        'industries': ['AI 研究机构', '科技公司', '数据科学团队', '学术机构', 'AI 创业公司'],
    },
    'ollama': {
        'intro': 'Ollama 让本地运行大语言模型变得前所未有的简单。一条命令即可下载并运行 Llama、Mistral、Gemma 等主流开源模型。项目专注于简化部署体验，是本地 AI 开发的首选工具。',
        'highlights': ['一键安装，开箱即用', '支持所有主流开源模型', 'API 兼容 OpenAI 格式', '内存优化，消费级硬件可用', '活跃的模型库生态'],
        'scenarios': ['本地 AI 开发和测试', '隐私敏感场景的 AI 部署', 'AI 学习和实验', '离线 AI 应用', '开发环境模型服务'],
        'industries': ['个人开发者', '创业团队', '研究人员', '教育机构', '对数据安全敏感的企业'],
    },
}

# 赛道知识库
TRACK_KNOWLEDGE = {
    'agent': {
        'default_intro': '一个专注于 AI Agent 开发的项目，提供构建自主智能体的核心能力。Agent 是 2024-2025 年最火热的 AI 方向，能够自主规划、执行任务并使用工具。',
        'default_highlights': ['Agent 核心框架支持', '工具调用和 Function Calling', '多 Agent 协作能力', '记忆和状态管理'],
        'default_scenarios': ['智能助手开发', 'AI 自动化流程', '复杂任务编排', '对话系统'],
        'default_industries': ['SaaS', '企业服务', '效率工具', '客服'],
    },
    'llm-infra': {
        'default_intro': '一个 LLM 基础设施项目，为大语言模型应用提供核心支撑能力。在 AI 应用爆发的今天，LLM Infra 是整个生态的基石。',
        'default_highlights': ['LLM 调用和管理', '模型接口统一', 'Prompt 管理', '调用链追踪'],
        'default_scenarios': ['LLM 应用开发', 'AI 中台建设', '模型网关', 'Prompt 工程'],
        'default_industries': ['AI 公司', '科技企业', '云服务商', '系统集成商'],
    },
    'rag': {
        'default_intro': '一个专注于 RAG（检索增强生成）的项目。RAG 是让大模型"接入知识"的关键技术，广泛应用于知识库问答、智能搜索等场景。',
        'default_highlights': ['文档处理和分割', '向量化和存储', '检索和重排序', 'LLM 集成'],
        'default_scenarios': ['企业知识库', '智能问答系统', '文档分析', '智能搜索'],
        'default_industries': ['企业服务', '法律', '金融', '教育'],
    },
    'ai-ui': {
        'default_intro': '一个提供 AI 交互界面的项目。优秀的 UI 是 AI 能力落地的关键，让用户能够便捷地使用 AI 服务。',
        'default_highlights': ['精美的聊天界面', '多模型支持', '对话管理', '用户体验优化'],
        'default_scenarios': ['AI 聊天产品', '智能客服前端', 'AI 能力展示', '内部 AI 工具'],
        'default_industries': ['C 端产品', '企业内部工具', '教育', 'SaaS'],
    },
    'automation': {
        'default_intro': '一个专注于自动化的项目，帮助用户减少重复性工作，提升效率。AI 与自动化的结合正在重塑工作方式。',
        'default_highlights': ['工作流编排', '多系统集成', 'AI 能力接入', '可视化配置'],
        'default_scenarios': ['业务流程自动化', '数据同步', '营销自动化', '运维自动化'],
        'default_industries': ['运营团队', '营销', '电商', '企业 IT'],
    },
    'coding': {
        'default_intro': '一个 AI 编程辅助项目，帮助开发者提升编码效率。AI Coding 是生产力革命的前沿阵地。',
        'default_highlights': ['代码补全和生成', '代码解释和重构', '多语言支持', 'IDE 集成'],
        'default_scenarios': ['开发效率提升', '代码学习', '代码审查', '文档生成'],
        'default_industries': ['软件公司', '创业团队', '个人开发者', '教育'],
    },
    'ml-framework': {
        'default_intro': '一个机器学习框架或工具项目，为 AI 模型的训练和部署提供基础能力。',
        'default_highlights': ['模型训练支持', '推理优化', '多框架兼容', '生态完善'],
        'default_scenarios': ['模型开发', 'AI 研究', '生产部署', '模型优化'],
        'default_industries': ['AI 研究', '科技公司', '学术机构', '云服务商'],
    },
    'other': {
        'default_intro': '一个与 AI 相关的创新项目，在特定领域提供独特的价值。',
        'default_highlights': ['创新技术方案', '特定场景优化', '开源社区支持'],
        'default_scenarios': ['特定场景应用', '技术探索', '概念验证'],
        'default_industries': ['科技公司', '创业团队', '研究机构'],
    },
}

def generate_project_details(project: dict, score: dict, track: str) -> dict:
    """生成项目详细内容：介绍、亮点、场景、VC点评"""
    name = project.get('name', '').lower()
    desc = project.get('description') or ''
    stars = project.get('stars', 0)
    forks = project.get('forks', 0)
    language = project.get('language') or 'Unknown'
    topics = project.get('topics', [])
    
    # 尝试匹配已知项目
    known_key = None
    for key in PROJECT_KNOWLEDGE.keys():
        if key in name:
            known_key = key
            break
    
    # 获取赛道默认值
    track_info = TRACK_KNOWLEDGE.get(track, TRACK_KNOWLEDGE['other'])
    
    details = {}
    
    # === 1. 项目介绍 ===
    if known_key:
        details['intro'] = PROJECT_KNOWLEDGE[known_key]['intro']
    else:
        # 基于项目信息动态生成
        intro_parts = [track_info['default_intro']]
        if stars >= 100000:
            intro_parts.append(f'项目已获得超过 {stars//1000}K Stars，是该领域最受欢迎的开源项目之一。')
        elif stars >= 50000:
            intro_parts.append(f'项目拥有 {stars//1000}K+ Stars，社区活跃度高。')
        elif stars >= 10000:
            intro_parts.append(f'项目已积累 {stars//1000}K+ Stars，具有一定影响力。')
        
        if language and language != 'Unknown':
            intro_parts.append(f'主要使用 {language} 开发。')
        
        details['intro'] = ' '.join(intro_parts)
    
    # === 2. 项目亮点 ===
    if known_key:
        details['highlights'] = PROJECT_KNOWLEDGE[known_key]['highlights']
    else:
        highlights = track_info['default_highlights'].copy()
        # 基于标签动态添加
        if 'self-hosted' in topics or 'self-hosted' in desc.lower():
            highlights.insert(0, '支持自托管部署，数据完全可控')
        if stars >= 50000:
            highlights.insert(0, f'超过 {stars//1000}K Stars，社区验证')
        if any(x in topics for x in ['docker', 'kubernetes', 'helm']):
            highlights.append('容器化部署，运维友好')
        if 'api' in topics or 'sdk' in topics:
            highlights.append('提供 API/SDK，易于集成')
        details['highlights'] = highlights[:5]
    
    # === 3. 应用场景和行业推荐 ===
    if known_key:
        details['scenarios'] = PROJECT_KNOWLEDGE[known_key]['scenarios']
        details['industries'] = PROJECT_KNOWLEDGE[known_key]['industries']
    else:
        details['scenarios'] = track_info['default_scenarios']
        details['industries'] = track_info['default_industries']
    
    # === 4. VC 点评 (200+ 字) ===
    vc_parts = []
    
    # 开场：市场定位
    if track == 'agent':
        vc_parts.append(f'【市场洞察】{project["name"]} 切入的是 AI Agent 赛道，这是 2024-2025 年最火热的 AI 应用方向。随着 GPT-4、Claude 3 等模型能力的提升，Agent 从概念走向落地，市场空间巨大。')
    elif track == 'llm-infra':
        vc_parts.append(f'【市场洞察】{project["name"]} 定位于 LLM 基础设施层，这是整个 AI 应用生态的基石。随着企业 AI 应用需求爆发，LLM Infra 工具的市场需求持续增长。')
    elif track == 'rag':
        vc_parts.append(f'【市场洞察】{project["name"]} 聚焦 RAG 赛道，这是让大模型"接入知识"的关键技术。企业知识库问答是当前最成熟的 AI 落地场景之一，市场验证充分。')
    elif track == 'ai-ui':
        vc_parts.append(f'【市场洞察】{project["name"]} 提供 AI 交互界面解决方案。优秀的 UI 是 AI 能力落地的最后一公里，ChatGPT 的成功证明了 AI UI 的商业价值。')
    elif track == 'automation':
        vc_parts.append(f'【市场洞察】{project["name"]} 切入自动化赛道，AI + 自动化的组合正在重塑企业工作流程。Zapier 估值 50 亿美元，证明了这个赛道的天花板。')
    else:
        vc_parts.append(f'【市场洞察】{project["name"]} 在 AI 领域提供差异化价值，具有一定的市场空间和增长潜力。')
    
    # 数据表现
    fork_ratio = round(forks / stars * 100, 1) if stars > 0 else 0
    if stars >= 100000:
        vc_parts.append(f'【数据亮点】项目已斩获 {stars:,} Stars，属于头部开源项目。{fork_ratio}% 的 Fork 率表明社区参与度{"较高" if fork_ratio > 15 else "正常"}，开发者生态健康。')
    elif stars >= 50000:
        vc_parts.append(f'【数据亮点】{stars:,} Stars 的数据表现亮眼，已进入该领域第一梯队。Fork 率 {fork_ratio}%，社区活跃度{"出色" if fork_ratio > 15 else "良好"}。')
    elif stars >= 10000:
        vc_parts.append(f'【数据亮点】{stars:,} Stars 表明项目已获得市场初步验证。关注后续增长趋势和社区建设。')
    else:
        vc_parts.append(f'【数据表现】项目当前 {stars:,} Stars，处于早期阶段。需关注产品打磨和用户增长。')
    
    # Vibecoding 潜力
    if score['vibe_difficulty'] >= 4:
        vc_parts.append(f'【Vibecoding 潜力】技术实现难度较低（{score["vibe_difficulty"]}/5），非常适合独立开发者快速包装成产品。{"自带 UI 组件，" if "自带UI" in score.get("tags", []) else ""}建议结合特定垂直场景做差异化。')
    elif score['vibe_difficulty'] >= 3:
        vc_parts.append(f'【Vibecoding 潜力】技术门槛中等（{score["vibe_difficulty"]}/5），需要一定的技术功底。适合有经验的开发者，建议选择熟悉的领域切入。')
    else:
        vc_parts.append(f'【Vibecoding 潜力】项目技术复杂度较高（{score["vibe_difficulty"]}/5），不建议新手直接尝试。更适合作为技术学习对象或企业级集成。')
    
    # 风险提示
    risks = []
    if track in ['agent', 'rag']:
        risks.append('赛道竞争激烈，需要差异化定位')
    if stars < 10000:
        risks.append('项目仍处早期，稳定性待验证')
    if score['moat'] <= 2:
        risks.append('护城河较浅，易被复制')
    
    if risks:
        vc_parts.append(f'【风险提示】{"; ".join(risks)}。')
    
    # 总结建议
    if score['total'] >= 8:
        vc_parts.append(f'【投资建议】综合评分 {score["total"]}/10，强烈推荐关注。无论是学习、使用还是基于此创业，都是优质标的。')
    elif score['total'] >= 7:
        vc_parts.append(f'【投资建议】综合评分 {score["total"]}/10，值得关注。建议深入调研后，结合自身优势选择切入点。')
    else:
        vc_parts.append(f'【投资建议】综合评分 {score["total"]}/10，可以观望。关注项目后续发展，等待更好的时机。')
    
    details['vc_review'] = ' '.join(vc_parts)
    
    return details

# ============ 项目分析 ============

def analyze_project(project: dict, date: str) -> dict:
    """分析单个项目，返回标准化数据结构"""
    score = calculate_score_v2(project)
    track = detect_track(project)
    details = generate_project_details(project, score, track)
    
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
        'details': details,  # 新增详情字段
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
                'forks': p['forks'],
                'language': p['language'],
                'track': p['track'],
                'score': p['score'],
                'details': p.get('details', {}),  # 新增详情
            }
            for i, p in enumerate(sorted_projects[:5])
        ],
        'all_ai_projects': [
            {
                'id': p['id'],
                'name': p['name'],
                'score': p['score']['total'],
                'track': p['track'],
                'details': p.get('details', {}),  # 新增详情
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
        details = proj.get('details', {})
        tags_str = ' '.join([f'`{t}`' for t in score['tags'][:4]])
        
        # 项目亮点列表
        highlights = details.get('highlights', [])
        highlights_str = '\n'.join([f'- {h}' for h in highlights[:5]]) if highlights else '- 暂无'
        
        # 应用场景
        scenarios = details.get('scenarios', [])
        scenarios_str = '、'.join(scenarios[:5]) if scenarios else '暂无'
        
        # 行业推荐
        industries = details.get('industries', [])
        industries_str = '、'.join(industries[:5]) if industries else '暂无'
        
        # VC 点评
        vc_review = details.get('vc_review', '暂无点评')
        
        report += f"""### {proj['rank']}. [{proj['name']}]({proj['url']})

**{score['verdict']}** | 总分：**{score['total']}/10** {'🏆' if score['featured'] else ''} | ⭐ {proj['stars']:,} | {proj['language']}

---

#### 📖 项目介绍

{details.get('intro', proj['description'])}

---

#### ✨ 项目亮点

{highlights_str}

---

#### 🎯 适合的应用场景

{scenarios_str}

#### 🏢 行业推荐

{industries_str}

---

#### 📊 Vibecoding 评分

| 维度 | 得分 | 说明 |
|------|:----:|------|
| 🎯 Vibecoding 难度 | {score['vibe_difficulty']}/5 | {'简单，适合快速包装' if score['vibe_difficulty'] >= 4 else '中等难度' if score['vibe_difficulty'] >= 3 else '较复杂，需技术功底'} |
| 🏰 逻辑护城河 | {score['moat']}/5 | {'高壁垒' if score['moat'] >= 4 else '中等壁垒' if score['moat'] >= 3 else '易复制'} |
| 📈 增长潜力 | {score['growth']}/5 | ⭐ {proj['stars']:,} |
| 💰 变现清晰度 | {score['monetization']}/5 | {'路径清晰' if score['monetization'] >= 4 else '有潜力' if score['monetization'] >= 3 else '需探索'} |

**标签**：{tags_str}

---

#### 💼 VC 点评

{vc_review}

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
