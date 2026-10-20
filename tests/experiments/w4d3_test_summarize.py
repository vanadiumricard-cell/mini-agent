from mini_agent.context import (
    summarize_history,
    build_context,
    context_report,
)
from mock_llm import MockLLM
def make_history(rounds):
    history = [{"role": "system", "content": "你是 MiniAgent，一个可以使用工具的 AI 助手。"}]
    history.append({"role": "user", "content": "我叫小明，最近在学习 Python，喜欢用 VS Code 写代码。"})
    history.append({"role": "assistant", "content": "好的小明，我记住了：你在学 Python，用 VS Code。"})
    for i in range(1, rounds + 1):
        history.append({"role": "user", "content": f"闲聊第 {i} 轮：" + "内容" * 100})
        history.append({"role": "assistant", "content": f"回应第 {i} 轮：" + "回应" * 100})
    return history
print("== Mock 压缩测试 ==")
fake = make_history(10)
before_len = len(fake)
mock = MockLLM([{"role": "assistant", "content": "【模拟摘要】用户是小明，在学 Python。"}])
ok = summarize_history(fake, mock, max_tokens=2000)

print("执行压缩:", ok, "| LLM 调用次数:", mock.call_count)
print("消息数: 压缩前", before_len, "→ 压缩后", len(fake))
print("结构:", [m["role"] for m in fake[:3]], "...")
assert ok is True
assert mock.call_count == 1
assert fake[0]["role"] == "system" and fake[1]["role"] == "system"
assert "【早期对话摘要】" in fake[1]["content"]
assert "模拟摘要" in fake[1]["content"]
assert fake[2]["role"] == "user"
assert len(fake) < before_len
print("✓ Mock 机制验证通过")
for ever_messages in fake :
             print(ever_messages)
print()
view = build_context(fake, max_tokens=1500)
print("视图结构:", [m["role"] for m in view[:3]], "...")
assert view[1]["content"].startswith("【早期对话摘要】")
print("✓ 摘要永驻视图")
for ever_messages in fake:
     print(ever_messages)
print()
from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ToolRegistry

llm = DeepSeekLLM()
history = make_history(16)

print("== 真实压缩测试 ==")
print("压缩前:", context_report(history))
ok = summarize_history(history, llm, max_tokens=2000)
print("执行压缩:", ok)
print("压缩后:", context_report(history))
print()
print("生成的摘要:")
print(history[1]["content"])
print()

history.append({"role": "user", "content": "我叫什么名字？我在学什么？用什么编辑器？"})
agent = Agent(llm, ToolRegistry())
final = agent.run(history)
print("问：我叫什么名字？我在学什么？用什么编辑器？")
print("答:", final["content"])


