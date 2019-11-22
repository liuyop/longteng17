import pytest
from test_cases.web_test.pages.baidu_page import BaiduPage
from test_cases.web_test.pages.login_page import LoginPage
from test_cases.web_test.pages.menu_page import MenuPage
from test_cases.web_test.pages.add_goods_page import AddGoodsPage
from test_cases.web_test.pages.goods_list_page import GoodsListPage


@pytest.fixture
def selenium(selenium):  # 覆盖原有selenium
    selenium.implicitly_wait(15)
    # selenium.maximize_window() # 启动浏览器后最大化
    return selenium


@pytest.fixture
def chrome_options(chrome_options):  # 覆盖原有chrome_options
    chrome_options.add_argument('--start-maximized') # 以最大化启动浏览器
    chrome_options.add_experimental_option('w3c',  False)
    chrome_options.add_argument("--no-sandbox")  #添加沙盒模式
    # chrome_options.add_argument('--headless')  # 无界面启动
    # chrome_options.headless = True # 无界面启动
    return chrome_options

@pytest.fixture
def baidu_page(selenium):
    selenium.get('https://www.baidu.com')
    baidu_page = BaiduPage(selenium)
    return baidu_page

@pytest.fixture
def ecshop_login_page(selenium):
    # 1. 进入这个页面
    selenium.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    # 2. 生成并返回页面对象
    ecshop_login_page = LoginPage(selenium)
    return ecshop_login_page

@pytest.fixture
def ecshop_menu_page(selenium, login_page):
    """登录后返回菜单页面"""
    login_page.login('liuyp', 'abc123')  # 也可以从数据文件或环境变量中读取
    return MenuPage(selenium)

@pytest.fixture
def add_goods_page(selenium, menu_page):
    """从MenuPage跳到添加商品页面"""
    menu_page.click_menu('商品管理', '添加新商品')
    # 把页面对象返回给用例
    return AddGoodsPage(selenium)

# @pytest.fixture
# def goods_list_page(selenium, menu_page):
#     """从MenuPage跳到添加商品页面"""
#     menu_page.click_menu('商品管理', '商品列表')
#     # 把页面对象返回给用例
#     return GoodsListPage(selenium)











