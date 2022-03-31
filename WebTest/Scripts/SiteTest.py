import urllib3
from selenium.webdriver.common.by import By
from selenium import webdriver
import unittest
from Locators import Locator

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SiteTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://techdemotbaseo.kinsta.cloud/")
        self.driver.maximize_window()
        self.password = self.driver.find_element(By.XPATH, Locator.password_input)
        self.submit = self.driver.find_element(By.XPATH, Locator.submit)

    def test0_GoToURL(self):
        self.assertTrue('TBA' in self.driver.title, 'Fail to load home page')

    def test1_InsertValidPassword(self):
        self.password.send_keys('optivalqa')
        self.submit.click()
        test = self.driver.find_element(By.XPATH, "/html/body/section[2]/div/h1").text
        self.assertEqual(test, "BEST BETTING APPS IN THE UK", "Not Found")

    def test2_InsertInValidPassword(self):
        self.password.send_keys('invalid_optivalqa')
        self.submit.click()
        self.assertTrue('TBA' in self.driver.title, "Fail didn't return to the home page")

    def tearDown(self):
        if self.driver is not None:
            self.driver.close()
            self.driver.quit()



