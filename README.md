<<<<<<< HEAD
# Selenium Grid Automation Test Project

## Project Overview
本项目基于 Python + pytest + Selenium Grid 实现跨浏览器自动化测试，主要功能包括：
- 多浏览器并行测试（Chrome/Edge/Firefox）
- 自动化测试报告生成（含失败截图）
- Docker 容器化部署测试环境
- 可配置的Cookie管理

## Technology Stack
- **测试框架**: pytest
- **浏览器自动化**: Selenium 4
- **报告系统**: pytest-html
- **环境管理**: Docker + docker-compose
- **配置管理**: JSON 配置文件

## 项目结构
```
├── tests/              # 测试用例目录
├── pages/              # 页面对象模型
├── reports/            # 测试报告和截图
│   ├── screenshots/
│   └── *.html
├── config.json         # 配置文件
├── conftest.py         # pytest全局配置
└── docker-compose.yml  # Grid容器配置
```

## Test Execution Workflow
1. **启动Selenium Grid**
   ```bash
   docker-compose up -d
   ```
2. **加载配置**
   - 读取config.json中的cookie配置
   - 初始化浏览器能力配置
3. **参数化浏览器驱动**
   - 自动创建Chrome/Edge/Firefox驱动实例
   - 浏览器最大化窗口并设置隐式等待
4. **执行测试用例**
   ```bash
   pytest tests/ -v
   ```
5. **生成测试报告**
   - 自动生成带时间戳的HTML报告
   - 失败用例自动保存浏览器截图
   - 报告路径：reports/test_report_*.html

## Environment Setup
```bash
# 安装依赖
pip install -r requirements.txt

# 启动虚拟环境（Windows）
python -m venv venv
venv\Scripts\activate
```

## Important Notes
- 确保Docker服务已启动
- 浏览器驱动版本需与本地浏览器兼容
- 测试报告路径在conftest.py中自动创建
- 失败截图保存路径：reports/screenshots/
- 运行测试前请确保Grid节点已注册到Hub
=======