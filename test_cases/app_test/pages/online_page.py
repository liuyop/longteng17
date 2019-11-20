

class OnlinePage(object):

    contact_btn_loc = ('id', 'com.lqr.wechat:id/llContacts')
    # name_btn_loc = ('xpath', '//*[@text="歪歪"]')
    cheat_btn_loc = ('id', 'com.lqr.wechat:id/btnCheat')
    content_ipt_loc = ('id', 'com.lqr.wechat:id/etContent')
    send_btn_loc = ('id', 'com.lqr.wechat:id/btnSend')

    def __init__(self, driver):
        self.driver = driver

    def click_contact_button(self):
        """点击通讯录按钮"""
        self.driver.find_element(*self.contact_btn_loc).click()

    def click_name_button(self, name):
        """点击联系人"""
        self.driver.find_element_by_xpath(f'//*[@text="{name}"]').click()
        # self.driver.find_element(*self.name_btn_loc).click()

    def click_cheat_button(self):
        """点击发消息"""
        self.driver.find_element(*self.cheat_btn_loc).click()

    def input_content(self, content):
        """输入消息"""
        self.driver.find_element(*self.content_ipt_loc).send_keys(content)

    def click_send_button(self):
        """点击发送按钮"""
        self.driver.find_element(*self.send_btn_loc).click()

    def send_content(self, name, content):
        self.click_contact_button()
        self.click_name_button(name)
        self.click_cheat_button()
        self.input_content(content)
        self.click_send_button()




