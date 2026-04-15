# 基础的 GET 请求示例
import requests

params = {
    "name": "test",
    "age": 20,
    "city": "南昌"
}
response = requests.get("https://httpbin.org/get", params=params)
print("状态码:", response.status_code)
print("url:", response.url)
print("返回数据:", response.json())
# -------------------------------------------


# 豆瓣 API 调用示例
# 调用豆瓣搜索 API   它是一个爬取豆瓣热门电影的小爬虫
# 这是今天的核心任务。豆瓣有一个公开的搜索接口，不需要 key 就能调用：
# 这段代码伪装成浏览器，访问豆瓣电影接口，获取 5 部热门电影，然后打印出前 3 部的名字和评分。
import requests

# 这是豆瓣电影的接口地址
# 不是普通网页，是专门返回电影数据的接口
# 直接访问会返回 JSON 格式的电影信息
url = "https://movie.douban.com/j/search_subjects"

# 请求参数，告诉豆瓣要什么数据：
# type要电影不是电视剧
# tag: "热门" → 要热门标签
# page_limit: 5 → 一次返回 5 部电影
params = {
    "type": "movie",
    "tag": "热门",
    "page_limit": 5
}

# 请求头，非常重要
# 豆瓣会检查：你是不是浏览器？
# 这里伪装成Chrome谷歌 浏览器访问，否则会被拒绝
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

response = requests.get(url, params=params, headers=headers, timeout=10)

print("状态码:", response.status_code)
if response.status_code == 200:
    data = response.json()
    # data.get("subjects", []) → 拿到电影列表
    # len(...) → 计算一共几部
    print("共返回", len(data.get("subjects", [])), "部电影")
    # 循环遍历前 3 部电影
    # 打印：电影名 movie['title']   评分 movie['rate']
    for movie in data.get("subjects", [])[:3]:
        print(f"  电影: {movie['title']}, 评分: {movie['rate']}")

# --------------------------------------------------


# POST 请求示例
import requests

url = "https://httpbin.org/post"

# 方式1：发送 JSON 数据（推荐，接口测试最常用）
data_json = {
    "username": "cxr",
    "password": "123456"
}
response = requests.post(url, json = data_json)

print("状态码", response.status_code)
print("服务器收到的JSON数据：", response.json()["json"])

# 方式2：发送表单数据
data_form = {
    "username": "testuser",
    "password": "123456"
}
response2 = requests.post(url, data=data_form)
print("表单方式:", response2.json()["form"])
# ------------------------------------
# session 示例
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
# ---------------------------------------

# 天气查询函数
import requests


def get_weather(city_lat, city_lon):
    """
    根据经纬度获取当前天气
    使用Open-Meteo 免费天气API 无需key
    :param city_lat: 纬度
    :param city_lon: 经度
    :return:温度、风速、天气代码、是否成功。
    """
    # 这是免费天气服务器的地址
    url = "https://api.open-meteo.com/v1/forecast"
    # 参数（告诉 API 要查哪里）
    params = {
        "latitude": city_lat,
        "longitude": city_lon,
        "current_weather": "true"
    }
    # 请求头（伪装身份）
    headers = {
        "User_Agent": "MyWeatherApp/1.0"
    }
    # try 防报错（超级重要）
    # 下面代码可能出错，先试试，错了不崩
    try:
        # 发送请求，设置 10 秒超时，10秒没回应就算了。
        response = requests.get(url, params=params, headers=headers, timeout=10)
        # 检查是否成功，不是 200 就直接报错
        response.raise_for_status()
        # 服务器返回的文字 → 变成 Python 能看懂的字典
        data = response.json()
        # 拿出当前天气
        weather = data["current_weather"]

        # 返回：温度、风速、天气代码、是否成功。
        return {
                "temperature": weather["temperature"],
                "windspeed": weather["windspeed"],
                "weathercode": weather["weathercode"],
                "success": True
        }
    # 如果报错了，错了就告诉用户：失败 + 原因。
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return {"success": False, "error": str(e)}


# 测试几个城市
cities = {
    "北京": (39.9042, 116.4074),
    "上海": (31.2304, 121.4737),
    "广州": (23.1291, 113.2644)
}

for city_name, (lat, lon) in cities.items():
    result = get_weather(lat, lon)
    if result["success"]:
        print(f"{city_name} 当前温度: {result['temperature']}°C, 风速: {result['windspeed']} km/h")
    else:
        print(f"{city_name} 查询失败: {result['error']}")

