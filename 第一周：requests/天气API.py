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

