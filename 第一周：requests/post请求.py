import requests

url = "https://httpbin.org/post"

# 方式1：发送 JSON 数据（推荐，接口测试最常用）
data_json = {
    "username": "cxr",
    "password": "123456"
}
response = requests.post(url, json=data_json)

print("状态码", response.status_code)
print("服务器收到的JSON数据：", response.json()["json"])

# 方式2：发送表单数据
data_form = {
    "username": "testuser",
    "password": "123456"
}
response2 = requests.post(url, data=data_form)
print("表单方式:", response2.json()["form"])
