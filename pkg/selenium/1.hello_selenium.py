# 来源: https://github.com/SeleniumHQ/seleniumhq.github.io/blob/trunk/examples/python/tests/hello/hello_selenium.py
from selenium import webdriver

# 设置启动浏览器的参数
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # 不要自动关闭浏览器

# 实例化一个 Chrome 类型的 WebDriver。
driver = webdriver.Chrome(options=options)
# selenium 依赖于 WebDriver，这里我们实例化了一个 Chrome 的 WebDriver。selenium 会自动下载 chromedriver.exe 文件到 `~/.cache/selenium/chromedriver/win64/${VERSION}/` 目录中  # noqa: E501
# 然后使用 chromedriver.exe 启动浏览器。

driver.get("http://selenium.dev")
