from selenium import webdriver
from selenium.webdriver.common.by import By


def initWebDriver() -> webdriver.Chrome:
    # 设置启动浏览器的参数
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # 不要自动关闭浏览器
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    return driver


# 通过 XPath 定位元素
def XPath(driver: webdriver.Chrome):
    # 查找元素。返回 WebElement 实例。
    btn = driver.find_element(By.XPATH, '//*[@id="my-check-2"]')

    # 模拟点击该元素
    btn.click()


if __name__ == "__main__":
    driver = initWebDriver()

    url = "https://www.selenium.dev/selenium/web/web-form.html"
    driver.get(url)

    # Selenium 的 WebElement 类是控制页面元素的核心。
    # find_element() 方法返回一个 WebElement 实例
    ele = driver.find_element(By.CLASS_NAME, "form-control")

    # WebElement 下有多个方法可以获取该元素的信息或处理该元素。
    # 获取该元素中指定的属性的值
    print(ele.get_attribute("class"))
    # 可以通过 outerHTML 关键字，获取整个元素，而不只获取特定的属性。这个用法在官方文档中没有任何示例？还是我没找到？
    print(ele.get_attribute("outerHTML"))
    # 在该元素内输入内容（因为是 input 标签，如果是 button 标签则可以点击）
    ele.send_keys("DesistDaydream")

    # 通过 XPath 定位元素
    XPath(driver)
