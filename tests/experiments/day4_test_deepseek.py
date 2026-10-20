import os
import httpx
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("DEEPSEEK_API_KEY")
url = "https://api.deepseek.com/chat/completions"
headers={
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data={
    "model": "deepseek-v4-flash",
    "messages": [
        {"role": "user",
         "content": "你好，用一句话介绍一下自己"
        }
    ],
    "stream": False
}
response=httpx.post(url, 
                    headers=headers, 
                    json=data,
                    timeout=30
                )

response_data=response.json()
answer=response_data["choices"][0]["message"]["content"]
print(answer)
