from mini_agent.context import (
    build_context,
    estimate_messages_tokens,
    context_report,
)
messages = [{"role": "system", "content": "你是 MiniAgent，一个可以使用工具的 AI 助手。"}]
for i in range(1, 21):
    messages.append({"role": "user", "content": f"第 {i} 个问题：" + "问题内容" * 120})
    messages.append({"role": "assistant", "content": f"第 {i} 个回答：" + "回答内容" * 120})

print("完整历史:", len(messages), "条 |", context_report(messages))
view = build_context(messages, max_tokens=3000)
print("本次视图:", len(view), "条 |", context_report(view))
print("视图第一条:", view[0]["role"], "| 视图第二条:", view[1]["role"])
print("视图里最早的用户问题:", view[1]["content"][:20])
print()

assert view[0]["role"] == "system"
assert view[1]["role"] == "user"
assert len(view) < len(messages)
print("✓ 裁剪生效：system 保留、窗口从 user 消息开始")
print()
# ── 2. 协议安全测试：窗口起点不能在 tool 轮次中间 ──
tool_history = [
    {"role": "system", "content": "你是 MiniAgent。"},
    {"role": "user", "content": "旧问题" + "长" * 300},
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [{"id": "c1", "type": "function",
                        "function": {"name": "calculator", "arguments": "{}"}}],
    },
    {"role": "tool", "tool_call_id": "c1", "content": "旧结果" + "长" * 300},
    {"role": "assistant", "content": "旧回答"},
    {"role": "user", "content": "新问题"},
    {
        "role": "assistant",
        "content": None,
        "tool_calls": [{"id": "c2", "type": "function",
                        "function": {"name": "calculator", "arguments": "{}"}}],
    },
    {"role": "tool", "tool_call_id": "c2", "content": "新结果"},
]
view2 = build_context(tool_history, max_tokens=200)
print("协议测试视图:")
for m in view2:
    print("  ", m["role"], "|", str(m.get("content"))[:20])
assert view2[1]["content"] == "新问题"
print("✓ 协议安全：窗口从最近的 user 消息开始，tool 轮次完整")
print()
# ── 3. 极端预算：兜底逻辑 ──
view3 = build_context(tool_history, max_tokens=1)
print("极端预算视图:", [m["role"] for m in view3])
assert view3[1]["role"] == "user"
print("✓ 兜底逻辑生效（宁可超预算，不破坏协议）")
