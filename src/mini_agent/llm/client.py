
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
    def chat(self,messages:list[dict],tools:list[dict]|None=None)->str:
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"}
        data={
            "model":self.model,
            "messages":messages,
            "stream":False
        }
        if tools is not None:
            data["tools"]=tools

        response=httpx.post(self.url,
                            headers=headers,
                            json=data,
                            timeout=30
                            )
        response.raise_for_status()
        response_data=response.json()
        message=response_data["choices"][0]["message"]
        return message
        
 

