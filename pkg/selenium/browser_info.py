# https://www.selenium.dev/zh-cn/documentation/webdriver/interactions/
#
from selenium import webdriver


def initWebDriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    # 若 Chrome 使用 --remote-debugging-port 参数开启了 Debug 端口，selenium 可以通过该端口直接控制当前正在运行的浏览器
    options.add_experimental_option("debuggerAddress", "127.0.0.1:39000")
    driver = webdriver.Chrome(options=options)

    return driver


if __name__ == "__main__":
    driver = initWebDriver()

    driver.switch_to.window(driver.window_handles[-1])
    # 当前标签页的标题
    print("标签页标题: ", driver.title)
    # 当前标签页的 URL
    print("标签页URL: ", driver.current_url)
