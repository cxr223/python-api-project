# resp.json() 是 requests 库自带的方法，作用：
# 把接口返回的字符串格式 JSON，自动转换成 Python 的字典
# 原始接口返回长这样（纯文本字符串）
# {"subjects": [{"title":"电影名","rate":"8.9"}], ...}
# 它只是一串文字，Python 没法直接取里面的 subjects、title、rate。
# 调用 resp.json() 之后
# Python 自动解析，变成：
# 外层：字典 dict
# 里面 subjects：列表 list
# 列表里面每个元素：又是字典
# 之后你才能用：
# 取列表
# data["subjects"]
# 取第一个电影
# data["subjects"][0]
# 取电影评分、标题
# data["subjects"][0]["rate"]
# data["subjects"][0]["title"]
# 去取值、做断言。

# 发请求 → 断言状态码 → .json () 解析数据 → 断言字段 / 类型 / 内容
import requests


def test_douban_status_code():
    """
    断言 状态码 == 200（接口请求成功）
    :return:
    """
    # 豆瓣电影搜索API地址
    url = "https://movie.douban.com/j/search_subjects"
    # 请求参数：找电影、热门、返回5条
    params = {"type": "movie", "tag": "热门", "page_limit": 5}
    # 请求头：模拟浏览器访问，否则会被拦截
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers)

    # 断言1：状态码是200
    assert resp.status_code == 200, "状态码不是200，接口请求失败"


def test_douban_has_subjects():
    """
    断言 字段存在 + 数据格式正确
    :return:
    """
    url = "https://movie.douban.com/j/search_subjects"
    params = {"type": "movie", "tag": "热门", "page_limit": 5}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers)
    # 把接口返回的字符串格式 JSON，自动转换成 Python 的字典
    data = resp.json()

    # 断言2：返回的JSON中包含'subjects'（电影列表）字段
    assert "subjects" in data, "返回结果中没有 subjects 字段"
    # 断言3：subjects是一个列表，且长度大于0
    assert isinstance(data["subjects"], list), "subjects 不是列表类型"
    assert len(data["subjects"]) > 0, "电影列表为空"


def test_douban_first_movie_title_not_empty():
    """
    断言 值范围 + 字段不为空
    :return:
    """
    url = "https://movie.douban.com/j/search_subjects"
    params = {"type": "movie", "tag": "热门", "page_limit": 5}
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers)
    data = resp.json()
    # 拿到第一条电影
    first_movie = data["subjects"][0]

    # 断言4：第一电影的标题不为空字符串
    assert first_movie["title"] != "", "电影标题为空"
    # 断言5：评分是数字（或者可以断言大于0）
    assert float(first_movie["rate"]) > 0, "电影评分异常"
