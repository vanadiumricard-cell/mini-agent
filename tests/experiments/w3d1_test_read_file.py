from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ToolRegistry, read_file, read_file_schema 
print("== 直接调用工具 ==")
print("读 pyproject.toml（前 200 字符）:")
print(read_file("pyproject.toml")[:200])
print()
print("越界测试:", read_file("C:/Windows/win.ini"))
print("逃逸测试:", read_file("../secret.txt"))
print("不存在测试:", read_file("no_such_file.txt"))
print("目录测试:", read_file("src"))
print()
llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register("read_file", read_file, read_file_schema)
agent = Agent(llm, registry)

messages = [
    {"role": "user", "content": "读一下 pyproject.toml，告诉我这个项目要求的 Python 版本和构建工具是什么"}
]
final = agent.run(messages)
print("答:", final["content"])
print()
for message in messages:
    if message.get("tool_calls"):
        for call in message["tool_calls"]:
            print("  调用:", call["function"]["name"], call["function"]["arguments"])
print()

messages2 = [
    {"role": "user", "content": "读一下 docs/goal.md，用一句话总结这个项目的目标"}
]
final2 = agent.run(messages2)
print("答:", final2["content"])