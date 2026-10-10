import json
import sys
sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")
def handle(message):
    if "id" not in message:
        return None
    if message.get("method")=="ping":
        return{"jsonrpc":"2.0","id":message["id"],"result":{"pong":True}}
    return{"jsonrpc":"2.0",
           "id":message["id"],
           "error":{"code":-32601,"message":f"未知方法：{message.get('method')}"}}
def main():
    for line in sys.stdin:
        line=line.strip()
        if not line:
            continue
        message=json.loads(line)
        response=handle(message)
        if response is not None:
            print(json.dumps(response,ensure_ascii=False),flush=True)
if __name__ == "__main__":
    main() 