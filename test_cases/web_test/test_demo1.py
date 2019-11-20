import pytest
import logging

@pytest.mark.skip
def test_baidu1(selenium):
    selenium.get('https://www.baidu.com')
    selenium.find_element_by_id('kw').send_keys('少年的你')
    selenium.find_element_by_id('su').click()

@pytest.mark.skip
def test_baidu2(selenium):
    from test_cases.web_test.pages.baidu_page import BaiduPage
    selenium.get('https://www.baidu.com')
    baidu_page = BaiduPage(selenium)
    baidu_page.search('少年的你')


@pytest.mark.skip
def test_baidu3(baidu_page):
    print('测试百度搜索 少年的你')
    baidu_page.search('少年的你')

@pytest.mark.skip
def test_ecshop_login1(selenium):
    from test_cases.web_test.pages.login_page import LoginPage
    selenium.get('http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    ecshop_login_page = LoginPage(selenium)
    ecshop_login_page.login('liuyp', 'abc123')


@pytest.mark.skip
def test_ecshop_login2(ecshop_login_page):
    ecshop_login_page.login('liuyp', 'abc123')


@pytest.mark.skip
def test_menu(selenium):
    from test_cases.web_test.pages.login_page import LoginPage
    from test_cases.web_test.pages.menu_page import MenuPage
    selenium.get(
        'http://39.104.14.232/ecshop/wwwroot/admin/privilege.php?act=login')
    page = LoginPage(selenium)
    page.login('admin', '123456')
    page = MenuPage(selenium)
    page.click_menu('商品管理', '添加新商品')


@pytest.mark.skip
def test_ecshop_menu(ecshop_menu_page):
    ecshop_menu_page.input_menu('商品管理', '添加新商品')

@pytest.mark.skip
def test_add_goods(add_goods_page):
    add_goods_page.input_goods_name('dell电脑')
    add_goods_page.input_goods_category("电脑")
    add_goods_page.input_goods_price('3999')
    add_goods_page.click_submit_btn()

def test_logging():
    logging.debug('调试日志')
    logging.info('fff')
    logging.warning('警告信息')
    logging.error('报错信息')
    logging.critical('严重出错')


# if __name__ == '__main__':
#     pytest.main(['test_demo1.py', '--html=report.html'])

