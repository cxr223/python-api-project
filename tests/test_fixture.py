import requests
# common_headers = 只是一个字典（头文件）
# 你每次发请求，都必须手动写 headers=common_headers。
# douban_session = 自带头文件的 “请求工具”
# 它已经把 headers 装进去了，你直接用它发请求，永远不用写 headers！
# 以后所有接口测试，都只用 douban_session，不要再用 common_headers！
# 因为：
# 代码更短
# 更不容易写错
# 能自动保持登录
# 这是行业通用最佳实践


# 用例1：使用 公共Session fixture   更实用的 fixture（推荐）
def test_douban_with_fixture(douban_session):
    """
    测试豆瓣接口：直接使用自带请求头的session
    :param douban_session:
    :return:None
    """
    # 参数名对应conftest中的fixture函数名
    url = "https://movie.douban.com/j/search_subjects"
    params = {"type": "movie", "tag": "热门", "page_limit": 5}
    # 直接调用get，无需写headers！
    resp = douban_session.get(url, params=params)
    # 断言：接口响应成功 + 返回电影数据
    assert resp.status_code == 200
    assert "subjects" in resp.json()


# 用例2：使用 公共请求头 fixture   最简单的 fixture
def test_common_headers_usage(common_headers):
    """
    测试公共请求头：直接传入使用
    :param common_headers:
    :return: None
    """
    # 你可以直接使用common_headers这个字典
    resp = requests.get("https://httpbin.org/headers", headers=common_headers)
    assert resp.status_code == 200
