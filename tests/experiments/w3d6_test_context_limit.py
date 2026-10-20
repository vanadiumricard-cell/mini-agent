from pathlib import Path

from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ToolRegistry, ReadFileTool

ROOT = Path(__file__).resolve().parents[1]

# ── 0. 造一个 1000 行的测试文件（脚本直接写，不走工具、不用确认）──
big = ROOT / "sandbox" / "big.txt"
big.parent.mkdir(exist_ok=True)
big.write_text(
    "\n".join(
        f"第 {i} 行：这是用于测试上下文问题的文件，内容是凑数的普通文字。"
        for i in range(1, 1001)
    ),
    encoding="utf-8",
)
tool = ReadFileTool()
full_size = len(big.read_text(encoding="utf-8"))
capped = tool.run("sandbox/big.txt")
print(f"旧行为（无上限）：一次读入约 {full_size} 字符")
print(f"新行为（200 行上限）：一次读入约 {len(capped)} 字符")
print(f"单次开销缩小到约 {len(capped) * 100 // full_size}%")
print()

# ── 1. 直接看输出格式（免费）──
print("== 默认读取（开局 + 结尾提示）==")
lines = capped.splitlines()
print("\n".join(lines[:5]))
print("...")
print("\n".join(lines[-2:]))
print()
print("== 指定范围读取（第 451-460 行）==")
print(tool.run("sandbox/big.txt", start_line=451, end_line=460))
print()
print("== 越界测试 ==")
print(tool.run("sandbox/big.txt", start_line=5000))
print()
llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register(ReadFileTool())
agent = Agent(llm, registry)


def ask(question):
    messages = [{"role": "user", "content": question}]
    final = agent.run(messages)
    reads = [m for m in messages if m.get("role") == "tool"]
    total_chars = sum(len(str(m)) for m in messages)
    print("问:", question)
    print("答:", final["content"])
    print(f"（工具被调用 {len(reads)} 次 | 本轮总字符 {total_chars}）")
    print()
    for ever_messages in messages:
                 print(ever_messages)


ask("sandbox/big.txt 的第 50 行是什么？")
ask("sandbox/big.txt 一共有多少行？")
ask("sandbox/big.txt 的第 500 行是什么？不要猜，亲自看")