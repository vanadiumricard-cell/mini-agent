import json
import os
import sys
import time
import httpx
from dotenv import load_dotenv
from mini_agent.llm.base import BaseLLM
class DeepSeekLLM(BaseLLM):
    RETRY_STATUS = {429, 500, 502, 503, 504}
     # 这些状态码值得重试
    def __init__(self):
        load_dotenv()
        self.last_usage = None
        self.api_key=os.getenv("DEEPSEEK_API_KEY")
        self.url="https://api.deepseek.com/chat/completions"
        self.model="deepseek-flash"
        self.max_attempts = 3
        self.timeout = 30 
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
    #非流式重试
    def _post_with_retry(self,headers,data):
        for attempt in range(1, self.max_attempts+1):
            try:
                response = httpx.post(self.url, headers=headers, json=data, timeout=self.timeout)
            except (httpx.TimeoutException, httpx.NetworkError) as err:
                if attempt==self.max_attempts:
                    raise
                wait=2**(attempt - 1)#**乘方
                print(f"[网络错误 {type(err).__name__}，{wait}s 后重试（{attempt}/{self.max_attempts}）]",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            if response.status_code in self.RETRY_STATUS and attempt<self.max_attempts:
                wait=2**(attempt - 1)
                print(f"  [HTTP {response.status_code}，{wait}s 后重试（{attempt}/{self.max_attempts}）]",
                      file=sys.stderr)
                time.sleep(wait)
                continue
            return response
    def _chat_once(self,headers,data):
        data["stream"]=False
        response=self._post_with_retry(headers,data)
        if response.status_code != 200:
            print("API 错误响应:", response.text)
        response.raise_for_status()
        response_data=response.json()
        self.last_usage = response_data.get("usage")
        message=response_data["choices"][0]["message"]
        return message
    def _chat_stream(self,headers,data,on_token):
        data["stream"]=True
        for attempt in range(1, self.max_attempts + 1):
            emitted = [False]              # 本轮是否已吐过文字（吐过就不能安全重试）
            def emit(piece):
                emitted[0] = True
                on_token(piece)
            try:
                return self._stream_once(headers, data, emit)
            except (httpx.TimeoutException, httpx.NetworkError) as err:
                if emitted[0] or attempt == self.max_attempts:
                    raise
                wait = 2 ** (attempt - 1)
                print(f"  [流式连接失败 {type(err).__name__}，{wait}s 后重试（{attempt}/{self.max_attempts}）]",
                      file=sys.stderr)
                time.sleep(wait)
            except httpx.HTTPStatusError as err:
                if (err.response.status_code in self.RETRY_STATUS
                        and not emitted[0] and attempt < self.max_attempts):
                    wait = 2 ** (attempt - 1)
                    print(f"  [HTTP {err.response.status_code}，{wait}s 后重试（{attempt}/{self.max_attempts}）]",
                          file=sys.stderr)
                    time.sleep(wait)
                else:
                    raise
    def _stream_once(self, headers, data, on_token):
        self.last_usage = None
        content_parts = []
        role = "assistant"
        tool_states = {}          # index -> {"id","type","name","arguments"}

        with httpx.stream("POST", self.url,
                          headers=headers,
                          json=data,
                          timeout=60) as response:
            """
            长连接httpx.stream
            建立**一条持续不断的 TCP 连接**。模型每生成一小块文本，服务器就通过**同一个 TCP 连接**，把这一小段 chunk 推过来。
            搭配flush完成流式输出
            timeout 参数：是【读超时 (read_timeout)】，指：连续 60 秒没有收到任何新数据，就抛出超时异常
            """
            if response.status_code != 200:
                print("API 错误响应:", response.read().decode("utf-8", errors="replace"))
            response.raise_for_status()
            #raise_for_status()内置方法，status_code>=400：主动抛出httpx.HTTPStatusError异常
            for line in response.iter_lines():
                if not line or not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                chunk = json.loads(payload)
                if chunk.get("usage"):
                    self.last_usage = chunk["usage"]
                choices = chunk.get("choices") or []
                if not choices:
                    continue
                choice = choices[0]
                delta = choice.get("delta") or {}
                role = delta.get("role", role)

                piece = delta.get("content") or ""
                if piece:
                    content_parts.append(piece)
                    on_token(piece)

                for tc in delta.get("tool_calls") or []:
                    
                    idx = tc.get("index", 0)
                    state = tool_states.setdefault(
                        idx, {"id": None, "type": "function", "name": "", "arguments": ""})
                    if tc.get("id"):
                        state["id"] = tc["id"]
                    if tc.get("type"):
                        state["type"] = tc["type"]
                    fn = tc.get("function") or {}
                    if fn.get("name"):
                        state["name"] = fn["name"]
                    if fn.get("arguments"):
                        state["arguments"] += fn["arguments"]

        message = {"role": role, "content": "".join(content_parts) or None}
        if tool_states:
            message["tool_calls"] = [
                {"id": state["id"], "type": state["type"],
                 "function": {"name": state["name"], "arguments": state["arguments"]}}
                for _, state in sorted(tool_states.items())
            ]
        return message
        
    
        
        
 

