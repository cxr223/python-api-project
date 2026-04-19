# 用 requests.Session() 之后，你不需要手动处理 cookie，session 对象会自动帮你管理。
# 后续你做接口自动化测试时，会用 session 来模拟用户登录后的行为。
import requests

# 创建一个 session 对象（就像一个虚拟浏览器）
session = requests.Session()

# 先用 GET 访问一个设置 cookie 的接口
session.get("https://httpbin.org/cookies/set?name=testuser&session_id=abc123")

# 然后 GET 获取当前 cookie，看是否被自动携带了
response = session.get("https://httpbin.org/cookies")
print("Session自动携带的cookie:", response.json()["cookies"])

# 用同一个 session 先登录（假设），再访问需要登录的接口
session2 = requests.Session()
# 模拟登录（发送登录信息）
session2.post("https://httpbin.org/post", json={"username": "test"})
# 之后用同一个 session 访问任何接口，都会自动携带登录后的 cookie
response2 = session2.get("https://httpbin.org/cookies")
print(response2.json())