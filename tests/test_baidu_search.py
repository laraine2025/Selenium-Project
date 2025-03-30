import time
import pytest
from pages.baidu_page import BaiduPage
from pages.search_result_page import SearchResultPage


def test_baidu_search_without_login(driver):
    """Test Baidu search without login"""
    # 创建百度页面对象
    baidu_page = BaiduPage(driver)
    
    # 打开百度首页并执行搜索
    baidu_page.open().search("Selenium Grid测试")
    
    # 创建搜索结果页面对象
    search_result_page = SearchResultPage(driver)
    
    # 验证搜索结果页面标题包含搜索关键词
    assert "Selenium Grid测试" in search_result_page.get_title()
    
    # 截图保存
    search_result_page.take_screenshot("baidu_search_result.png")


def test_baidu_search_with_login(driver, cookies):
    """Test Baidu search with login"""
    # 检查是否有有效的cookie
    valid_cookies = [cookie for cookie in cookies if cookie.get('name') and cookie.get('value')]
    
    if not valid_cookies:
        pytest.skip("没有有效的登录cookie，跳过登录测试")
    
    # 创建百度页面对象
    baidu_page = BaiduPage(driver)
    
    # 打开百度首页
    baidu_page.open()
    
    # 添加cookie实现登录
    baidu_page.add_cookies(cookies)
    
    # 执行搜索
    baidu_page.search("Selenium Grid登录测试")
    
    # 创建搜索结果页面对象
    search_result_page = SearchResultPage(driver)
    
    # 验证搜索结果页面标题包含搜索关键词
    assert "Selenium Grid登录测试" in search_result_page.get_title()
    
    # 截图保存
    search_result_page.take_screenshot("baidu_search_login_result.png")