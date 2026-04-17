# 用到 pytest 专属语法（参数化 parametrize、夹具 fixture、标签 mark 等）→ 必须 import pytest
# 情况 1：不加 return
# 满足下面任意一个就不用写：
# 函数内部直接写完断言
# 数据只在函数自己内部用，别人不用
# 只是执行操作，不需要传出结果
# 情况 2：必须加 return
# 把功能封装成工具函数
# 里面的结果，别的函数要调用、要用
import pytest
import requests


def get_weather(lat, lon):
    """
    封装一个获取天气的函数（给测试调用）
    :param lat:纬度
    :param lon:经度
    :return:resp
    """
    # 免费天气API地址
    url = "https://api.open-meteo.com/v1/forecast"
    # 请求参数：纬度、经度、获取当前天气
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    # 发送请求，10秒超时
    resp = requests.get(url, params=params, timeout=10)
    # 返回响应结果
    return resp


# 装饰器：让同一个测试函数，跑多组不同数据
# 使用参数化装饰器，传入多组(纬度,经度,城市名)
# 格式规则：
# 第一部分 "lat,lon,city"
# 定义你要传的参数名字
# 名字可以随便写，但必须和测试函数参数一致
# 第二部分 [ ... ]
# 里面是多组数据列表
# 每一组 (纬度, 经度, 城市名) 就是一条测试数据
# 有几组数据，pytest 就会跑几次测试
@pytest.mark.parametrize("lat,lon,city", [
    (39.9042, 116.4074, "beijing"),
    (31.2304, 121.4737, "shanghai"),
    (23.1291, 113.2644, "guangzhou"),
    (30.5728, 104.0668, "chendu"),   # 增加一个城市
])
# 测试函数：参数必须和上面装饰器里的名字一一对应
def test_weather_status_code(lat, lon, city):
    # 调用函数获取天气,= 左边的 resp，就是上面函数 return 回来的东西。
    resp = get_weather(lat, lon)
    # 断言：状态码必须是200
    assert resp.status_code == 200, f"{city} 天气接口返回非200"


# pytest 参数化进阶用法：多组数据测试（边界值 / 多场景）
# 这段代码是接口测试中最经典的边界值测试场景：
# 我们选的 [1,5,10,20,100] 不是随机数字，而是覆盖了所有关键边界：
# 最小值：1（极限最小分页）
# 常规值：5、10、20（用户常用值）
# 最大值 / 临界值：100（接口允许的最大分页）
# pytest参数化装饰器，给测试函数传入多组测试数据
@pytest.mark.parametrize("limit", [1, 5, 10, 20, 100])
def test_douban_page_limit(limit):
    """
    函数名必须以 test_ 开头（pytest 识别规则）
    入参 limit：接收参数化装饰器传入的数据
    测试豆瓣电影API的分页参数 page_limit
    验证：接口返回的电影数量 ≤ 传入的分页限制值（边界值测试）
    :param limit:
    :return:
    """
    # 1. 发送GET请求，调用豆瓣热门电影搜索接口
    resp = requests.get(
        url="https://movie.douban.com/j/search_subjects",  # 接口地址
        # 请求参数：type=电影，tag=热门，page_limit=参数化的分页数量
        params={
            "type": "movie",
            "tag": "热门",
            "page_limit": limit
        },
        # 请求头：必须携带User-Agent，否则豆瓣会拒绝请求,模拟浏览器请求，绕过豆瓣的反爬限制
        headers={"User-Agent": "Mozilla/5.0"}
    )
    # 2. 将接口返回的JSON字符串转换为Python字典
    data = resp.json()
    # 3. 核心断言：验证接口返回结果符合预期
    # data.get("subjects", [])：安全获取电影列表，无数据时返回空列表
    # len()：统计返回的电影数量
    # 断言：返回数量 永远不超过 请求的limit值（接口核心规则）
    assert len(data.get("subjects", [])) <= limit


# 进阶补充：同一个函数传入多个参数（多维度测试）
# 这是参数化的高阶用法：同时传多个参数（比如同时测试 城市+分页、用户名+密码）。
# 同时参数化 city 和 limit，笛卡尔积组合执行
# 执行次数：3个城市 × 3个分页 = 9次测试
# 自动覆盖所有组合，无需手动编写重复代码
@pytest.mark.parametrize("city", ["beijing", "shanghai", "guangzhou"])
@pytest.mark.parametrize("limit", [1, 10, 20])
def test_city_movie(city, limit):
    resp = requests.get(
        "https://movie.douban.com/j/search_subjects",
        params={"type": "movie", "tag": city, "page_limit": limit},
        headers={"User-Agent": "Mozilla/5.0"}
    )
    data = resp.json()
    assert len(data.get("subjects", [])) <= limit
