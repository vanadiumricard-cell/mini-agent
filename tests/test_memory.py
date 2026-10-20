from mock_llm import MockLLM

from mini_agent.context import (
    build_context,
    estimate_messages_tokens,
    estimate_tokens,
    summarize_history,
)
from mini_agent.memory import MemoryManager


def test_estimate_tokens_cjk_heavier_than_ascii():
    assert estimate_tokens("你好世界") > estimate_tokens("hello world")


def test_build_context_keeps_system_and_user_boundary():
    messages = [{"role": "system", "content": "你是 MiniAgent。"}]
    for i in range(1, 21):
        messages.append({"role": "user", "content": f"问题 {i} " + "内容" * 100})
        messages.append({"role": "assistant", "content": f"回答 {i} " + "回答" * 100})

    view = build_context(messages, max_tokens=2000)
    assert view[0]["role"] == "system"
    assert view[1]["role"] == "user"
    assert len(view) < len(messages)
    # 照妖镜：窗口必须"装满预算"（roles bug 的墓碑）
    assert estimate_messages_tokens(view) > 2000 * 0.7


def test_build_context_tool_protocol_safety():
    history = [
        {"role": "system", "content": "你是 MiniAgent。"},
        {"role": "user", "content": "旧问题" + "长" * 300},
        {"role": "assistant", "content": None,
         "tool_calls": [{"id": "c1", "type": "function",
                         "function": {"name": "calculator", "arguments": "{}"}}]},
        {"role": "tool", "tool_call_id": "c1", "content": "旧结果" + "长" * 300},
        {"role": "assistant", "content": "旧回答"},
        {"role": "user", "content": "新问题"},
        {"role": "assistant", "content": None,
         "tool_calls": [{"id": "c2", "type": "function",
                         "function": {"name": "calculator", "arguments": "{}"}}]},
        {"role": "tool", "tool_call_id": "c2", "content": "新结果"},
    ]
    view = build_context(history, max_tokens=200)
    assert view[1]["content"] == "新问题"


def test_summarize_history_with_mock():
    fake = [{"role": "system", "content": "你是 MiniAgent。"}]
    fake.append({"role": "user", "content": "我叫小明。"})
    fake.append({"role": "assistant", "content": "记住了。"})
    for i in range(10):
        fake.append({"role": "user", "content": f"闲聊 {i}：" + "内容" * 100})
        fake.append({"role": "assistant", "content": f"回应 {i}：" + "回应" * 100})

    mock = MockLLM([{"role": "assistant", "content": "【模拟摘要】"}])
    assert summarize_history(fake, mock, max_tokens=2000) is True
    assert fake[1]["role"] == "system"
    assert "【早期对话摘要】" in fake[1]["content"]
    assert "模拟摘要" in fake[1]["content"]


def test_summarize_history_noop_when_small():
    messages = [{"role": "system", "content": "hi"}, {"role": "user", "content": "hello"}]
    mock = MockLLM([])
    assert summarize_history(messages, mock, max_tokens=100000) is False
    assert len(messages) == 2


def test_memory_manager_compress_once():
    mock = MockLLM([{"role": "assistant", "content": "摘要内容"}])
    memory = MemoryManager(mock, max_tokens=2000)
    memory.add({"role": "system", "content": "你是 MiniAgent。"})
    memory.add({"role": "user", "content": "我叫小明。"})
    memory.add({"role": "assistant", "content": "记住了。"})
    for i in range(10):
        memory.add({"role": "user", "content": f"闲聊 {i}：" + "内容" * 100})
        memory.add({"role": "assistant", "content": f"回应 {i}：" + "回应" * 100})

    assert memory.compress() is True
    assert memory.compress_count == 1
    assert memory.compress() is False        # 已低于预算，不会重复压缩
    assert memory.compress_count == 1
    assert "context" in memory.stats()