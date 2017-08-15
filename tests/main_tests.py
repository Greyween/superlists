import unittest

from selenium import webdriver


class NewVisitorText(unittest.TestCase):
  def setUp(self):
    self.browser = webdriver.Firefox()

  def tearDown(self):
    self.browser.close()

  def test_can_start_a_list_and_retrieve_it_later(self):
    self.browser.get("http://localhost:8000")
    self.assertIn('To-Do', self.browser.title)
    self.fail('Finish the test')

if __name__ == '__main__':
  unittest.main(warnings='ignore')
