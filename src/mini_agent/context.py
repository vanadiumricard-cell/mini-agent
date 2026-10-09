CONTEXT_LIMIT = 1000000
MAX_CONTEXT_TOKENS=int(CONTEXT_LIMIT*0.75)
def estimate_tokens(text:str)->int:
    if not text:
        return 0
    cjk=0
    for ch in text:
        if"\u4e00"<=ch<="\u9fff":
            cjk+=1
    other=len(text)-cjk
    
    return max(1,int(cjk*1.2+other/3))
def estimate_messages_tokens(messages:list[dict])->int:
    return sum(estimate_tokens(str(m))for m in messages)
def context_report(messages:list[dict])->str:
    used=estimate_messages_tokens(messages)
    percent=used*100/CONTEXT_LIMIT
    return f"context ≈ {used} / {CONTEXT_LIMIT} token（{percent:.1f}%）"
"""从完整历史构建本次发送给模型的视图：
    1. system 消息永远保留
    2. 从最新消息往前装，装到预算为止
    3. 窗口起点必须是 user 消息（保证 tool 调用协议完整）"""
def build_context(messages:list[dict],max_tokens:int=MAX_CONTEXT_TOKENS)->list[dict]:
    system=[]
    rest=list(messages)
    while rest and rest[0].get("role")=="system":
        system.append(rest[0])
        rest=rest[1:]
    if not rest:
        return system
    kept=[]
    used=estimate_messages_tokens(system)
    for message in reversed(rest):
        cost=estimate_tokens(str(message))
        if kept and used+cost>max_tokens:
            break
        kept.append(message)
        used+=cost
    kept.reverse()
    # 把窗口起点推到最近的 user 消息（协议安全）
    while kept and kept[0].get("role")!="user":
        kept.pop(0)
    # 兜底：预算太小导致窗口为空时，保住最后一轮 user 起始的片段
    if not kept:
        for i in range(len(rest)-1,-1,-1):
            if rest[i].get("role")=="user":
                kept=rest[i:]
                break
    return system+kept
SUMMARY_PROMPT = (
    "请把下面这段早期对话压缩成简洁的摘要。保留：用户的关键信息与偏好、"
    "已完成的任务与结论、未完成的事项。用要点列出，不要编造。\n\n"
)
def summarize_history(messages:list[dict],llm,max_tokens:int=MAX_CONTEXT_TOKENS)->bool:
    """历史超过预算时，把最老的一段让 LLM 压缩成摘要消息。
    返回 True 表示执行了压缩。"""
    if estimate_messages_tokens(messages)<=max_tokens:
        return False
    keep_budget=max_tokens//2
    #整数除法，向下取整
    cut=len(messages)
    #cut是计算压缩范围，下标比cut小的（前面的）压缩，初始取最大值，逐渐减少
    used=0
    for i in range(len(messages)-1,-1,-1):
        cost=estimate_tokens(str(messages[i]))
        if used+cost>keep_budget and cut<len(messages):
            break
          # cut<len(messages)是为了防止第一条消息就超预算，至少保留一条消息再压缩
        used+=cost
        cut=i
        #缩小cut
    while cut<len(messages)and messages[cut].get("role")!="user":
        cut+=1
        # cut<len(messages)防止一直找不到role=user死循环
    if cut>=len(messages):
        return False
    #找不到协议安全，放弃压缩
    prefix_start=1 if messages and messages[0].get("role")=="system" else 0
    old=messages[prefix_start:cut]
    if not old:
        return False
    old_text="\n".join(f"{m.get('role')}:{m.get('content')}"for m in old)
    summary=llm.chat([{"role":"user","content":SUMMARY_PROMPT+old_text}])["content"]
    summary_message={"role":"system","content":f"【早期对话摘要】\n{summary}"}
    messages[:]=messages[:prefix_start]+[summary_message]+messages[cut:]
    return True

      
          

