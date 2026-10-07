from mini_agent.tools import Tool, ToolRegistry


class BadTool(Tool):
    name = "bad_tool"
    description = "故意写错的工具"
    parameters = {
        "x": {"type": "string", "dsecription": "拼错的键"},
    }
    required = ["x"]

    def run(self, x):
        return x


registry = ToolRegistry()
try:
    registry.register(BadTool())
    print("没有拦截，异常！")
except ValueError as error:
    print("成功拦截:", error)