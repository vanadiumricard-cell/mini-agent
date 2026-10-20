from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ToolRegistry, list_files, list_files_schema
print("== 直接调用工具 ==")
print("工具目录:")
print(list_files("src/mini_agent/tools"))
print()
print("项目根（第一层）:")
print(list_files())
print()
print("所以py文件：")
print(list_files(".","**/*.py"))
print()
print("越界测试:", list_files("C:/Windows"))
print("不存在测试:", list_files("no_such_dir"))
print()
llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register("list_files", list_files, list_files_schema)
agent = Agent(llm, registry)

messages = [
    {"role": "user", "content": "项目里的 src/mini_agent/tools 目录下有哪些文件？"}
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
    {"role": "user", "content": "帮我找出项目里所有的 Python 文件，只列路径"}
]
final2 = agent.run(messages2)
print("答:", final2["content"])
print()
for message in messages2:
    if message.get("tool_calls"):
        for call in message["tool_calls"]:
            print("  调用:", call["function"]["name"], call["function"]["arguments"])