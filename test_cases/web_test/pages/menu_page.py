class MenuPage(object):
    # 实例化时要传入driver
    def __init__(self, driver):
        self.driver = driver
        self.driver.switch_to.frame('menu-frame')

    # 页面元素
    def click_menu(self, menu_name, sub_menu_name):
        self.driver.find_element_by_link_text(menu_name).click()
        self.driver.find_element_by_link_text(sub_menu_name).click()
        self.driver.switch_to.default_content()