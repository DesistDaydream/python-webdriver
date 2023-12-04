from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

import cv2

import time, random, base64  # noqa: E401

backgroundImgPath = "./images/jd_background.png"
blockImgPath = "./images/jd_block.png"
backgroundImgGrayPath = "./images/jd_background_gray.png"
blockImgGrayPath = "./images/jd_block_gray.png"
backgroundImgBinaryPath = "./images/jd_background_binary.png"
blockImgBinaryPath = "./images/jd_block_binary.png"


def initWebDriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:39000")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)

    return driver


def login(driver: webdriver.Chrome) -> None:
    driver.execute_script("window.open('https://plogin.m.jd.com/login/login')")
    driver.switch_to.window(driver.window_handles[-1])
    print(driver.title)

    # 选择密码登录
    driver.find_element(By.XPATH, '//*[@id="app"]/div/p[1]/span[1]').click()
    # 输入用户名和密码
    # TODO: 使用当前浏览器时有可能会保存了账号密码。有没有简单的清除输入框内容的方式？
    # driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(sys.argv[1])
    # driver.find_element(By.XPATH, '//*[@id="pwd"]').send_keys(sys.argv[2])
    # 同意协议
    pEle = driver.find_element(By.XPATH, '//*[@id="app"]/div/p[2]/input')
    # 若已经勾选则不要再点击。
    if pEle.is_selected():
        print("已勾选")
    else:
        pEle.click()

    time.sleep(1)
    # 点击登录
    driver.find_element(By.XPATH, '//*[@id="app"]/div/a').click()


def handlingImg() -> int:
    # 获取滑块图片
    time.sleep(2)

    backgroundImgEle = driver.find_element(By.XPATH, '//*[@id="cpc_img"]')
    with open(backgroundImgPath, "wb") as f:
        f.write(base64.b64decode(backgroundImgEle.get_attribute("src")[22:]))
    blockImgEleEle = driver.find_element(By.XPATH, '//*[@id="small_img"]')
    with open(blockImgPath, "wb") as f:
        f.write(base64.b64decode(blockImgEleEle.get_attribute("src")[22:]))

    # 将图片灰度后，对比两张图片以定位滑块位置
    backgroundImg = cv2.imread(backgroundImgPath, 0)
    cv2.imwrite(backgroundImgGrayPath, backgroundImg)
    blockImg = cv2.imread(blockImgPath, 0)
    cv2.imwrite(blockImgGrayPath, blockImg)

    # 对图像进行二值化处理。转成纯色以便更利于图像匹配。
    # _, backgroundImg = cv2.threshold(backgroundImg, 110, 255, cv2.THRESH_BINARY)
    # _, blockImg = cv2.threshold(blockImg, 40, 255, cv2.THRESH_BINARY_INV)
    # cv2.imwrite("images/background_02.png", backgroundImg)
    # cv2.imwrite("images/block_02.png", blockImg)

    # 获取滑块在缺口图的位置
    resultMatrix = cv2.matchTemplate(backgroundImg, blockImg, cv2.TM_CCOEFF_NORMED)
    _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(resultMatrix)
    print(_minVal, _maxVal, minLoc, maxLoc)

    # 返回最佳匹配的横坐标
    return maxLoc[0]


def handlingSlider(driver: webdriver.Chrome, maxLoc) -> None:
    # 调整滑块需要移动的距离
    # 由于获取到的图片与页面展示的图片的像素不一样，页面展示的图片是经过压缩的，所以要先等比例调整。
    distance = maxLoc * 275 / 290

    slider = driver.find_element(By.XPATH, '//*[@id="captcha_modal"]/div/div[3]/div/div')

    action = ActionChains(driver)
    action.click_and_hold(slider).perform()

    # 将需要移动的距离拆分为多段
    tracks, backTracks = get_track(distance)
    for track in tracks:
        action.move_by_offset(track, int(random.uniform(-1, 1))).perform()
    # action.move_by_offset(backTracks, int(random.uniform(-1, 1))).perform()

    action.release().perform()

    # time.sleep(3)


# 将需要移动的距离拆分为多段
def get_track(distanceTotal: int):
    tracks = []
    distanceCurrent, v, t = 0, 1, 0.2
    while distanceCurrent <= distanceTotal:
        a = 40
        v0 = v
        v = v0 + a * t
        move = v0 * t + 0.5 * a * (t * t)
        distanceCurrent += move
        tracks.append(round(move))

    print("待移动距离: {},计算出的总移动距离: {}".format(distanceTotal, sum(tracks)))
    print(tracks)

    backTracks = 0
    if sum(tracks) > distanceTotal:
        backTracks = distanceTotal - sum(tracks)
        print(backTracks)

    return tracks, backTracks


if __name__ == "__main__":
    driver = initWebDriver()
    login(driver)

    # 单独测试滑块功能，要保证页面已打开且已显示滑块验证
    # for handle in driver.window_handles:
    #     driver.switch_to.window(handle)
    #     if driver.title == "京东登录注册":
    #         break
    # 处理图片
    maxLoc = handlingImg()
    # 处理滑块验证
    handlingSlider(driver, maxLoc)
