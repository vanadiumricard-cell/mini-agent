class BaseLLM:
    def chat(self, message: str) -> str:
        raise NotImplementedError("This method should be implemented by subclasses.")
class demollm(BaseLLM):
    def chat(self,message:str) -> str:
       return f"demollm response to: {message}"
