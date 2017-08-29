from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
  def test_cannot_add_empty_list_items(self):
    self.browser.get(self.live_server_url)

    self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)
    self.wait_for(lambda: self.browser.find_element_by_css_selector(
      '#id_text:invalid')
    )

    self.create_item('Buy milk')
    self.wait_for(lambda: self.browser.find_element_by_css_selector(
      '#id_text:valid')
    )
    self.wait_for_row_in_list_table('1: Buy milk')

    self.browser.find_element_by_id('id_text').send_keys(Keys.ENTER)
    self.wait_for(lambda: self.browser.find_element_by_css_selector(
      '#id_text:invalid')
    )
    
    self.create_item('Make tea')
    self.wait_for_row_in_list_table('1: Buy milk')
    self.wait_for_row_in_list_table('2: Make tea')

  def test_cannot_add_duplicate_items(self):
    self.browser.get(self.live_server_url)
    self.create_item('Buy wellies')
    self.wait_for_row_in_list_table('1: Buy wellies')

    self.create_item('Buy wellies')
    
    self.wait_for(lambda: self.assertEqual(
      self.browser.find_element_by_css_selector('.has-error').text,
      "You've already got this in your list"
    ))    
