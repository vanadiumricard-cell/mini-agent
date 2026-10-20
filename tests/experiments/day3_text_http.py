import httpx
data = {
    "title": "miniagent",
    "body":"learning http post",
    "userid": 1
        }
response=httpx.post("https://jsonplaceholder.typicode.com/posts", json=data)
print(response.status_code)
print(response.json())
