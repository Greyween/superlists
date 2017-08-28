from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.models import Item, List
from lists.views import home
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

class HomePageTest(TestCase):
  def test_uses_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')

  def test_home_page_uses_item_form(self):
    response = self.client.get('/')
    self.assertIsInstance(response.context['form'], ItemForm)


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

  def post_invalid_input(self):
    list_ = List.objects.create()
    return self.client.post('/lists/%s/' % list_.id, 
                            data={'text': ''})

  def test_for_invalid_input_nothing_saved_to_db(self):
    self.post_invalid_input()
    self.assertEqual(Item.objects.count(), 0)

  def test_for_invalid_input_renders_list_template(self):
    response = self.post_invalid_input()
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'list.html')

  def test_for_invalid_input_passes_form_to_template(self):
    response = self.post_invalid_input()
    self.assertIsInstance(response.context['form'], ItemForm)
  
  def test_for_invalid_input_shows_error_in_page(self):
    response = self.post_invalid_input()
    self.assertContains(response, escape(EMPTY_ITEM_ERROR))

  def test_passes_correct_list_to_template(self):
    other_list = List.objects.create()
    correct_list = List.objects.create()
    response = self.client.get('/lists/%s/' % correct_list.id)
    self.assertEqual(response.context['list'], correct_list)

  def test_can_save_post_request_to_existing_list(self):
    correct_list = List.objects.create()
    other_list = List.objects.create()

    self.client.post(
      '/lists/%s/' % correct_list.id,
      data={'text': 'New item for existing list'}
    )

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'New item for existing list')
    self.assertEqual(new_item.list, correct_list)

  def test_post_redirects_to_list_view(self):
    correct_list = List.objects.create()
    other_list = List.objects.create()

    response = self.client.post(
      '/lists/%s/' % correct_list.id,
      data={'text': 'New item for existing list'}
    )

    self.assertRedirects(response, '/lists/%s/' % correct_list.id)

  def test_displays_item_form(self):
    list_ = List.objects.create()
    response = self.client.get('/lists/{}/'.format(list_.id))
    self.assertIsInstance(response.context['form'], ItemForm)
    self.assertContains(response, 'name="text"')


class NewListTest(TestCase):
  def test_can_save_post_request(self):
    response = self.client.post('/lists/new', data={'text': 'A new list item'})
    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new list item')
  
  def test_redirects_after_post(self):
    response = self.client.post('/lists/new', data={'text': 'A new list item'})
    new_list = List.objects.first()
    self.assertRedirects(response, '/lists/%s/' % new_list.id)

  def test_for_invalid_input_renders_home_template(self):
    response = self.client.post('/lists/new', data={'text': ''})
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'home.html')

  def test_validation_errors_are_shown_on_home_page(self):
    response = self.client.post('/lists/new', data={'text': ''})
    expected_error = escape(EMPTY_ITEM_ERROR)
    self.assertContains(response, expected_error)

  def test_for_invalid_input_passes_form_to_template(self):
    response = self.client.post('/lists/new', data={'text': ''})
    self.assertIsInstance(response.context['form'], ItemForm)

  def test_invalid_list_items_arent_saved(self):
    self.client.post('/lists/new', data={'text': ''})
    self.assertEqual(List.objects.count(), 0)
    self.assertEqual(Item.objects.count(), 0)
