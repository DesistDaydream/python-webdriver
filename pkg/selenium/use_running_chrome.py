from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:39000")
driver = webdriver.Chrome(options=options)
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
