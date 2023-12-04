from typing import Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import cv2
import requests

import sys, time, random  # noqa: E401

backgroundImgPath = "./images/background.png"
blockImgPath = "./images/block.png"


def initWebDriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:39000")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    return driver


def login(driver: webdriver.Chrome) -> None:
    driver.execute_script("window.open('https://www.liepin.com/')")
    driver.switch_to.window(driver.window_handles[-1])
    print(driver.title)

    # 旋转呢密码登录
    driver.find_element(By.XPATH, "//*[@id='home-banner-login-container']/div/div/div/div/div[2]/div/div[2]").click()
    # 输入用户名和密码
    driver.find_element(By.XPATH, '//*[@id="login"]').send_keys(sys.argv[1])
    driver.find_element(By.XPATH, '//*[@id="pwd"]').send_keys(sys.argv[2])
    # 同意协议
    pEle = driver.find_element(
        By.XPATH, '//*[@id="home-banner-login-container"]/div/div/div/div/div[4]/div/label/span[1]/input'
    )
    # 若已经勾选则不要再点击。
    if pEle.is_selected():
        print("已勾选")
    else:
        pEle.click()

    time.sleep(1)
    # 点击登录
    driver.find_element(
        By.XPATH, '//*[@id="home-banner-login-container"]/div/div/div/div/div[3]/div/form/button'
    ).click()

    # 处理图片
    maxLoc = handlingImg()

    # 处理滑块验证
    handlingSlider(driver, maxLoc)


def handlingImg() -> int:
    # 获取滑块图片
    driver.switch_to.frame("tcaptcha_iframe")
    time.sleep(2)

    backgroundImgUrl = driver.find_element(By.XPATH, '//*[@id="slideBg"]').get_attribute("src")
    print(backgroundImgUrl)
    with open(backgroundImgPath, "wb") as f:
        f.write(requests.get(backgroundImgUrl).content)  # type: ignore

    blockImgEleUrl = driver.find_element(By.XPATH, '//*[@id="slideBlock"]').get_attribute("src")
    print(blockImgEleUrl)
    with open(blockImgPath, "wb") as f:
        f.write(requests.get(blockImgEleUrl).content)  # type: ignore

    # 将图片灰度后，对比两张图片以定位滑块位置
    backgroundImg = cv2.imread(backgroundImgPath, 0)
    cv2.imwrite("images/background_01.png", backgroundImg)
    blockImg = cv2.imread(blockImgPath, 0)
    # 滑块图片周围有阴影会干扰匹配，去掉周围的干扰像素
    blockImg = blockImg[24 : blockImg.shape[0] - 24, 24 : blockImg.shape[1] - 24]
    cv2.imwrite("images/block_01.png", blockImg)

    # 对图像进行二值化处理。转成纯色以便更利于图像匹配。
    _, backgroundImg = cv2.threshold(backgroundImg, 110, 255, cv2.THRESH_BINARY)
    _, blockImg = cv2.threshold(blockImg, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imwrite("images/background_02.png", backgroundImg)
    cv2.imwrite("images/block_02.png", blockImg)

    # 获取滑块在缺口图的位置
    resultMatrix = cv2.matchTemplate(backgroundImg, blockImg, cv2.TM_CCOEFF_NORMED)
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(resultMatrix)  # 获取最佳与最差匹配
    print(_minVal, _maxVal, minLoc, maxLoc)

    # 返回最佳匹配的横坐标
    return maxLoc[0]


def handlingSlider(driver: webdriver.Chrome, maxLoc) -> None:
    # 调整滑块需要移动的距离
    # 由于获取到的图片与页面展示的图片的像素不一样，页面展示的图片是经过压缩的，所以要先等比例调整。
    # 然后由于滑块不是从最左侧开始移动的，所以还要减去滑块左侧的一部分距离
    distance = maxLoc * 341 / 680 - 37

    # 获取滑块元素
    slider = driver.find_element(By.XPATH, '//*[@id="tcaptcha_drag_thumb"]')

    # 移动滑块
    action = ActionChains(driver)  # 实例化一个动作链
    action.click_and_hold(slider).perform()  # 按住滑块

    # action.pause(0.3).move_by_offset(distance / 4, 5).perform()
    # action.pause(0.1).move_by_offset(distance / 2, -2).perform()
    # action.pause(0.1).move_by_offset(distance / 4, -3).perform()
    # ==========================
    # 将需要移动的距离拆分为多段
    tracks = get_track(distance)
    print(distance, tracks)
    # 每次只移动一点以模拟人类手动移动滑块的情况。避免移动过快导致验证失败
    # TODO: 移动速度如何确定？
    for track in tracks:
        action.pause(0.01).move_by_offset(track, int(random.uniform(-1, 1))).perform()
    # ==========================

    action.release().perform()  # 释放滑块

    # time.sleep(3)


# 将需要移动的距离拆分为多段
def get_track(distance):
    # 移动轨迹
    track = []
    # 初始位置、初始速度、时间间隔
    # - 速度是指每次移动滑块的距离。并不是传统意义上的用手握住鼠标后滑动的速度。
    # - 时间间隔是指要把待移动举例拆分为多少段
    current, v, t = 0, 1, 0.2
    # 当前位置只要小于需要移动的举例，则继续拆分距离
    while current < distance:
        a = 4  # 加速度为2
        v0 = v  # 初速度
        v = v0 + a * t  # 当前速度
        # 移动距离
        move = v0 * t + 0.5 * a * (t * t)
        print(move)
        # 当前位移。用以与待移动的距离进行比较，当当前位置已经超过待移动举例时，则不用再拆分了
        current += move
        # 加入轨迹
        track.append(round(move))
    abc = 0
    for i in track:
        abc += i
    print(abc)
    return track


if __name__ == "__main__":
    driver = initWebDriver()
    # login(driver)

    # 单独测试滑块功能，要保证页面已打开且已显示滑块验证
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if driver.title == "【猎聘】-招聘_找工作_求职_企业招人平台":
            break
    # 处理图片
    maxLoc = handlingImg()
    # 处理滑块验证
    handlingSlider(driver, maxLoc)