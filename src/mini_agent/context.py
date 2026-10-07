CONTEXT_LIMIT = 1000000
def estimate_tokens(text:str)->int:
    if not text:
        return 0
    cjk=0
    for ch in text:
        if"\u4e00"<=ch<="\u9fff":
            cjk+=1
    other=len(text)-cjk
    
    return max(1,int(cjk+other/3))
def estimate_messages_tokens(messages:list[dict])->int:
    return sum(estimate_tokens(str(m))for m in messages)
def context_report(messages:list[dict])->str:
    used=estimate_messages_tokens(messages)
    percent=used*100/CONTEXT_LIMIT
    return f"context ≈ {used} / {CONTEXT_LIMIT} token（{percent:.1f}%）"