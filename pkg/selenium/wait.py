from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # 不要自动关闭浏览器

    driver = webdriver.Chrome(options=options)

    # 有时候一个页面还没加载完成，selenium 无法获取到元素，此时可以让 selenium 等待一会，以便保证可以正确找到想要的元素
    # implicitly_wait() 是一种隐式等待。这是一个全局设置，适用于所有 driver 下的定位元素操作（比如 find_element() 等）。
    # 每个定位元素的操作在未找到元素时，都会等待 X 时间后，如果还没有找到该元素，则立刻返回错误。默认值: 0。i.e. 只要没找到立刻返回错误  # noqa: E501
    driver.implicitly_wait(2)

    url = "https://passport.baidu.com/v2/?login"
    driver.get(url)

    userlogButton = driver.find_element(By.XPATH, "//p[@title='用户名登录']")
    print(userlogButton.get_attribute("class"))
    print(userlogButton.get_attribute("outerHTML"))
    userlogButton.click()
