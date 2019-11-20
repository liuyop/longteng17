import pytest
from appium import webdriver
from test_cases.app_test.pages.login_page import LoginPage
from test_cases.app_test.pages.online_page import OnlinePage


@pytest.fixture(scope='session')
def driver():
    caps = {
        "platformName": "Android",
        "platformVersion": "5.1.1",
        "deviceName": "127.0.0.1:62001",
        "appPackage": "com.lqr.wechat",
        "appActivity": "com.lqr.wechat.ui.activity.SplashActivity",
        "unicodeKeyboard": True,
        "resetKeyboard": True,
        "autoLaunch": False
      }
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', caps)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    """登录"""
    driver.launch_app()
    login_page = LoginPage(driver)
    return login_page


@pytest.fixture
def online_page(driver, login_page):
    """登录后进入聊天页面"""
    driver.launch_app()
    login_page.login('18010181267', '123456')  # 也可以从数据文件或环境变量中读取
    return OnlinePage(driver)