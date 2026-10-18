"""MCP 客户端：启动服务器进程，通过 stdio 完成协议交互。

职责三层：
1. 进程生命周期：start() / close()
2. 协议收发：_request() / _notify()（拼 JSON、读写行、id 对应）
3. MCP 语义：initialize() / list_tools() / call_tool()
"""
import json
import subprocess
class MCPConnectionError(RuntimeError):
    """连接层故障：服务器崩了 / 管道断了（可以重连再试）"""
class MCPClient:
    def __init__(self,command):
        self.command=command
        self.process=None
        self.server_info=None
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
            #子对象不存在
            return
        try:
            self.process.stdin.close()
        except(BrokenPipeError,OSError):
            pass
        # 管道可能已经断了——收尾时不要被它绊倒:如果是BrokenPipeError,OSError这两种错误类型（内置），就pass(不理他，继续运行)，如果是预设外的错误类型，依旧直接报错
        self.process.wait(timeout=5)
    def restart(self):
        """自愈：重拉服务器进程 + 重新握手"""
        try:
            self.close()
        except Exception:
            pass
        self.start()
        self.initialize()
    # 2. 协议收发 
    def _send(self,message):
        try:
            self.process.stdin.write(json.dumps(message,ensure_ascii=False)+"\n")
            self.process.stdin.flush()
        except(BrokenPipeError,OSError) as err:
            raise MCPConnectionError(f"管道已断{err}")from err
            #管道在读端写段都关闭后，会自动回收，子进程一端被close，kill，管道依然正常，依然可以写入（管道正常写入，但子进程无法接收不会报错）
    def _recv(self):
        while True:
            line = self.process.stdout.readline()
            if not line:
                raise MCPConnectionError("服务器已退出（stdout）达到eof")
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