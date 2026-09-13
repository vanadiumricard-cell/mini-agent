class BaseLLM:
    def chat(self, message: list[dict],tools:list[dict]|None=None) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
class demollm(BaseLLM):
    def chat(self,message:list[dict],tools:list[dict]|None=None) -> str:
       return f"demollm response to: {message}"
