from mini_agent.tools import ToolRegistry, calculator
registry = ToolRegistry()
registry.register("calculator", calculator)
tool=registry.get("calculator")
print(tool(10,20,"add"))
