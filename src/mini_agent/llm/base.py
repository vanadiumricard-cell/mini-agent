class BaseLLM:
    def chat(self, messages: list[dict],tools:list[dict]|None=None,on_token=None) -> dict:
        raise NotImplementedError("This method should be implemented by subclasses.")
class demollm(BaseLLM):
    def chat(self, messages: list[dict], tools: list[dict] | None = None, on_token=None) -> dict:
        content = f"demollm response to: {messages[-1]['content']}"
        if on_token is not None:
            on_token(content)          # 演示用：把整段当一片"流"出去
        return {"role": "assistant", "content": content}