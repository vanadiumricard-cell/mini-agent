from mini_agent.context import (
    estimate_tokens,
    estimate_messages_tokens,
    context_report,
)
from mini_agent.llm.client import DeepSeekLLM
from mini_agent.tools import ReadFileTool

# ── 1. 感受 token 密度 ──
print("你好世界 →", estimate_tokens("你好，世界"), "token")
print("Hello world →", estimate_tokens("Hello world"), "token")
cn = "这是一句用于测试的中文句子，大约三十个字符，用来对比中英文的 token 密度差异。"
en = "This is an English sentence of a similar length for the comparison."
print(f"中文 {len(cn)} 字 → 约 {estimate_tokens(cn)} token")
print(f"英文 {len(en)} 字符 → 约 {estimate_tokens(en)} token")
print()

llm = DeepSeekLLM()
messages = [{"role": "user", "content": cn}]
message = llm.chat(messages)
real = llm.last_usage["prompt_tokens"]
est = estimate_messages_tokens(messages)
print("真实 usage:", llm.last_usage)
print(f"真实 prompt_tokens = {real} | 我们估算 = {est} | 真实/估算 = {real / est:.2f}")
print()
tool = ReadFileTool()
content = tool.run("sandbox/big.txt")      # w3d6 生成的 200 行文件
plain = [{"role": "user", "content": "你好"}]
with_file = plain + [{"role": "tool", "tool_call_id": "call_x", "content": content}]
print("普通问候:", context_report(plain))
print("加一条 200 行文件结果:", context_report(with_file))
