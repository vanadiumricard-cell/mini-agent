from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ToolRegistry,calculator,calculator_schema
registry=ToolRegistry()
registry.register("calculator",calculator,calculator_schema)
schemas=registry.get_schemas()
print("schema数量",len(schemas))
print("schema",schemas[0])
print()
llm=DeepSeekLLM()
messages=[{"role":"user","content":"帮我计算88*99"}]
message=llm.chat(messages,tools=schemas)
tool_calls=message.get("tool_calls")
if tool_calls:
    name=tool_calls[0]["function"]["name"]
    print("模型选择了",name)
    tool=registry.get(name)
    print("注册表取回:", tool)
    print("就是 calculator 吗?", tool is calculator)
else:
    print("模型直接回答:", message.get("content"))
