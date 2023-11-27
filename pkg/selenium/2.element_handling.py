from selenium import webdriver
from selenium.webdriver.common.by import By


# 设置启动浏览器的参数
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)  # 不要自动关闭浏览器
driver = webdriver.Chrome(options=options)

url = "https://passport.baidu.com/v2/?login"
driver.get(url)

# Selenium 的 WebElement 类是控制页面元素的核心。
# 查找元素。返回 WebElement 实例。
userlogButton = driver.find_element(By.XPATH, "//p[@title='用户名登录']")
# 获取该元素中指定的属性的值
print(userlogButton.get_attribute("class"))
# 可以通过 outerHTML 关键字，获取整个元素，而不只获取特定的属性。这个用法在官方文档中没有任何示例？还是我没找到？
print(userlogButton.get_attribute("outerHTML"))
# 模拟点击该元素
userlogButton.click()

# 模拟输入
# TODO: 在 input 标签中输入

# driver.find_element(By.XPATH, "//input[@placeholder='请输入手机号']").send_keys("")
# driver.find_element(By.XPATH, "//input[@class='policy_tip-checkbox']").click()
# driver.find_element(By.XPATH, "//button[text()='获取验证码']").click()
