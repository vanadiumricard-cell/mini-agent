import os
import httpx
from dotenv import load_dotenv
from mini_agent.llm.base import BaseLLM
class DeepSeekLLM(BaseLLM):
    def __init__(self):
        load_dotenv()
        self.api_key=os.getenv("DEEPSEEK_API_KEY")
        self.url="https://api.deepseek.com/chat/completions"
        self.model="deepseek-v4-flash"
    def chat(self,messages:list[dict])->str:
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"}
        data={
            "model":self.model,
            "messages":messages
            ,
            "stream":False
        }
        response=httpx.post(self.url,
                            headers=headers,
                            json=data,
                            timeout=30
                            )
        response.raise_for_status()
        response_data=response.json()
        answer=response_data["choices"][0]["message"]["content"]
        return answer
def get_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "calculator",
                "description": "进行基本数学计算",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {
                            "type": "number",
                            "description": "第一个数字"
                        },
                        "b": {
                            "type": "number",
                            "description": "第二个数字"
                        },
                        "operation": {
                            "type": "string",
                            "enum": [
                                "add",
                                "subtract",
                                "multiply",
                                "divide"
                            ],
                            "description": "计算类型"
                        }
                    },
                    "required": [
                        "a",
                        "b",
                        "operation"
                    ]
                }
            }
        }
    ]

