from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SearchResultPage:
    """百度搜索结果页面对象类，封装搜索结果页面的元素和操作"""
    
    # 页面元素定位器
    SEARCH_RESULTS = (By.ID, "content_left")
    RESULT_ITEMS = (By.CSS_SELECTOR, ".result.c-container")
    RESULT_TITLES = (By.CSS_SELECTOR, ".t a")
    RESULT_SUMMARIES = (By.CSS_SELECTOR, ".c-abstract")
    NEXT_PAGE = (By.XPATH, "//a[@class='n' and contains(text(), '下一页')]")
    
    def __init__(self, driver):
        """初始化页面对象
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def wait_for_results(self):
        """等待搜索结果加载完成"""
        self.wait.until(EC.presence_of_element_located(self.SEARCH_RESULTS))
        return self
    
    def get_result_count(self):
        """获取搜索结果数量"""
        results = self.driver.find_elements(*self.RESULT_ITEMS)
        return len(results)
    
    def get_result_titles(self):
        """获取所有搜索结果的标题"""
        titles = self.driver.find_elements(*self.RESULT_TITLES)
        return [title.text for title in titles]
    
    def get_result_summaries(self):
        """获取所有搜索结果的摘要"""
        summaries = self.driver.find_elements(*self.RESULT_SUMMARIES)
        return [summary.text for summary in summaries]
    
    def click_result(self, index=0):
        """点击指定索引的搜索结果
        
        Args:
            index: 结果索引，默认为0（第一个结果）
        """
        results = self.driver.find_elements(*self.RESULT_TITLES)
        if 0 <= index < len(results):
            results[index].click()
        return self
    
    def go_to_next_page(self):
        """点击下一页"""
        next_page = self.wait.until(EC.element_to_be_clickable(self.NEXT_PAGE))
        next_page.click()
        self.wait_for_results()
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