from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import (
    ToolRegistry,
    get_current_time, get_current_time_schema,
    read_file, read_file_schema,
    list_files, list_files_schema,
    write_file, write_file_schema,
)
'''
print("== 直接调用工具 ==")
print("越界测试（直接拒绝，不会询问）:")
print(write_file("C:/temp/hack.txt", "test"))
print()
print("正常写入（看到提示请输入 y）:")
print("结果:", write_file("sandbox/hello.txt", "你好，MiniAgent！\n这是第一个由工具写入的文件。"))
print()
print("读回来验证:")
print(read_file("sandbox/hello.txt"))
print()
print("拒绝测试（看到提示请输入 n）:")
print("结果:", write_file("sandbox/reject_test.txt", "这行不应该被写入"))
print("验证（应该报文件不存在）:")
print(read_file("sandbox/reject_test.txt"))
print()
'''
llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register("get_current_time", get_current_time, get_current_time_schema)
registry.register("read_file", read_file, read_file_schema)
registry.register("list_files", list_files, list_files_schema)
registry.register("write_file", write_file, write_file_schema)
agent = Agent(llm, registry)
'''
print("== Agent 写入测试（看到提示请输入 y）==")
messages = [
    {"role": "user", "content": "请在 sandbox 目录里新建一个文件 note.txt，内容写上：MiniAgent 学习笔记 - 由 Agent 自动创建"}
]
final = agent.run(messages)
print("答:", final["content"])
print()
a=0
for message in messages:
    
    if message.get("tool_calls"):
        a=a+1
        for call in message["tool_calls"]:
            print("第",a,"次调用:", call["function"]["name"], "参数:", call["function"]["arguments"][:100])
print()
for ever_messages in messages:
             print(ever_messages)
'''
print("== 组合任务：时间 + 写入（看到提示请输入 y）==")
messages2 = [
    {"role": "user", "content": "获取当前时间，并把它写入 sandbox/time.txt"}
]
final2 = agent.run(messages2)
print("答:", final2["content"])
print()
a=0
for message in messages2:
    
    if message.get("tool_calls"):
        a=a+1
        for call in message["tool_calls"]:
            print("第",a,"次调用:", call["function"]["name"], "参数:", call["function"]["arguments"][:100])
print()
for ever_messages in messages2:
             print(ever_messages)
print()
print("验证 time.txt:", read_file("sandbox/time.txt"))
