from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.memory import MemoryManager
from mini_agent.tools import ToolRegistry
llm = DeepSeekLLM()
agent = Agent(llm, ToolRegistry())
memory = MemoryManager(llm, max_tokens=2500)
memory.add({"role": "system", "content": "你是 MiniAgent，回答尽量简洁。"})
FILLER = "接下来是一些无关紧要的闲聊内容，用来把上下文撑大。" * 15
def turn(text, label):
    memory.add({"role": "user", "content": text})
    before = memory.compress_count
    final = agent.run(memory)
    fired = memory.compress_count - before
    print(f"【{label}】压缩触发: {'✅ 是' if fired else '— 否'}")
    print(f"  油表: {memory.stats()}")
    print(f"  回答: {final['content'][:100]}")
    print()
    return final
def print_summary(label):
    for m in memory.messages:
        if m.get("role") == "system" and "【早期对话摘要】" in str(m.get("content", "")):
            print(f"----- 当前摘要（{label}）-----")
            print(m["content"])
            print()
turn("你好！我叫小明，正在学习 Python，平时用 VS Code 写代码。", "第 1 轮：自我介绍")
turn("我最近在做一个小项目，叫 mini-agent。", "第 2 轮：项目信息")
for i in range(1, 7):
    turn(FILLER, f"填充 {i}")
print("========== 检查 1：压缩之后，还记得最初的事实吗？==========")
answer1 = turn("问几个问题：我叫什么名字？在学什么？我的项目叫什么？", "检查 1")
print("完整回答:", answer1["content"])
print()
print_summary("检查 1 之后")
for i in range(7, 13):
    turn(FILLER, f"填充 {i}")

# ── 检查 2：二次压缩（滚动摘要）后 ──
print("========== 检查 2：又压了一轮之后，还记得吗？==========")
answer2 = turn("再考考你：我叫什么名字？用什么编辑器？项目叫什么？", "检查 2")
print("完整回答:", answer2["content"])
print()
print_summary("检查 2 之后")

