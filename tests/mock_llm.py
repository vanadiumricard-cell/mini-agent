from mini_agent.llm.base import BaseLLM
class MockLLM(BaseLLM):
    def __init__(self,responses):
        self.responses=responses
        self.call_count=0
    def chat(self,messages,tools=None):
        response=self.responses[self.call_count]
        self.call_count+=1
        return response