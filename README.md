# API自动化测试学习项目

## 项目简介
本项目用于学习接口自动化测试，基于Python + pytest + requests。

## 测试覆盖
- 豆瓣电影搜索API（不同标签、不同分页）
- Open-Meteo天气API（多个城市）

## 如何运行
1. 安装依赖：`pip install requests pytest`
2. 运行所有测试：`pytest tests/ -v`
3. 生成HTML报告：`pytest tests/ --html=report.html`

## 项目结构
- tests/ : 所有测试文件和conftest.py
- week1_demo.py : 第一周练习脚本
- report.html # pytest HTML 自动化测试报告（42 用例全量通过）
- .gitignore # Git 文件忽略配置
- LICENSE # 开源协议