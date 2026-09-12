from mini_agent.tools import ToolRegistry
from mini_agent.llm.client import DeepSeekLLM
class Agent:
   def __init__(self,llm,tool_registry):
         self.llm=llm
         self.tool_registry=tool_registry
   def decide_tool(self,user_input):
        if"计算"in user_input:
             return"calculator"
        return None
   def run_tool(self,tool_name,*args):
        tool=self.tool_registry.get(tool_name)
        if tool is None:
             raise ValueError(f"找不到工具：{tool_name}")
        return tool(*args)
   def run(self,messages):
        response=self.llm.chat(messages)
        return response
                              
        

