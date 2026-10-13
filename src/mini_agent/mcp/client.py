"""MCP 客户端：启动服务器进程，通过 stdio 完成协议交互。

职责三层：
1. 进程生命周期：start() / close()
2. 协议收发：_request() / _notify()（拼 JSON、读写行、id 对应）
3. MCP 语义：initialize() / list_tools() / call_tool()
"""
import json
import subprocess
class MCPClient:
    def __init__(self,command):
        self.command=command
        self.process=None
        self.sever_info=None
        self._next_id=1
    #  1. 进程生命周期 
    def start(self):
        self.process=subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            encoding="utf-8",
        )
    def close(self):
        if self.process is None:
            return
        self.process.stdin.close()
        self.process.wait(timeout=5)
    # 2. 协议收发 
    def _send(self,message):
        self.process.stdin.write(json.dumps(message,ensure_ascii=False)+"\n")
        self.process.stdin.flush()
    def _recv(self):
        while True:
            line = self.process.stdout.readline()
            if not line:
                raise RuntimeError("服务器已退出（stdout）达到eof")
            message=json.loads(line)
            if "id"in message: # 有 id 才是响应,通知直接跳过
                return message
    def _request(self,method,params=None):
        """发一个请求，等一个响应；协议层错误抛异常"""
        request_id = self._next_id
        self._next_id += 1
        message = {"jsonrpc": "2.0", "id": request_id, "method": method, "params": params or {}}
        self._send(message)
        response = self._recv()
        if response.get("id") != request_id:
            raise RuntimeError(f"响应 id 不匹配：期望 {request_id}，收到 {response.get('id')}")
        if "error" in response:
            error = response["error"]
            raise RuntimeError(f"MCP 协议错误 {error['code']}: {error['message']}")
        return response["result"]
    def _notify(self, method, params=None):
        """发一个通知：不需要响应"""
        message = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        self._send(message)
     # ── 3. MCP 语义 ──
    def initialize(self):
        result = self._request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "mini-agent", "version": "0.1.0"},
        })
        self.server_info = result.get("serverInfo")
        self._notify("notifications/initialized")   # 握手完成通知
        return result
    def list_tools(self):
        return self._request("tools/list")["tools"]
    def call_tool(self, name, arguments):
        return self._request("tools/call", {"name": name, "arguments": arguments})