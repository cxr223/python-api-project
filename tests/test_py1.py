def test_one():
    assert 1 + 1 == 2


def test_two():
    assert "hello".upper() == "HELLO"


# def test_3():
#     # 故意写一个会失败的断言，观察pytest输出
#     assert 2 * 3 == 7, "错了"
