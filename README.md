# OpenMaintainer

一个面向 GitHub 开源仓库维护场景的 **AI Agent Demo**：
自动完成 Issue 分拣、PR 初审、测试建议、README/Changelog 草稿生成。

> 目标：**最快可运行、可展示具体成果**。

---

## 功能概览

OpenMaintainer 提供 4 个核心 Agent（可串联，也可独立调用）：

1. **Issue Triage Agent**
   - 读取 Issue 标题、正文、标签、历史评论
   - 产出：优先级、分类、处理建议、需要补充的信息清单

2. **PR Review Agent**
   - 输入 PR diff / changed files / CI 结果
   - 产出：风险点评、代码规范建议、是否建议合并

3. **Test Suggestion Agent**
   - 根据改动生成测试建议（单测/集成/回归）
   - 输出可复制到 PR 评论的测试计划

4. **Docs Agent（README/Changelog）**
   - 从 commits / PR 信息生成 README 更新草稿与 Changelog 条目

---

## 项目结构

```bash
openmaintainer/
├─ src/openmaintainer/
│  ├─ agents.py           # Agent 定义
│  ├─ schemas.py          # 结构化输出 schema
│  ├─ github_tools.py     # GitHub API 工具函数
│  ├─ runner.py           # CLI 入口执行器
│  └─ prompts.py          # 各 Agent 系统提示词
├─ scripts/
│  └─ demo_payloads/      # 本地演示输入
├─ .github/workflows/
│  └─ openmaintainer.yml  # GitHub Actions 自动化工作流
├─ pyproject.toml
├─ .env.example
└─ README.md
```

---

## 快速开始

### 1) 安装

```bash
python -m venv .venv
source .venv/bin/activate


### 2) 配置环境变量

复制示例：

```bash
cp .env.example .env
```

至少需要：

- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- `GITHUB_REPOSITORY`（例如 `owner/repo`）

### 3) 本地运行 Demo

```bash
---

## GitHub Actions 集成

仓库已提供 `.github/workflows/openmaintainer.yml`，支持：

- `issues.opened/reopened/edited` 自动触发 Issue 分拣
- `pull_request.opened/synchronize/reopened` 自动触发 PR 审查与测试建议
- `workflow_dispatch` 手动触发全流程

你可以让 action 将结果写入：

- Issue Comment
- PR Review Comment
- Step Summary

---

## 使用场景示例

- 新 Issue 进来后，自动给出：
  - `type: bug/feature/question`
  - `priority: p0~p3`
  - 是否缺少复现步骤
- 新 PR 提交后，自动给出：
  - 潜在 breaking changes
  - 建议补充的测试用例
  - 文档是否需要更新
- 发布前自动整理：
  - 本周期 Changelog 草稿
  - README 新增功能说明草稿

---

## 可演示成果（适合快速交付）

1. **一键跑通的本地 CLI Demo**
2. **可见的结构化输出 JSON**（便于验收）
3. **GitHub Actions 自动触发日志**
4. **可复制粘贴到真实仓库的工作流模板**

---

## 后续可扩展

- 多 Agent handoff（如 Issue Agent 将高风险问题交给 PR Agent）
- 引入 tracing 观测 Agent 决策链路
- 增加规则引擎（CODEOWNERS、标签策略、分支保护策略）
- 支持多语言模板（中文/英文维护评论）

---

## License

MIT
