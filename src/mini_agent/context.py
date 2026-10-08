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
    if rest and rest[0].get("role")=="system":
        system.append(rest[0])
        rest=rest[1:]
    if not rest:
        return system
    kept=[]
    used=estimate_messages_tokens(system)
    for message in reversed(rest):
        cost=estimate_messages_tokens(str(message))
        if kept and used+cost>max_tokens:
            break
        kept.append(message)
        used+=cost
    kept.reverse()
    # 把窗口起点推到最近的 user 消息（协议安全）
    while kept and kept[0].get("roles")!="user":
        kept.pop(0)
    # 兜底：预算太小导致窗口为空时，保住最后一轮 user 起始的片段
    if not kept:
        for i in range(len(rest)-1,-1,-1):
            if rest[i].get("role")=="user":
                kept=rest[i:]
                break
    return system+kept

