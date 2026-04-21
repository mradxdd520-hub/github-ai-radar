# GitHub AI 雷达 V2

🤖 每日扫描 GitHub Trending，发现最具 **Vibecoding 变现潜力** 的 AI 项目。

## 🎯 在线访问

👉 **[https://mradxdd520-hub.github.io/github-ai-radar/](https://mradxdd520-hub.github.io/github-ai-radar/)**

## ✨ 功能特点

### 🚀 创业黑马榜
- 每日 Top 5 高潜力 AI 项目
- VC 视角 + 独立开发者视角双重分析
- 历史数据可追溯

### 📚 归档项目库
- 所有扫描过的项目持久存储
- 多维度筛选：赛道、评分、Vibe 难度
- 搜索功能

### 📊 评分体系 V2

| 维度 | 权重 | 说明 |
|------|:----:|------|
| 🎯 Vibecoding 难度 | 30% | 技术实现难度，越低越好 |
| 🏰 逻辑护城河 | 25% | 竞争壁垒、技术门槛 |
| 📈 增长潜力 | 25% | Stars 增速、社区活跃度 |
| 💰 变现清晰度 | 20% | 商业模式是否清晰 |

**精选标准**：总分 ≥ 7.5 且 Vibecoding 难度 ≥ 4

## 📁 项目结构

```
github-ai-radar/
├── index.html              # 前端页面
├── data/
│   ├── archive.json        # 归档数据库
│   ├── snapshots/          # 每日快照
│   └── trending_*.json     # 原始数据
├── reports/                # Markdown 报告
└── scripts/
    └── analyze_projects.py # 分析脚本
```

## 🔧 本地运行

```bash
# 启动本地服务
python3 -m http.server 8080

# 打开浏览器访问
open http://localhost:8080
```

## 🤖 自动化任务

每日 10:00 自动执行：
1. 获取 GitHub Trending 数据
2. 筛选 AI 相关项目
3. 运行评分分析
4. 更新归档数据库
5. 生成报告并推送

---

*Powered by [WorkBuddy](https://www.codebuddy.cn/) 自动化*
