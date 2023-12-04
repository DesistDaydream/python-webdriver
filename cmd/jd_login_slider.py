from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common import NoSuchElementException, NoSuchWindowException, TimeoutException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx
from zipfile import ZipFile

import cv2

import sys, os, requests, base64, time, random  # noqa: E401

chrome_driver_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chromedriver")
version_file_path = os.path.join(chrome_driver_folder, "version")
chrome_driver_versions_json = (
    "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
)


def version_match(chrome_version, driver_version):
    return chrome_version[0 : chrome_version.rfind(".")] == driver_version[0 : driver_version.rfind(".")]


def unzip_chrome_driver(final_version_dir, zip_file_path):
    f = ZipFile(zip_file_path, "r")
    for file in f.namelist():
        f.extract(file, final_version_dir)
    f.close()
    os.remove(zip_file_path)


# 下载 chromedriver
def download_chrome_driver():
    if not os.path.exists(chrome_driver_folder):
        os.mkdir(chrome_driver_folder)

    resp = requests.get(chrome_driver_versions_json)
    json = resp.json()
    versions = json["versions"]
    # 从注册表中获取系统中 Chrome 的版本
    chrome_version, _ = QueryValueEx(OpenKey(HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"), "version")

    match = list(filter(lambda x: version_match(chrome_version, x["version"]), versions))
    length = len(match)
    if length == 0:
        print(f"没有找到相应版本的 ChromeDriver，当前 Chrome 版本：{chrome_version}")
        return 0
    else:
        download_json = match[length - 1]
        final_version = download_json["version"]
        final_version_dir = os.path.join(chrome_driver_folder, final_version)
        if not os.path.exists(final_version_dir):
            platform_json = list(
                filter(lambda x: x["platform"] == "win64", download_json["downloads"]["chromedriver"])
            )[0]
            download_url = platform_json["url"]
            print(f"找到并开始下载相应版本的 ChromeDriver，版本：{final_version}")
            download_resp = requests.get(download_url)
            os.mkdir(final_version_dir)
            zip_file_path = os.path.join(final_version_dir, "chromedriver.zip")
            with open(zip_file_path, "wb") as zip_file:
                zip_file.write(download_resp.content)
                print("下载成功")
            with open(version_file_path, "w") as version_file:
                version_file.write(final_version)
            unzip_chrome_driver(final_version_dir, zip_file_path)


# 滑块移动
def get_track(distance):
    tracks = []  # 移动轨迹
    current = 0  # 当前位移
    mid = distance * 4 / 5  # 减速阈值
    t = 0.2  # 计算间隔
    v = 0  # 初速度
    while current < distance:
        if current < mid:
            a = random.uniform(200, 500)  # 加速度？
        else:
            a = -(random.uniform(12.5, 13.5))
        v0 = v
        v = v0 + a * t  # 当前速度?
        x = v0 * t + 1 / 2 * a * t * t  # 移动距离?
        current += x  # 当前位移?

        # 加入轨迹？不用比较直接写 track.append(round(move))？
        if 0.6 < current - distance < 1:
            x = x - 0.53
            tracks.append(round(x, 2))

        elif 1 < current - distance < 1.5:
            x = x - 1.4
            tracks.append(round(x, 2))
        elif 1.5 < current - distance < 3:
            x = x - 1.8
            tracks.append(round(x, 2))

        else:
            tracks.append(round(x, 2))

    print(sum(tracks))
    return tracks


# 生成一个列表，和为19
def generate_list():
    while True:
        lst = random.sample(range(1, 20), random.randint(2, 4))
        if sum(lst) == 19:
            return lst


def get_chrome_driver_exec_path():
    if not os.path.exists(version_file_path):
        return ""
    else:
        with open(version_file_path, "r") as version_file:
            version = version_file.read()
        return os.path.join(chrome_driver_folder, version, "chromedriver-win64", "chromedriver.exe")


def init_webdriver():
    ua = "jdapp;android;12.1.6;;;M/5.0;appBuild/98973;ef/1;ep/%7B%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22ts%22%3A1696642454996%2C%22ridx%22%3A-1%2C%22cipher%22%3A%7B%22sv%22%3A%22CJK%3D%22%2C%22ad%22%3A%22DJPuYzqmZJCyDNZrZwG1DG%3D%3D%22%2C%22od%22%3A%22ENPsCJS2CNrwCtGmZJGmCK%3D%3D%22%2C%22ov%22%3A%22Ctu%3D%22%2C%22ud%22%3A%22DJPuYzqmZJCyDNZrZwG1DG%3D%3D%22%7D%2C%22ciphertype%22%3A5%2C%22version%22%3A%221.2.0%22%2C%22appname%22%3A%22com.jingdong.app.mall%22%7D;jdSupportDarkMode/0;Mozilla/5.0 (Linux; Android 10; Xiaomi Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36"  # noqa: E501
    print(f"User-Agent: {ua}")
    # stealth_js = "https://cdn.jsdelivr.net/gh/requireCool/stealth.min.js/stealth.min.js"
    # stealth_js_resp = requests.get(stealth_js)
    # js = stealth_js_resp.text
    # 读取本地 stealth.min.js 文件的内容。上面链接里的内容就算开了代理有时候都 get 不到。
    js = open("./config/stealth.min.js", "r").read()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)  # 不要自动关闭浏览器
    chrome_options.add_argument("log-level=3")
    # 去除webdriver特征
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(executable_path=get_chrome_driver_exec_path())
    driver = webdriver.Chrome(options=chrome_options, service=service)
    # driver = webdriver.Chrome(options=chrome_options)

    # 隐藏webdriver指纹
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": js})
    driver.execute_cdp_cmd("Emulation.setUserAgentOverride", {"userAgent": ua})
    return driver


def handlingSlider(driver: webdriver.Chrome):
    cpcImgPath = "./images/cpc_img.png"
    smallImgPath = "./images/small_img.png"

    while True:
        # 获取背景图片，并保存到本地
        cpc_img = driver.find_element(By.XPATH, "//img[@id='cpc_img']")
        with open(cpcImgPath, "wb") as f:
            f.write(base64.b64decode(cpc_img.get_attribute("src")[22:]))
        # 获取滑块图片，并保存到本地
        small_img = driver.find_element(By.XPATH, "//img[@id='small_img']")
        with open(smallImgPath, "wb") as f:
            f.write(base64.b64decode(small_img.get_attribute("src")[22:]))

        # 将图片灰度后，对比两张图片以定位滑块位置
        backgroud_img = cv2.imread(cpcImgPath, 0)
        slider_img = cv2.imread(smallImgPath, 0)
        resultMatrix = cv2.matchTemplate(backgroud_img, slider_img, cv2.TM_CCOEFF_NORMED)  # 获取滑块在缺口图的位置
        _minVal, _maxVal, minLoc, maxLoc = cv2.minMaxLoc(resultMatrix)  # 获取最佳与最差匹配
        print(_minVal, _maxVal, minLoc, maxLoc)
        distance = int(maxLoc[0] * 39 / 50)
        # distance = loc * 278 / 360

        # 获取滑块元素
        slider = driver.find_element(By.XPATH, "//div[@class='bg-blue']")
        # 移动滑块
        action = ActionChains(driver)  # 实例化一个动作链
        action.click_and_hold(slider).perform()  # 按住滑块
        # ==========================
        tracks = get_track(distance)
        for track in tracks:
            action.move_by_offset(track, 0).perform()
        time.sleep(0.18)
        action.move_by_offset(-3, 0).perform()
        action.move_by_offset(3, 0).perform()
        # action.move_by_offset(distance + random.randint(22, 23), 0).perform()  # 移动缺口过后
        # time.sleep(random.uniform(0.5, 0.8))  # 停留时间
        # for x in generate_list():
        #     action.move_by_offset(-x, 0).perform()  # 逆向移动
        #     time.sleep(random.uniform(0.1, 0.3))
        # ==========================
        action.release().perform()  # 释放滑块

        time.sleep(3)


def login(driver: webdriver.Chrome):
    # 输入手机号并点击发送验证码
    driver.find_element(By.XPATH, "//input[@placeholder='请输入手机号']").send_keys(sys.argv[1])
    driver.find_element(By.XPATH, "//input[@class='policy_tip-checkbox']").click()
    driver.find_element(By.XPATH, "//button[text()='获取验证码']").click()

    # 处理滑块验证
    handlingSlider(driver)


def getCookie(driver: webdriver.Chrome):
    cookies = driver.get_cookies()
    pt_key = ""
    pt_pin = ""
    for cookie in cookies:
        if cookie["name"] == "pt_key":
            pt_key = cookie["value"]
        elif cookie["name"] == "pt_pin":
            pt_pin = cookie["value"]

    print(f"pt_key: {pt_key}")
    print(f"pt_pin: {pt_pin}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("请输入账号")
        exit()

    # 下载 chrome driver
    download_chrome_driver()

    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", True)  # 不要自动关闭浏览器
    # driver = webdriver.Chrome(options=options)
    driver = init_webdriver()
    driver.implicitly_wait(3)
    url = "https://home.m.jd.com/myJd/newhome.action"
    driver.get(url)

    login(driver)

    try:
        if WebDriverWait(driver, 600, poll_frequency=0.2, ignored_exceptions=None).until(
            expected_conditions.title_is("多快好省，购物逛京东！")
        ):
            print("登录成功")
    except NoSuchElementException:
        exit(0)
    except NoSuchWindowException:
        exit(0)
    except TimeoutException:
        exit(0)

    getCookie(driver)

    driver.close()
