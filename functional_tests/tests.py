from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element('id', 'id_list_table')        
                rows = table.find_elements('tag name', 'tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(.5)
        

    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)

        header_text = self.browser.find_element('tag name', 'h1').text
        self.assertIn('To-Do', header_text)

        input_box = self.browser.find_element('id', 'id_new_item')
        self.assertEqual(input_box.get_attribute('placeholder'), 'Enter a to-do item')

        input_box.send_keys('Buy peacock feathers')

        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        input_box = self.browser.find_element('id', 'id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element('id', 'id_new_item')

        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        first_user_list_url = self.browser.current_url
        self.assertRegex(first_user_list_url, '/lists/.+')

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)

        page_text = self.browser.find_element('tag name', 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        input_box = self.browser.find_element('id', 'id_new_item')

        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        second_user_list_url = self.browser.current_url
        self.assertRegex(second_user_list_url, '/lists/.+')
        self.assertNotEqual(first_user_list_url, second_user_list_url)

        page_text = self.browser.find_element('tag name', 'body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

