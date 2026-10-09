from mini_agent.llm.client import DeepSeekLLM
from mini_agent.memory import MemoryManager
from mini_agent.context import build_context, estimate_messages_tokens
llm = DeepSeekLLM()
TURNS = 40
BUDGET = 4000
FILLER = "接下来是一些无关紧要的闲聊内容，用来把上下文撑大。" * 10
def make_turns():
    turns = ["你好，我叫小明，正在学习 Python，我的项目叫 mini-agent。"]
    for i in range(2, TURNS + 1):
        turns.append(f"闲聊第 {i} 轮：" + FILLER)
    return turns
def fake_reply():
    return {"role": "assistant", "content": "好的，收到。"}
# ── 策略 A：裸奔（不做任何管理）──
storage_a = [{"role": "system", "content": "你是 MiniAgent。"}]
sizes_a = []
for text in make_turns():
    storage_a.append({"role": "user", "content": text})
    sizes_a.append(estimate_messages_tokens(storage_a))
    storage_a.append(fake_reply())

storage_b = [{"role": "system", "content": "你是 MiniAgent。"}]
sizes_b = []
for text in make_turns():
    storage_b.append({"role": "user", "content": text})
    view = build_context(storage_b, max_tokens=BUDGET)
    sizes_b.append(estimate_messages_tokens(view))
    storage_b.append(fake_reply())

print("C 策略运行中（每轮摘要会真实调用 API）...")
memory_c = MemoryManager(llm, max_tokens=BUDGET)
memory_c.add({"role": "system", "content": "你是 MiniAgent。"})
sizes_c = []
for i, text in enumerate(make_turns(), 1):
    memory_c.add({"role": "user", "content": text})
    if memory_c.compress():
        print(f"  第 {i} 轮触发压缩（累计 {memory_c.compress_count} 次）")
    sizes_c.append(estimate_messages_tokens(memory_c.context()))
    memory_c.add(fake_reply())
    print()
print(f"{'轮次':<6} | {'A 裸奔':>8} | {'B 纯窗口':>8} | {'C 窗口+摘要':>10}")
print("-" * 44)
for i in range(TURNS):
    print(f"{i+1:<8} | {sizes_a[i]:>8} | {sizes_b[i]:>8} | {sizes_c[i]:>10}")
print("-" * 44)
sum_a, sum_b, sum_c = sum(sizes_a), sum(sizes_b), sum(sizes_c)
print(f"总发送量：A={sum_a} | B={sum_b} | C={sum_c} token")
print(f"C 相对 A 节省：{100 - sum_c * 100 // sum_a}%")
print(f"A 的最终视图：{sizes_a[-1]} token（还在涨！）")
print()
# ── 记忆检查 ──
print("== 记忆检查：'小明'还在最终视图里吗？==")
print("A:", any("小明" in str(m) for m in storage_a))
print("B:", any("小明" in str(m) for m in build_context(storage_b, max_tokens=BUDGET)))
print("C:", any("小明" in str(m) for m in memory_c.context()))
print()

# ── C 的真实摘要 ──
for m in memory_c.messages:
    if m.get("role") == "system" and "【早期对话摘要】" in str(m.get("content", "")):
        print("C 的当前摘要:")
        print(m["content"])
