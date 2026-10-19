import json
import os
import httpx
from dotenv import load_dotenv
from mini_agent.llm.base import BaseLLM
class DeepSeekLLM(BaseLLM):
    def __init__(self):
        load_dotenv()
        self.last_usage = None
        self.api_key=os.getenv("DEEPSEEK_API_KEY")
        self.url="https://api.deepseek.com/chat/completions"
        self.model="deepseek-flash"
    def chat(self,messages:list[dict],tools:list[dict]|None=None,on_token=None)->dict:
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"}
        data={
            "model":self.model,
            "messages":messages,
        }
        """返回完整 assistant message。
        on_token 不传 = 普通模式；传了 = 流式模式（每收到一段文本就回调 on_token）""" 
        if tools:
            data["tools"]=tools
        if on_token is None:
            return self._chat_once(headers,data)
        return self._chat_stream(headers,data,on_token)
    def _chat_once(self,headers,data):
        data["stream"]=False
        response=httpx.post(self.url,
                            headers=headers,
                            json=data,
                            timeout=30
                            )
        if response.status_code != 200:
            print("API 错误响应:", response.text)
        response.raise_for_status()
        response_data=response.json()
        self.last_usage = response_data.get("usage")
        message=response_data["choices"][0]["message"]
        return message
    def _chat_stream(self,headers,data,on_token):
        data["stream"]=True
        self.last_usage=None
        content_parts=[]
        role="assistant"
        finish_reason=None
        with httpx.stream("POST",self.url,headers=headers,json=data,timeout=60) as response:
            """
            长连接httpx.stream
            建立**一条持续不断的 TCP 连接**。模型每生成一小块文本，服务器就通过**同一个 TCP 连接**，把这一小段 chunk 推过来。
            搭配flush完成流式输出
            timeout 参数：是【读超时 (read_timeout)】，指：连续 60 秒没有收到任何新数据，就抛出超时异常
            """
            if response.status_code != 200:
                print("API 错误响应:", response.read().decode("utf-8",errors="replace"))
            response.raise_for_status()
            #提取字典并拼装
            for line in response.iter_lines():
                if not line or not line.startswith("data:"):
                    continue
                payload=line[5:].strip()
                if payload=="[DONE]":
                    break
                chunk=json.loads(payload)
                if chunk.get("usage"):
                    self.last_usage=chunk["usage"]
                choices=chunk.get("choices") or []
                if not choices:
                    continue
                choice=choices[0]
                delta=choice.get("delta") or {}
                role=delta.get("role",role)
                piece=delta.get("content") or ""
                if piece:
                    content_parts.append(piece)
                    on_token(piece)
                if choice.get("finish_reason"):
                    finish_reason=choice["finish_reason"]
        return {"role":role,"content":"".join(content_parts)}
    
        
        
 

