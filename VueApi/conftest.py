import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from VueApi.config import  getConfig

cofing = getConfig.Config()
dr = cofing.getconf("DRIVER").driver
import pytest
import allure

driver = int(dr)
#添加报错截图到allure报告里，利用pytest钩子函数
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    hook pytest失败
    :param item:
    :param call:
    :return:
    '''
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # pic_info = adb_screen_shot()
        with allure.step('添加失败截图...'):
            allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

def pytest_configure(config):
    """忽略@pytest.mark.last警告"""
    config.addinivalue_line(
        "markers", "last"  # login_success 是标签名
    )

# def adb_screen_shot():
# driver.get_screenshot_as_png()
# driver.get_screenshot_as_base64()
# driver.get_screenshot_as_file("122.jpg")
# os.popen("adb screen -p testfailue.jpg")
from selenium.webdriver import Chrome, ChromeOptions


#pytest 的 fixture 函数方法，全局调用browser
@pytest.fixture(scope='session', autouse=True)
#allure.step('初始化浏览器')
def browser():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument("--window-size=1960,1080");

    global driver
    if driver == 1:
        driver = webdriver.Chrome(executable_path="d:\\vue_api\\chromedriver.exe")
    elif driver == 2:
        opt = ChromeOptions()  # 创建Chrome参数对象
        # , chrome_options = option
        opt.headless = True
        driver = webdriver.Chrome(executable_path="d:\\vue_api\\chromedriver.exe",chrome_options = option)

    return driver


# def browser():
#     global driver
#     if driver is None:
#         driver = webdriver.Chrome()
#     return driver
#
