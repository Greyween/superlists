import time, unittest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorText(unittest.TestCase):
  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.close()

  def create_item(self, item):
    input_box = self.browser.find_element_by_id('new_item')
    self.assertEqual(input_box.get_attribute('placeholder'), 'To-do item')
    input_box.send_keys(item)
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

  def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])
    

  def test_can_start_a_list_and_retrieve_it_later(self):
    self.browser.get("http://localhost:8000")
    self.assertIn('To-Do', self.browser.title)
    header_text = self.browser.find_element_by_tag_name('h1').text
    self.assertIn('To-Do', header_text)
  
    self.create_item('Buy peacock feathers')
    self.check_for_row_in_list_table('1: Buy peacock feathers')

    self.create_item('Learn alchemy')
    self.check_for_row_in_list_table('2: Learn alchemy')

    self.fail('Finish the test')

if __name__ == '__main__':
  unittest.main(warnings='ignore')
