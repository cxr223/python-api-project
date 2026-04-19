# import requests
#
# params = {
#     "name": "test",
#     "age": 20,
#     "city": "南昌"
# }
# response = requests.get("https://httpbin.org/get", params=params)
# print("状态码:", response.status_code)
# print("url:", response.url)
# print("返回数据:", response.json())

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get("https://httpbin.org/headers", headers=headers)

print("服务器收到的请求头:", response.json()["headers"]["User-Agent"][:50] + "...")