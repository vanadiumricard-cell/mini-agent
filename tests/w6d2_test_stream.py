import sys
import time

from mini_agent.llm.client import DeepSeekLLM

llm = DeepSeekLLM()
messages = [{"role": "user", "content": "用三句话介绍一下什么是流式输出"}]

print("=== 流式输出（看字一个一个蹦）===")
first_at = [None]
start = time.time()


def on_token(piece):
    if first_at[0] is None:
        first_at[0] = time.time() - start
    sys.stdout.write(piece)
    sys.stdout.flush()


streamed = llm.chat(messages, on_token=on_token)
total = time.time() - start
print()
print("=== 结束 ===")
print(f"首字延迟: {first_at[0]:.2f}s | 总时长: {total:.2f}s")
print("累计内容长度:", len(streamed["content"]))
assert streamed["content"]
print()

print("=== 对照：非流式（等全部生成完才一次性吐出）===")
start2 = time.time()
message = llm.chat(messages)
total2 = time.time() - start2
print("内容:", message["content"])
print(f"总时长: {total2:.2f}s —— 用户在 {total2:.2f}s 内什么都看不到")
print()

print(f"结论：首字延迟 {first_at[0]:.2f}s（流式） vs {total2:.2f}s（非流式=总时长）")