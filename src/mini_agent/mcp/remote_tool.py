"""MCPTool：把远程 MCP 工具适配成本地 Tool（适配器模式）。

远程工具活在另一个进程里，但经过这层包装，
ToolRegistry 和 Agent 完全分不出它和本地工具的区别。
"""
from mini_agent.tools import Tool
class MCPTool(Tool):
    def __init__(self,client,tool_info):
        self.client=client
        self.name=tool_info["name"]
        self.description=tool_info.get("description","")
        schema=tool_info.get("inputSchema",{})
        self.parameters=schema.get("properties",{})
        self.required=schema.get("required",[])
    def run(self,**kwargs):
        result=self.client.call_tool(self.name,kwargs)
        texts=[]
        for block in result.get("content",[]):
            if block.get("type")=="text":
                texts.append(block.get("text",""))
        return "\n".join(texts) if texts else str(result)
def register_mcp_tools(registry,client):
    count=0
    for tool_info in client.list_tools():
        registry.register(MCPTool(client,tool_info))
        count+=1
    return count       
