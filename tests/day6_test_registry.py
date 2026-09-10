from mini_agent.tools import ToolRegistry, calculator
registry = ToolRegistry()
registry.register("calculator", calculator)
tool_name="calculator"
tool=registry.get(tool_name)
result=tool(10,40,"add")
print(f"工具 {tool_name},结果 {result}")
