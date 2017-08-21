from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class NewVisitorTest(FunctionalTest):
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

