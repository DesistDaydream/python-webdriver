# https://www.selenium.dev/zh-cn/documentation/webdriver/interactions/windows
#
from selenium import webdriver


def tabHandle(driver: webdriver.Chrome):
    # WebDriver 不区分窗口和标签页。如果打开了一个新标签页或窗口，Selenium 将使用 **Handle(句柄)** 处理它，每个标签页和窗口的 Handle 是其唯一的标识符，该标识符在单个会话中保持持久性。  # noqa: E501
    # 可以使用以下方法获得当前窗口的窗口句柄:
    print(driver.current_window_handle)
    # 这个窗口的 Handle 与打开窗口时创建的第一个标签页的 Handle 相同。，若创建了第二个标签页，关闭了第一个标签页，则窗口的 Handle 与 第二个标签页的 Handle 相同。也就是说，窗口即是标签页。窗口就是打开的第一个标签页。  # noqa: E501

    # 获取所有窗口的所有标签页的句柄，返回一个 `List[str]`，不管标签页在多少个窗口中，哪怕窗口属于其他账户，也会一并获取到。  # noqa: E501
    all_handles = driver.window_handles

    for handle in all_handles:  # 遍历全部标签页句柄
        print(handle)
        # TODO: 通过标签页句柄获取标签页信息。handle 里只有标签页的句柄字符串，类似于 ID。

    # 通过执行 JS 脚本在新标签页打开网站
    driver.execute_script("window.open('https://home.m.jd.com/myJd/newhome.action')")
    # 切换到最新打开的标签页
    driver.switch_to.window(all_handles[-1])


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:39000")
    driver = webdriver.Chrome(options=options)

    # 打开一个新的窗口并打开一个新标签页
    driver.switch_to.new_window("window")
    # 在当前窗口中打开一个标签页
    driver.switch_to.new_window("tab")

    tabHandle(driver)
