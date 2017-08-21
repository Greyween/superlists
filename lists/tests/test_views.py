from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item, List
from lists.views import home

class HomePageTest(TestCase):
  def test_uses_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
  def test_uses_list_template(self):
    list_ = List.objects.create()
    response = self.client.get('/lists/%s/' % list_.id)
    self.assertTemplateUsed(response, 'list.html')

  def test_displays_only_items_for_that_list(self):
    correct_list = List.objects.create()
    Item.objects.create(text='Item 1', list=correct_list)
    Item.objects.create(text='Item 2', list=correct_list)

    other_list = List.objects.create()
    Item.objects.create(text='Other Item 1', list=other_list)
    Item.objects.create(text='Other Item 2', list=other_list)
    
    response = self.client.get('/lists/%s/' % correct_list.id)

    self.assertContains(response, 'Item 1')
    self.assertContains(response, 'Item 2')
    self.assertNotContains(response, 'Other Item 1')
    self.assertNotContains(response, 'Other Item 2')

  def test_passes_correct_list_to_template(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = self.client.get('/lists/%s/' % correct_list.id)
    self.assertEqual(response.context['list'], correct_list)


class NewListPost(TestCase):
  def test_can_save_post_request(self):
    response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new list item')
  
  def test_redirects_after_post(self):
    response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
    new_list = List.objects.first()
    self.assertRedirects(response, '/lists/%s/' % new_list.id)


class NewItemTest(TestCase):
  def test_can_save_post_request_to_existing_list(self):
    correct_list = List.objects.create()
    other_list = List.objects.create()

    self.client.post(
      '/lists/%s/add_item' % correct_list.id,
      data={'item_text': 'New item for existing list'}
    )

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'New item for existing list')
    self.assertEqual(new_item.list, correct_list)

  def test_redirects_to_list_view(self):
    correct_list = List.objects.create()
    other_list = List.objects.create()

    response = self.client.post(
      '/lists/%s/add_item' % correct_list.id,
      data={'item_text': 'New item for existing list'}
    )

    self.assertRedirects(response, '/lists/%s/' % correct_list.id)
