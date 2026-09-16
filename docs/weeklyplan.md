
---

# 04. 每周/每日计划

文件：`docs/04_weekly_plan.md`

这里不需要现在一次性把 10 周的每天都写死。

因为你在学习过程中可能会：

- 某个知识掌握得很快
- 某个知识需要多花两天
- 遇到 Bug
- 想增加新的功能

因此我建议采用：

> **总体路线固定 + 每周详细计划动态调整**

目前先记录 Week 1：

```markdown
# MiniAgent Weekly Plan

# Week 1：LLM Client 基础

## 本周目标

完成：

MiniAgent v0.1

核心能力：

Day 1  项目骨架 / Python 包
  ↓
Day 2  LLM 抽象接口
  ↓
Day 3  HTTP / JSON / API
  ↓
Day 4  DeepSeek API 接入
  ↓
Day 5  多轮对话
  ↓
Day 6  Tool + ToolRegistry
  ↓
Day 7  真正的 Tool Calling
# Week 2：Agent Loop 与工具系统（v0.4）

## 本周目标
完成：MiniAgent v0.4 —— 可交互、自动调用工具的 Agent

w2d1 chat() 支持 tools → w2d2 schema 绑定 → w2d3 Agent Loop → w2d4 鲁棒性
→ w2d5 接入 chat.py + System Prompt → w2d6 第二个工具 → w2d7 收官