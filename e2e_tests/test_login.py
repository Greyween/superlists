import re

from selenium.webdriver.common.keys import Keys
from django.core import mail

from .base import FunctionalTest

TEST_EMAIL = 'edith@example.com'
SUBJECT = 'Your login link for Superlists'

class LoginTest(FunctionalTest):
  def test_can_get_email_link_to_log_in(self):
    self.browser.get(self.live_server_url)
    email_field = self.browser.find_element_by_name('email')
    email_field.send_keys(TEST_EMAIL)
    email_field.send_keys(Keys.ENTER)

    self.wait_for(lambda: self.assertIn(
      'Check your email',
      self.browser.find_element_by_tag_name('body').text
    ))

    email = mail.outbox[0]
    self.assertIn(TEST_EMAIL, email.to)
    self.assertEqual(email.subject, SUBJECT)

    self.assertIn('Use this link to log in', email.body)
    url_search = re.search(r'http://.+/.+$', email.body)
    if not url_search:
      self.fail('Could not find url in email body:\n{}'.format(email.body))
    url = url_search.group(0)
    self.assertIn(self.live_server_url, url)

    self.browser.get(url)
    
    self.wait_for(
      lambda: self.browser.find_element_by_link_text('Log Out')
    )
    navbar = self.browser.find_element_by_css_selector('.navbar')
    self.assertIn(TEST_EMAIL, navbar.text)

    self.browser.find_element_by_link_text('Log Out').click()

    self.wait_for(
      lambda: self.browser.find_element_by_name('email')
    )

    navbar = self.browser.find_element_by_css_selector('.navbar')
    self.assertNotIn(TEST_EMAIL, navbar.text)
