
from mini_agent.context import (
    MAX_CONTEXT_TOKENS,
    build_context,
    context_report,
    estimate_messages_tokens,
    summarize_history,
)
class MemoryManager:
    """记忆管家：持有完整历史，负责视图构建与压缩。

    - messages：完整存储（永不丢失）
    - context()：本次发送给模型的视图（system 永驻 + 最近内容）
    - compress()：超过预算时把老历史压缩成摘要
    - stats()：油表（视图 / 存储 / 压缩次数）
    """
    def __init__(self,llm,max_tokens=MAX_CONTEXT_TOKENS):
        self.llm=llm
        self.max_tokens=max_tokens
        self.messages=[]
        self.compress_count=0
    def add(self,message):
        self.messages.append(message)
    def context(self):
        return build_context(self.messages,max_tokens=self.max_tokens)
    def compress(self):
        if summarize_history(self.messages,self.llm,max_tokens=self.max_tokens):
            self.compress_count+=1
            return True
        return False
    def stats(self):
        view = context_report(self.context())
        stored = estimate_messages_tokens(self.messages)
        return f"{view} | 存储 {stored} token | 压缩 {self.compress_count} 次" 

