
---

# 02. 项目目的与学习方法

文件：`docs/02_goal.md`

```markdown
# MiniAgent 项目目的

## 1. 项目背景

本项目不是为了直接开发一个商业级 AI Agent 产品。

项目的主要目的，是通过亲手开发一个简化版 Agent，系统学习现代 AI Agent 的核心架构。

参考的产品和概念包括：

- Coding Agent
- OpenClaw 类 Agent
- Codex 类 Coding Agent
- Tool Calling
- Agent Loop
- Context Management
- MCP

最终目标是在 2～3 个月内完成一个可以写入个人简历的 MiniAgent 项目。

---

# 2. 核心学习目标

通过本项目理解 AI Agent 的基本运行机制：

```text
用户输入
    ↓
Agent
    ↓
LLM 思考
    ↓
是否需要使用工具
    ↓
Tool Calling
    ↓
获取工具结果
    ↓
再次交给 LLM
    ↓
生成最终回答