import os, time, unittest

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
  def setUp(self):
    self.browser = webdriver.Firefox()
    staging_server = os.environ.get('STAGING_SERVER')
    if staging_server:
      self.live_server_url = 'http://' + staging_server

  def tearDown(self):
    self.browser.close()

  def create_item(self, item):
    input_box = self.browser.find_element_by_id('new_item')
    self.assertEqual(input_box.get_attribute('placeholder'), 'To-do item')
    input_box.send_keys(item)
    input_box.send_keys(Keys.ENTER)

  def wait_for_row_in_list_table(self, row_text):
    start_time = time.time()
    while True:
      try:
        table = self.browser.find_element_by_id('list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        return
      except (AssertionError, WebDriverException) as e:
        if time.time() - start_time > MAX_WAIT:
          raise e
        time.sleep(0.5)

  def test_can_start_a_list_and_retrieve_it_later(self):
    self.browser.get(self.live_server_url)
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)
  
    self.create_item('Buy peacock feathers')
    self.wait_for_row_in_list_table('1: Buy peacock feathers')

    self.create_item('Learn alchemy')
    self.wait_for_row_in_list_table('2: Learn alchemy')
  
  def test_multiple_users_can_start_lists_at_different_urls(self):
    self.browser.get(self.live_server_url)
    self.create_item('Conquer the world')
    self.wait_for_row_in_list_table('1: Conquer the world')

    list_url_1 = self.browser.current_url
    self.assertRegex(list_url_1, '/lists/.+')

    self.tearDown()
    self.setUp()
    
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy peacock feathers', page_text)
    self.assertNotIn('Learn alchemy', page_text)

    self.create_item('Buy milk')
    self.wait_for_row_in_list_table('1: Buy milk')
    
    list_url_2 = self.browser.current_url
    self.assertRegex(list_url_2, '/lists/.+')
    self.assertNotEqual(list_url_1, list_url_2)

    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy peacock feather', page_text)
    self.assertIn('Buy milk', page_text)

  def test_layout_and_styling(self):
    self.browser.get(self.live_server_url)
    self.browser.set_window_size(1024, 768)
    
    input_box = self.browser.find_element_by_id('new_item')
    self.assertAlmostEqual(
      input_box.location['x'] + input_box.size['width'] / 2, 
      512, delta=10
    )

    input_box.send_keys('testing')
    input_box.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: testing')

    input_box = self.browser.find_element_by_id('new_item')
    self.assertAlmostEqual(
      input_box.location['x'] + input_box.size['width'] / 2, 
      512, delta=10
    )
    

if __name__ == '__main__':
  unittest.main(warnings='ignore')
