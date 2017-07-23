import unittest
from appium import webdriver
from time import sleep
import HTMLTestRunner
import time
import my_testRunner


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        desired_caps = {'platformName': 'Android',
                        'platformVersion': '6.0',
                        'deviceName': '192.168.163.101:5555',
                        'app': 'C:\\Users\\admin\\Desktop\\selendroid-test-app-0.17.0.apk',
                        'appPackage': 'io.selendroid.testapp',
                        'appActivity': '.HomeScreenActivity',
                        'unicodeKeyboard': True,
                        'resetKeyboard': True,
                        'automationName': 'Selendroid',
                        'noReset': True}
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_1(self):
        driver = self.driver
        driver.find_element_by_id('buttonStartWebview').click()
        driver.find_element_by_id('spinner_webdriver_test_data').click()
        driver.find_element_by_link_text('xhtmlTestPage').click()
        sleep(2)
        # 此时验证的信息在WEBVIEW_0的context中，所以需要切换到web app
        driver.switch_to.context('WEBVIEW_0')
        self.assertTrue(driver.page_source.__contains__('XHTML Might Be The Future'))
        # print(driver.contexts)  # 打印当前界面中的所有上下

    def test_2(self):
        driver = self.driver
        driver.find_elements_by_link_text('click me')[0].click()
        sleep(2)
        self.assertTrue(driver.page_source.__contains__('List of stuff'))
        driver.switch_to.context('NATIVE_APP')
        driver.find_element_by_id('goBack').click()
        sleep(1)
        self.assertTrue(driver.find_element_by_id('buttonTest').is_displayed())

if __name__ == '__main__':
    cases_MyTestCase = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
    cases_my_testRunner = unittest.TestLoader().loadTestsFromTestCase(my_testRunner.TestOne)
    suite = unittest.TestSuite([cases_MyTestCase, cases_my_testRunner])
    suite.addTest(my_testRunner.TestOne('test_2'))
    now = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
    fp = open(now + 'Result.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, verbosity=2, title='Test Report', description=u'Result:')
    runner.run(suite)
    print(now)
    fp.close()