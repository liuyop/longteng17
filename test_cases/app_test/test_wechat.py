import pytest


@pytest.mark.nondestructive
def test_login(login_page):
    """登录：传入用户名和密码"""
    login_page.login('18010181267', '123456')


@pytest.mark.nondestructive
def test_online(online_page):
    """聊天：传入联系人和消息"""
    online_page.send_content('歪歪', '嗨！你好')


# if __name__ == '__main__':
#     pytest.main(['test_wechat.py', '--html=report.html'])