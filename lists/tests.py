from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item
from lists.views import home

class HomePageTest(TestCase):
  def test_uses_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')

  def test_can_save_post_request(self):
    response = self.client.post('/', data={ 'item_text': 'A new list item' })
    self.assertIn('A new list item', response.content.decode())
    self.assertTemplateUsed(response, 'home.html')

class ItemModelTest(TestCase):
  def test_saving_and_retrieving_items(self):
    first_item = Item()
    first_item.text = 'First list item'
    first_item.save()

    second_item = Item()
    second_item.text = 'Second list item'
    second_item.save()

    saved_items = Item.objects.all()
    self.assertEqual(saved_items.count(), 2)
    first_saved_item = saved_items[0]
    second_saved_item = saved_items[1]
    self.assertEqual(first_saved_item.text, 'First list item')
    self.assertEqual(second_saved_item.text, 'Second list item')