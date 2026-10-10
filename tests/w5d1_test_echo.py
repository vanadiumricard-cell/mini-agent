import json
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
print(ROOT)
server_path = ROOT / "mcp_servers" / "echo_server.py"
process = subprocess.Popen(
    [sys.executable, str(server_path)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
    encoding="utf-8",
)
print(process.pid)
print(str(subprocess.PIPE))
print(process.stdin,"----",process.stdout)
def send(message):
    line=json.dumps(message,ensure_ascii=False)
    print("→ 发送:", line)
    process.stdin.write(line+"\n")
    process.stdin.flush()
    responose=json.loads(process.stdout.readline())
    return responose
response = send({"jsonrpc": "2.0", "id": 1, "method": "ping", "params": {}})
assert response["result"]["pong"] is True 
response = send({"jsonrpc": "2.0", "id": 2, "method": "foo", "params": {}})
assert "error" in response
print()
process.stdin.close()
print("服务器退出码:", process.wait(timeout=5))
print("✓ 跨进程通信打通") 
    