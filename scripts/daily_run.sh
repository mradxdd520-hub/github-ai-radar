#!/bin/bash
# GitHub AI 雷达 - 每日运行脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
REPORTS_DIR="$PROJECT_DIR/reports"
TODAY=$(date +%Y-%m-%d)

# 确保 reports 目录存在
mkdir -p "$REPORTS_DIR"

# 生成报告
echo "🤖 GitHub AI 雷达 - 生成 $TODAY 报告..."
python3 "$SCRIPT_DIR/analyze_projects.py" > "$REPORTS_DIR/$TODAY.md"

echo "✅ 报告已生成: $REPORTS_DIR/$TODAY.md"

# 如果在 git 仓库中，自动提交
if [ -d "$PROJECT_DIR/.git" ]; then
    cd "$PROJECT_DIR"
    git add reports/
    git commit -m "📊 Daily report: $TODAY" || echo "No changes to commit"
    git push origin main || echo "Push failed, please push manually"
fi
