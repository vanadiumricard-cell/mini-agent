import os
import httpx
from dotenv import load_dotenv
from mini_agent.llm.client import get_tools
import json
from mini_agent.tools import calculator,ToolRegistry
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

url = "https://api.deepseek.com/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
messages=[
    {
      "role": "user",
      "content":"帮我计算 123*456"
    }

]
data = {
    "model": "deepseek-v4-flash",
    "messages": messages,
    "tools": get_tools()
}

response = httpx.post(
    url,
    headers=headers,
    json=data,
    timeout=60
)

response.raise_for_status()

response_data = response.json()
message=response_data["choices"][0]["message"]
tool_call=message["tool_calls"][0]
tool_name=tool_call["function"]["name"]
arguments=json.loads(
    tool_call["function"]["arguments"]
)
print("工具名称", tool_name)
print("工具参数", arguments)
registry=ToolRegistry()
registry.register("calculator", calculator)
tool=registry.get(tool_name)
result=tool(
     arguments["a"],
     arguments["b"],
     arguments["operation"]
)
messages.append(message)
messages.append(
    {
        "role":"tool",
        "tool_call_id":tool_call["id"],
        "content":str(result)
    }

)

print("工具执行结果" , result)
data = {
    "model": "deepseek-v4-flash",
    "messages": messages
}

response = httpx.post(
    url,
    headers=headers,
    json=data,
    timeout=60
)

response.raise_for_status()

final_data = response.json()

final_answer = final_data["choices"][0]["message"]["content"]

print("最终答案:", final_answer)