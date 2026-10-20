import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
server_path = ROOT / "mcp_servers" / "calculator_server.py"

process = subprocess.Popen(
    [sys.executable, str(server_path)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    encoding="utf-8",
)
def send_and_recv(message):
    line = json.dumps(message, ensure_ascii=False)
    print("→", line)
    process.stdin.write(line + "\n")
    process.stdin.flush()
    response = json.loads(process.stdout.readline())
    print("←", json.dumps(response, ensure_ascii=False)[:120])
    return response
def send_only(message):
    """通知：发完不读（没有人会回话）"""
    process.stdin.write(json.dumps(message) + "\n")
    process.stdin.flush()
# ── 1. 握手 ──
resp = send_and_recv({
    "jsonrpc": "2.0", "id": 1, "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "test-client", "version": "0.1"},
    },
})
assert resp["result"]["serverInfo"]["name"] == "mini-agent-calculator"
assert "tools" in resp["result"]["capabilities"]
print()
# ── 2. 握手完成通知（发完不读；如果服务器错误地回话，下面的断言会崩）──
send_only({"jsonrpc": "2.0", "method": "notifications/initialized"})
# ── 3. 工具发现 ──
resp = send_and_recv({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
tools = resp["result"]["tools"]
print("发现工具:", json.dumps(tools, ensure_ascii=False, indent=2))
assert tools[0]["name"] == "calculator"
assert "inputSchema" in tools[0]
print()
# ── 4. 工具调用：正常 ──
resp = send_and_recv({
    "jsonrpc": "2.0", "id": 3, "method": "tools/call",
    "params": {"name": "calculator",
               "arguments": {"a": 123, "b": 456, "operation": "multiply"}},
})
assert resp["result"]["content"][0]["text"] == "56088"
print()
# ── 5. 工具调用：业务错误（除零）──
resp = send_and_recv({
    "jsonrpc": "2.0", "id": 4, "method": "tools/call",
    "params": {"name": "calculator",
               "arguments": {"a": 5, "b": 0, "operation": "divide"}},
})
assert resp["result"]["isError"] is True
assert "除数不能为零" in resp["result"]["content"][0]["text"]
print()

# ── 6. 工具调用：协议错误（未知工具）──
resp = send_and_recv({
    "jsonrpc": "2.0", "id": 5, "method": "tools/call",
    "params": {"name": "weather", "arguments": {}},
})
assert resp["error"]["code"] == -32602
print()

# ── 收尾 ──
process.stdin.close()
print("服务器退出码:", process.wait(timeout=5))
print("✓ MCP 最小服务器全部场景通过")
