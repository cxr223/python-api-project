# 1.fixture 注入
# 测试函数参数写 douban_session，自动使用公共请求头，不用重复写 headers。
# 2.单参数参数化
# 测 tag：覆盖不同业务场景
# 测 limit：覆盖边界值（最小、正常、最大）
# 3.多参数组合参数化 ⭐ 进阶
# 叠加两个 @pytest.mark.parametrize，自动生成笛卡尔积组合，全面覆盖测试场景。
# 断言规范
# 断言状态码 200
# 断言返回数据结构
# 断言业务规则（返回数量 ≤ limit）
import pytest
import requests


# 从conftest.py中导入douban_session fixture（前提是你已经定义了）
def test_douban_different_tags(douban_session):
    tags = ["热门", "最新", "经典", "喜剧", "爱情"]
    for tag in tags:
        params = {"type": "movie", "tag": tag, "page_limit": 5}
        resp = douban_session.get("https://movie.douban.com/j/search_subjects", params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert "subjects" in data
        # 可选：检查返回的电影列表不为空（有些tag可能为空，可以只断言结构存在）
        print(f"Tag {tag} 返回 {len(data['subjects'])} 部电影")


# ==============================================
# 用例 1：参数化测试 不同电影标签（tag）
# ==============================================
# 使用参数化方式更规范
@pytest.mark.parametrize("tag", ["hot", "new", "classic", "comedy", "love"])
def test_douban_tag_param(tag, douban_session):
    params = {"type": "movie", "tag": tag, "page_limit": 5}
    resp = douban_session.get("https://movie.douban.com/j/search_subjects", params=params)
    assert resp.status_code == 200
    assert isinstance(resp.json().get("subjects"), list)


# ==============================================
# 用例 2：参数化测试 不同分页数量（page_limit）边界值
# ==============================================
@pytest.mark.parametrize("limit", [1, 5, 10, 20])
def test_douban_page_limit(limit, douban_session):
    params = {"type": "movie", "tag": "热门", "page_limit": limit}
    resp = douban_session.get("https://movie.douban.com/j/search_subjects", params=params)
    data = resp.json()
    # 注意：豆瓣接口实际返回数量可能小于等于limit
    assert len(data.get("subjects", [])) <= limit


# ==============================================
# 用例 3：多参数组合参数化（tag + limit）
# ==============================================
@pytest.mark.parametrize("tag", ["hot", "classic", "comedy"])
@pytest.mark.parametrize("limit", [1, 10, 20])
def test_douban_tag_limit_combine(tag, limit, douban_session):
    params = {
        "type": "movie",
        "tag": tag,
        "page_limit": limit
    }

    resp = douban_session.get(
        "https://movie.douban.com/j/search_subjects",
        params=params
    )
    data = resp.json()

    # 双重验证
    assert resp.status_code == 200
    assert len(data.get("subjects", [])) <= limit
