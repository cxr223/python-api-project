import pytest
import requests


# fixture 1：公共请求头（所有接口都用这个Header）

@pytest.fixture
def common_headers():
    """
    公共请求头fixture
    作用：返回固定的User-Agent，避免每个用例重复写
    :return:User-Agent
    """
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


# fixture 2：公共Session（带默认请求头，更高级）
@pytest.fixture
def douban_session():
    """
    公共会话Session
    作用：创建一个自带请求头的requests会话，全局复用
    优势：自动保持cookie，请求更高效
    :return:session
    """
    # 创建requests会话对象
    session = requests.Session()
    # 给会话设置公共请求头（一次设置，所有请求自动携带）全局设置请求头
    session.headers.update({"User-Agent": "Mozilla/5.0"})
    # 返回会话对象，供测试用例使用
    return session
