class LoginPage(object):
    # 实例化时要传入driver
    def __init__(self, driver):
        self.driver = driver

    # 页面元素
    username_ipt_loc = ('id', 'com.lqr.wechat:id/etPhone')  # 用户名框
    password_ipt_loc = ('id', 'com.lqr.wechat:id/etPwd')  # 密码框
    login_btn_loc = ('id', 'com.lqr.wechat:id/btnLogin')  # 登录按钮

    # 对每个元素操作，封装一个方法
    def input_username(self, username):
        """输入用户名"""
        self.driver.find_element(*self.username_ipt_loc).send_keys(username)

    def input_password(self, password):
        """输入密码"""
        self.driver.find_element(*self.password_ipt_loc).send_keys(password)

    def click_login_button(self):
        """点击登录按钮"""
        self.driver.find_element(*self.login_btn_loc).click()

    # 业务组合操作
    def login(self, username, password):
        """输入关键字并搜索"""
        self.click_login_button()
        self.input_username(username)
        self.input_password(password)
        self.click_login_button()