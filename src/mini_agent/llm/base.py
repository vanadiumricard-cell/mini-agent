class BaseLLM:
    def chat(self, message: list[dict],tools:list[dict]|None=None) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
class demollm(BaseLLM):
    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        last_message = messages[-1]["content"]
        return {
            "role": "assistant",
            "content": f"demollm response to: {last_message}",
        }