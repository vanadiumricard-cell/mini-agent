import httpx
headers = {
    "authorization": "Bearer demo_api_key",
    "content-type": "application/json"
}
data = {
    "model": "demo_model",
    "messages": [
        {
            "roles": "user",
            "content": "你好"
        }
    ]
}
print("headers:", headers)
print("\ndata:", data)