from mini_agent.tools import ToolRegistry, calculator, calculator_schema

from mini_agent.llm.client import DeepSeekLLM
llm=DeepSeekLLM()
registry=ToolRegistry()
registry.register("calculator",calculator,calculator_schema)
messages=[
    {"role":"user","content":"帮我计算 123*456"}

] 
message=llm.chat(messages,tools=registry.get_schemas)
print("完整message",message)
print()
tool_calls=message.get("tool_calls")
if tool_calls:
    call=tool_calls[0]
    print("工具名字", call["function"]["name"])
    print("参数",call["function"]["arguments"])
else:
    print("模型直接回答",message.get("content"))


