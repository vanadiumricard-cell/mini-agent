# MiniAgent 学习路线

这是整个项目的**总路线图**。

我建议暂时按照 **10 周**设计。这样比较适合你目前的基础，也符合 2～3 个月完成一个简历项目的目标。

## 项目周期

预计：

10 周

目标：

完成 MiniAgent v1.0

## Phase 1：LLM 基础

### Week 1：Python 项目与 LLM Client

学习：

- Python Package
- Module
- Import
- Class
- Type Hint
- HTTP
- JSON
- API

实现：

```
MiniAgent
    ↓
LLMClient
    ↓
LLM API
```

## Phase 2：Agent 基础

### Week 2：消息与多轮对话

学习：

- Message
- System Prompt
- User Message
- Assistant Message
- Conversation History

实现：

```
User
 ↓
Agent
 ↓
Message History
 ↓
LLM
```

### Week 3：Tool Calling

学习：

- Function Calling
- JSON Schema
- Python Function
- Tool Interface

实现：

```
Agent
 ↓
LLM
 ↓
选择 Tool
 ↓
执行 Python Function
```

成果：

MiniAgent v0.3
能够调用工具。

### Week 4：Agent Loop

学习：

- while Loop
- Agent Reasoning Loop
- Tool Result
- Stop Condition

实现：

```
LLM
 ↓
需要工具？
 ↓
Yes → Tool
 ↓
Tool Result
 ↓
LLM
 ↓
No
 ↓
Final Answer
```

成果：

MiniAgent v0.4
具备基本 Agent 能力。

## Phase 3：Agent 系统

### Week 5：Tool System

学习：

- Base Class
- Abstract Interface
- Registry Pattern

实现：

```
Tool Registry
├── Calculator
├── File Tool
└── Search Tool
```

成果：

MiniAgent v0.5
拥有可扩展的工具系统。

### Week 6：文件系统与 Coding Agent

学习：

- Python File IO
- Path
- Directory
- Code Execution

实现：

```
Agent
 ↓
读取文件
 ↓
分析代码
 ↓
修改文件
```

成果：

MiniAgent v0.6
初步具备 Coding Agent 能力。

### Week 7：Memory 与 Context

学习：

- Context Window
- Token
- Short-term Memory
- Context Compression

实现：

```
Conversation
    ↓
Memory Manager
    ↓
Context
    ↓
LLM
```

成果：

MiniAgent v0.7
支持基础上下文管理。

## Phase 4：现代 Agent 技术

### Week 8：MCP

学习：

- MCP 基本概念
- Client
- Server
- Tool Discovery

实现：

```
MiniAgent
     ↓
MCP Client
     ↓
External Tools
```

成果：

MiniAgent v0.8
支持基础 MCP。

## Phase 5：工程完善

### Week 9：CLI 与用户体验

学习：

- CLI
- Command
- Streaming
- Error Handling

实现：

```
mini-agent
> 帮我分析这个项目
```

成果：

MiniAgent v0.9
拥有基础命令行交互。

### Week 10：测试与项目整理

完成：

- Code Refactor
- Unit Test
- Documentation
- README
- Architecture Diagram

最终成果：

MiniAgent v1.0
