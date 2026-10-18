"""MCPTool：把远程 MCP 工具适配成本地 Tool（适配器模式）。

远程工具活在另一个进程里，但经过这层包装，
ToolRegistry 和 Agent 完全分不出它和本地工具的区别。
"""
from mini_agent.mcp.client import MCPConnectionError
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
        try:
            result=self.client.call_tool(self.name,kwargs)
        except MCPConnectionError:
            # 连接断了 → 重连一次再试（简单版自愈）
            # 注意：重试有"重复执行"风险（请求可能已送达）——只对幂等工具安全
            #幂等工具：重复执行没有区别的工具，计算器，非幂等工具：读写，命令行，重复执行容易出问题
            self.client.restart()
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
