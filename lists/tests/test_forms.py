from django.test import TestCase

from lists.models import List, Item
from lists.forms import ItemForm, EMPTY_ITEM_ERROR


class ItemFormTest(TestCase):
  def test_form_renders_item_text_input(self):
    form = ItemForm()
    self.assertIn('placeholder="To-Do Item"', form.as_p())
    self.assertIn('class="form-control input-lg"', form.as_p())

  def test_form_validation_for_blank_items(self):
    form = ItemForm(data={'text': ''})
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

  def test_form_save_handles_saving_to_list(self):
    list_ = List.objects.create()
    form = ItemForm(data={'text': 'make me'})
    new_item = form.save(for_list=list_)
    self.assertEqual(new_item, Item.objects.first())
    self.assertEqual(new_item.text, 'make me')
    self.assertEqual(new_item.list, list_)