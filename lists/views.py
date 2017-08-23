from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.models import Item, List

def home(request):
  return render(request, 'home.html')

def show_list(request, list_id):
  list_ = List.objects.get(id=list_id)
  return render(request, 'list.html', {
    'list': list_
  })

def new_list(request):
  list_ = List.objects.create()
  new_item_text = request.POST['item_text']
  item = Item(text=new_item_text, list=list_)
  try:
    item.full_clean()
    item.save()
  except ValidationError:
    list_.delete()
    error = "You can't have empty list item"
    return render(request, 'home.html', {'error': error})
  return redirect('/lists/%s/' % list_.id)

def add_item(request, list_id):
  list_ = List.objects.get(id=list_id)
  new_item_text = request.POST['item_text']
  Item.objects.create(text=new_item_text, list=list_)
  return redirect('/lists/%s/' % list_.id)
