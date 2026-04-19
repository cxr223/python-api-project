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