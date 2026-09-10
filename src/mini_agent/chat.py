from mini_agent.llm.client import DeepSeekLLM
def main():
    llm=DeepSeekLLM()
    messages=[]
    print("agent已启动")
    print("输入exit退出")
    while True:
        user_input=input("\n用户: ")
        if user_input=="exit":
            print("agent已退出")
            break
        messages.append({"role":"user","content":user_input})
        response=llm.chat(messages)
        print(f"agent: {response}")
        messages.append({"role":"assistant","content":response})

if __name__ == "__main__":
     main()