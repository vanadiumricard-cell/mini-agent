import sys
import time

from mini_agent.llm.client import DeepSeekLLM

llm = DeepSeekLLM()

# ── 1. 网络故障演练：指向一个不存在的服务 → 自动重试后失败 ──
original_url = llm.url
llm.url = "http://127.0.0.1:9/unreachable"      # 9 号端口：必然连不上
print("=== 1. 断网演练 ===")
start = time.time()
try:
    llm.chat([{"role": "user", "content": "hi"}])
    print("没有报错，异常！")
except Exception as err:
    elapsed = time.time() - start
    print(f"最终失败：{type(err).__name__}，耗时 {elapsed:.1f}s（含 1s + 2s 两次退避）")
    assert elapsed >= 2.5
llm.url = original_url
print()

# ── 2. 恢复后一切正常 ──
print("=== 2. 恢复后正常调用 ===")
message = llm.chat([{"role": "user", "content": "只回复两个字：收到"}])
print("回答:", message["content"])
assert message["content"]
print()

# ── 3. 流式回归 ──
print("=== 3. 流式回归 ===")
def show(piece):
    sys.stdout.write(piece)
    sys.stdout.flush()


streamed = llm.chat([{"role": "user", "content": "只回复两个字：好的"}], on_token=show)
print()
assert streamed["content"]
print("✓ 韧性验证通过")