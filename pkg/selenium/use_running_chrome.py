from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initWebDriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    # 若 Chrome 使用 --remote-debugging-port 参数开启了 Debug 端口，selenium 可以通过该端口直接控制当前正在运行的浏览器
    options.add_experimental_option("debuggerAddress", "127.0.0.1:39000")
    driver = webdriver.Chrome(options=options)

    return driver


if __name__ == "__main__":
    driver = initWebDriver()

    driver.execute_script("window.open('https://home.m.jd.com/myJd/newhome.action')")
    driver.switch_to.window(driver.window_handles[-1])
    print(driver.title)

    wait = WebDriverWait(driver, 120)
    wait.until(EC.title_is("京东触屏版"))

    try:
        cookies = driver.get_cookies()
        pt_key = ""
        pt_pin = ""
        for cookie in cookies:
            if cookie["name"] == "pt_key":
                pt_key = cookie["value"]
            elif cookie["name"] == "pt_pin":
                pt_pin = cookie["value"]
        print(f"pt_key={pt_key};pt_pin={pt_pin};")
    except Exception as e:
        print("获取cookie失败:{}".format(e))
