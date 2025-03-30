import json
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime


def load_cookies():
    """Load cookie configuration file"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('cookies', [])
    except (FileNotFoundError, json.JSONDecodeError):
        return []


@pytest.fixture(scope="session")
def grid_url():
    """Return Selenium Grid Hub URL"""
    return "http://localhost:4444"


@pytest.fixture(params=['chrome', 'edge', 'firefox'])
def driver(request, grid_url):
    """Create WebDriver instance with multi-browser support"""
    browser_name = request.param
    
    if browser_name == 'chrome':
        options = Options()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        capabilities = {'browserName': 'chrome'}
    elif browser_name == 'edge':
        options = EdgeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        capabilities = {'browserName': 'MicrosoftEdge'}
    elif browser_name == 'firefox':
        options = FirefoxOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        capabilities = {'browserName': 'firefox'}
    else:
        raise ValueError(f"不支持的浏览器类型: {browser_name}")
    
    driver = webdriver.Remote(
        command_executor=grid_url,
        options=options
    )
    
    driver.implicitly_wait(10)
    
    # 返回driver实例
    yield driver
    
    # 测试结束后关闭浏览器
    driver.quit()


@pytest.fixture
def cookies():
    """返回cookie配置"""
    return load_cookies()


# 配置HTML报告
def pytest_configure(config):
    """配置pytest-html报告"""
    # 创建报告目录
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # 设置报告文件名（包含时间戳）
    report_file = os.path.join('reports', f'test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
    
    # 配置HTML报告
    config.option.htmlpath = report_file
    config.option.self_contained_html = True


# 添加截图到HTML报告
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        try:
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
                screenshot_dir = "reports/screenshots"
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                
                screenshot_path = os.path.join(screenshot_dir, f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                driver.save_screenshot(screenshot_path)
                
                # 修改这里，使用pytest_html.extras
                if hasattr(report, "extras"):
                    report.extras.append(pytest_html.extras.image(screenshot_path))
                else:
                    report.extras = [pytest_html.extras.image(screenshot_path)]
        except Exception as e:
            print(f"截图失败: {e}")