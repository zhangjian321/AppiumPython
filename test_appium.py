# coding = utf-8

'''
Created on: 2017-5-27
Author: Albert
Project：Wooplus
'''

import unittest
from appium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait


class TestWooplus(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        desired_caps = {'platformName': 'Android',
                        'platformVersion': '5.0',
                        'deviceName': '167850c8',
                        'app': 'D:\\android测试版\\304(47_5.2.3).apk',
                        'appPackage': 'com.mason.wooplus',
                        'appActivity': '.activity.SplashActivity',
                        'unicodeKeyboard': True,
                        'resetKeyboard': True,
                        'noReset': True}
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)  # 隐式等待，在查找元素时也会以5秒来作为超市等待

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    # 只测试能否正常的登陆app
    def test_1_login(self):
        driver = self.driver
        if self.is_element_exist('id', 'com.mason.wooplus:id/me'):  # 判断是否登陆
            driver.find_element_by_id('com.mason.wooplus:id/me').click()
            driver.find_element_by_id('com.mason.wooplus:id/right_menu_settings').click()
            driver.find_elements_by_class_name('android.widget.RelativeLayout')[3].click()
            driver.find_element_by_id('com.mason.wooplus:id/buttonOk').click()
        driver.find_element_by_id('com.mason.wooplus:id/sign_in').click()
        edit_texts = driver.find_elements_by_class_name('android.widget.EditText')
        edit_texts[0].send_keys('aaaaaa@gmail.com')  # 这个居然会自动判断文本框中是否有内容，有，则会自动清空再输入
        edit_texts[1].send_keys('aaaaaa')
        driver.find_element_by_id('com.mason.wooplus:id/submit_btn').click()
        # WebDriverWait(driver, 10, poll_frequency=0.5, ignored_exceptions=None).until(lambda
        # x:x.find_element_by_name('Meet the one on WooPlus'))
        sleep(10)
        # 判断是否登陆成功
        if self.is_element_exist('name', 'OK, Let\'s Go') or self.is_element_exist('id', 'com.mason.wooplus:id/me'):
            print('test_1_login is done.')
        else:
            raise Exception('Login is failed.')

    # 测试左右滑动cards
    def test_2_swipe_cards(self):
        sleep(10)
        self.swipe_left(1000)
        sleep(2)
        self.swipe_right(1000)
        if self.is_element_exist('id', 'Wow! You two liked each other. Chat for free!'):
            self.driver.find_element_by_id('com.mason.wooplus:id/maybe_later').click()
        print('test_2_swipe_cards is done.')

    # 测试发送消息
    def test_3_send_message(self):
        driver = self.driver
        driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.mason.wooplus:id/message")').click()
        driver.find_elements_by_id('com.mason.wooplus:id/header')[0].click()
        driver.find_element_by_id('com.mason.wooplus:id/rc_edit_text').send_keys('Hello!')
        driver.find_element_by_android_uiautomator('new UiSelector().resourceId("com.mason.wooplus:id/rc_send_toggle")').click()
        # self.assertIsNone(driver.find_element_by_id('com.mason.wooplus:id/rc_warning'), 'Message send fail.')
        if not self.is_element_exist('id', 'com.mason.wooplus:id/rc_warning') or self.is_element_exist('name', 'The user is now blocking messages.'):
            print('test_3_send_message is done.')
        else:
            raise Exception('Message send fail.Please check the network or block.')

    def swipe_left(self, t):
        size = self.get_size()  # size[0]==width, size[1]==height
        x1 = int(size[0] * 0.8)
        y1 = int(size[1] * 0.3)
        x2 = int(size[0] * 0.2)
        y2 = int(size[1] * 0.3)
        self.driver.swipe(x1, y1, x2, y2, t)

    def swipe_right(self, t):
        size = self.get_size()
        x1 = int(size[0] * 0.2)
        y1 = int(size[1] * 0.3)
        x2 = int(size[0] * 0.8)
        y2 = int(size[1] * 0.3)
        self.driver.swipe(x1, y1, x2, y2, t)

    def get_size(self):
        width = self.driver.get_window_size()['width']
        height = self.driver.get_window_size()['height']
        return width, height

    def logout(self):
        driver = self.driver

    def is_element_exist(self, ca, string):
        try:
            if ca == 'id':
                e = self.driver.find_element_by_id(string)
            elif ca == 'name':
                e = self.driver.find_element_by_name(string)
            return True
        except Exception:
            return False

    # def test_number(self):
    #     self.test_login()
    #     self.test_swipe_cards()

if __name__ == '__main__':
    unittest.main()  # 该方法执行会让测试用例按照数字和大小写字母来顺序执行

    # # 直接将一个模块中的所有用例放在一个用例集合中，多个模块多个集合
    # cases_TestWooplus = unittest.TestLoader().loadTestsFromTestCase(TestWooplus)
    # cases_TestOne = unittest.TestLoader().loadTestsFromTestCase(my_testRunner.TestOne)
    # suite = unittest.TestSuite([cases_TestWooplus, cases_TestOne])  # 将两个小集合中的用例集中放在一个大集合中，便于一起执行
    # suite.addTest(my_testRunner.TestOne('Test_2'))  # 这里将一个模块中的某一个用例再添加到大集合中，就会再执行一遍
    # unittest.TextTestRunner(verbosity=2).run(suite)

    # suite = unittest.TestSuite()  # 这种方法用于有选择的执行测试用例，最好不要去注释测试用例
    # suite.addTest(TestWooplus('test_1_login'))
    # suite.addTest(TestWooplus('test_2_swipe_cards'))
    # unittest.TextTestRunner(verbosity=2).run(suite)  # suite中的TestCase也会按照数字和大小写字母来顺序执行

