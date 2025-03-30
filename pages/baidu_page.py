from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaiduPage:
    """Baidu search page object class, encapsulates all elements and operations of Baidu page"""
    
    # 页面URL
    URL = "https://www.baidu.com"
    
    # 页面元素定位器
    SEARCH_BOX = (By.ID, "kw")
    SEARCH_BUTTON = (By.ID, "su")
    SEARCH_RESULTS = (By.ID, "content_left")
    
    def __init__(self, driver):
        """Initialize page object

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open(self):
        """打开百度首页"""
        self.driver.get(self.URL)
        return self
    
    def get_search_box(self):
        """获取搜索框元素"""
        return self.wait.until(EC.presence_of_element_located(self.SEARCH_BOX))
    
    def search(self, keyword):
        """执行搜索操作
        
        Args:
            keyword: 搜索关键词
        """
        search_box = self.get_search_box()
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        
        # 等待搜索结果加载
        self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULTS))
        return self
    
    def add_cookies(self, cookies):
        """添加cookies实现登录
        
        Args:
            cookies: cookie列表
        """
        valid_cookies = [cookie for cookie in cookies if cookie.get('name') and cookie.get('value')]
        
        for cookie in valid_cookies:
            self.driver.add_cookie(cookie)
        
        # 刷新页面使cookie生效
        self.driver.refresh()
        return self
    
    def get_title(self):
        """获取页面标题"""
        return self.driver.title
    
    def take_screenshot(self, filename):
        """截图保存
        
        Args:
            filename: 截图文件名
        """
        self.driver.save_screenshot(filename)
        return self