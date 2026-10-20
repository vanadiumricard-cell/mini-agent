from mini_agent.agent import Agent
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import (
    ToolRegistry,
    calculator, calculator_schema,
    get_current_time, get_current_time_schema,
    read_file, read_file_schema,
    list_files, list_files_schema,
)
llm = DeepSeekLLM()
registry = ToolRegistry()
registry.register("calculator", calculator, calculator_schema)
registry.register("get_current_time", get_current_time, get_current_time_schema)
registry.register("read_file", read_file, read_file_schema)
registry.register("list_files", list_files, list_files_schema)
agent = Agent(llm, registry)
def show_result(title,messages,final):
    print("=" *50)
    print(title)
    print("=" *50)
    print("答：",final["content"])
    print()
    print("agent的动作：")
    a=0
    for message in messages:
        
        if message.get("tool_calls"):
            a=a+1
            for call in message["tool_calls"]:
                
                print("第",a,"次调用")
                
                print("调用：",call["function"]["name"],call["function"]["arguments"])
    total_chars=sum(len(str(m))for m in messages)
    total_rounds=sum(1 for m in messages if m.get("tool_calls"))
    print(f"统计: 消息 {len(messages)} 条 | 工具轮次 {total_rounds} | 总字符 {total_chars}")
    print()
'''
messages1 = [{"role": "user", "content": "用两三句话介绍这个项目是做什么的"}]
final1 = agent.run(messages1)
show_result("问题 1: 项目是干什么的", messages1, final1)
messages2 = [{"role": "user", "content": "src/mini_agent/agent.py 是干什么的？用三句话解释"}]
final2 = agent.run(messages2)
show_result("问题 2: agent.py 是干什么的", messages2, final2)
messages3 = [{"role": "user", "content": "用户问一个问题后，Agent 是如何一步步调用工具并给出回答的？请结合项目里的具体文件解释"}]
final3 = agent.run(messages3)
show_result("问题 3: 工具调用全流程", messages3, final3)
'''
messages4 = [{"role": "user", "content": "这个项目有哪些工具？"}]
final4 = agent.run(messages4)
show_result("附加: 有哪些工具", messages4, final4)

print(">>> 同一会话里追问一句：")
messages4.append({"role": "user", "content": "这些工具是在哪里注册的？"})
final5 = agent.run(messages4)
show_result("附加: 追问（同一会话）", messages4, final5)