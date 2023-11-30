# https://www.selenium.dev/zh-cn/documentation/webdriver/interactions/
#
from selenium import webdriver
import time


def initWebDriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    # 若 Chrome 使用 --remote-debugging-port 参数开启了 Debug 端口，selenium 可以通过该端口直接控制当前正在运行的浏览器
    options.add_experimental_option("debuggerAddress", "127.0.0.1:39000")
    driver = webdriver.Chrome(options=options)

    return driver


# https://www.selenium.dev/zh-cn/documentation/webdriver/interactions/
# 浏览器导航
def browserNavigation(driver: webdriver.Chrome):
    # 打开网站
    driver.get("https://selenium.dev")
    time.sleep(2)
    # 后退
    driver.back()
    time.sleep(2)
    # 前进
    driver.forward()
    time.sleep(2)
    # 刷新
    driver.refresh()


# https://www.selenium.dev/zh-cn/documentation/webdriver/interactions/alerts/
# 浏览器告警框、提示框、确认框
def browserAlert(driver: webdriver.Chrome):
    pass


# https://www.selenium.dev/zh-cn/documentation/webdriver/interactions/cookies/
# Cookie 管理
def browserCookie(driver: webdriver.Chrome):
    pass


if __name__ == "__main__":
    driver = initWebDriver()

    browserNavigation(driver)
    # browserAlert(driver)
