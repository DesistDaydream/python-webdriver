from selenium import webdriver


# 设置启动浏览器的参数
userDataDir = r"C:\Users\DesistDaydream\AppData\Local\Google\Chrome\User Data"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # 不要自动关闭浏览器
options.add_argument(f"--user-data-dir={userDataDir}")
options.add_argument("--profile-directory=ProfileSelenium")
# TODO: 只有关闭所有浏览器才能正常启动。如何避免？

driver = webdriver.Chrome(options=options)

url = "https://www.baidu.com"
driver.get(url)
