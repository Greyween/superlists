from django.shortcuts import redirect, render
from django.http import HttpResponse

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
  Item.objects.create(text=new_item_text, list=list_)
  return redirect('/lists/%s/' % list_.id)

def add_item(request, list_id):
  list_ = List.objects.get(id=list_id)
  new_item_text = request.POST['item_text']
  Item.objects.create(text=new_item_text, list=list_)
  return redirect('/lists/%s/' % list_.id)
