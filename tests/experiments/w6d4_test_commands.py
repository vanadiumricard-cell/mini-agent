import io
from contextlib import redirect_stdout

from mini_agent.chat import handle_command
from mini_agent.llm.base import demollm
from mini_agent.memory import MemoryManager
from mini_agent.tools import CalculatorTool, CurrentTimeTool, ToolRegistry
llm = demollm()
memory = MemoryManager(llm)
memory.add({"role": "system", "content": "你是 MiniAgent。"})
memory.add({"role": "user", "content": "你好"})
memory.add({"role": "assistant", "content": "你好！"})

registry = ToolRegistry()
registry.register(CalculatorTool())
registry.register(CurrentTimeTool())


def run(text):
    buf = io.StringIO()
    with redirect_stdout(buf):
        handle_command(text, memory, registry, llm)
    output = buf.getvalue()
    print(output)
    return output


# /help
output = run("/help")
assert "/stats" in output

# /tools
output = run("/tools")
assert "calculator" in output
assert "get_current_time" in output

# /stats
output = run("/stats")
assert "工具" in output

# /clear
output = run("/clear")
assert len(memory.messages) == 1
assert memory.messages[0]["role"] == "system"

# 未知命令
output = run("/foo")
assert "未知命令" in output

print("✓ 命令系统全部场景通过")