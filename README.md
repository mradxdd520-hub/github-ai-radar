# 🤖 GitHub AI 雷达

> 每日扫描 GitHub 趋势榜 · VC 视角深度解读 · 挖掘最具 Vibecoding 变现潜力的 AI 项目

[![Daily Scan](https://img.shields.io/badge/scan-daily-blue)](./reports)
[![AI Focus](https://img.shields.io/badge/focus-AI%20%7C%20LLM%20%7C%20Agent-orange)](./reports)

## 🎯 项目目标

作为一个架构师/独立开发者，我们每天都在关注 AI 领域的最新动态。这个项目帮你：

1. **自动扫描** GitHub 趋势榜中的 AI 相关项目
2. **VC 视角解读** 每个项目的商业潜力、技术壁垒、市场热度
3. **筛选出最具 Vibecoding 变现潜力** 的项目，帮你发现下一个风口

## 📊 评分体系

| 维度 | 权重 | 评估要点 |
|------|------|----------|
| 🔥 市场热度 | 25% | Stars、Forks、社区活跃度 |
| 🛡️ 技术壁垒 | 20% | 原创性、技术复杂度、语言选择 |
| 💰 商业潜力 | 25% | B2B 适用性、变现场景、企业需求 |
| 🧱 生态位置 | 15% | 是否处于 AI 工具链关键位置 |
| 🎯 Vibecoding | 15% | 独立开发者能否快速上手变现 |

## 📁 目录结构

```
github-ai-radar/
├── README.md           # 项目说明
├── reports/            # 每日报告
│   └── YYYY-MM-DD.md
└── scripts/            # 分析脚本
    └── analyze_projects.py
```

## 📅 最新报告

查看 [reports/](./reports) 目录获取每日分析报告。

## 🚀 本地运行

```bash
# 生成今日报告
python3 scripts/analyze_projects.py

# 报告会输出到 stdout，可以重定向到文件
python3 scripts/analyze_projects.py > reports/$(date +%Y-%m-%d).md
```

## 💡 关于 Vibecoding

Vibecoding 是一种以"感觉"驱动的快速开发方式——找到一个有潜力的开源项目，快速包装、部署、变现。这个雷达帮你找到最适合 Vibecoding 的项目。

---

*Built with ❤️ by 晨哥 & 晨仔*
