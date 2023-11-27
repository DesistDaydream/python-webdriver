# 来源: https://github.com/SeleniumHQ/seleniumhq.github.io/blob/trunk/examples/python/tests/getting_started/first_script.py

from selenium import webdriver
from selenium.webdriver.common.by import By

import time

# 设置启动浏览器的参数
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # 不要自动关闭浏览器

driver = webdriver.Chrome(options)

driver.get("https://www.selenium.dev/selenium/web/web-form.html")

title = driver.title

driver.implicitly_wait(0.5)

text_box = driver.find_element(by=By.NAME, value="my-text")
submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

text_box.send_keys("Selenium")
submit_button.click()

message = driver.find_element(by=By.ID, value="message")
text = message.text
