from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
  @skip
  def test_cannot_add_empty_list_items(self):
    self.browser.get(self.live_server_url)

    self.browser.find_element_by_id('new_item').send_keys(Keys.ENTER)
    error_text = self.browser.find_element_by_css_selector('.has-error').text
    self.wait_for(
      lambda: self.assert_equal(
        error_text, "You can't have empty list item")
    )

    self.create_item('Buy milk')
    self.wait_for_row_in_list_table('1: Buy milk')

    self.browser.find_element_by_id('new_item').send_keys(Keys.ENTER)
    error_text = self.browser.find_element_by_css_selector('.has-error').text
    self.wait_for(
      lambda: self.assert_equal(
        error_text, "You can't have empty list item")
    )
    
    self.create_item('Make tea')
    self.wait_for_row_in_list_table('1: Buy milk')
    self.wait_for_row_in_list_table('2: Make tea')    
