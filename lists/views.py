from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm

def home(request):
  form = ItemForm()
  return render(request, 'home.html', {'form': form})

def show_list(request, list_id):
  list_ = List.objects.get(id=list_id)
  form = ItemForm()
  if request.method == 'POST':
    form = ItemForm(data=request.POST)
    if form.is_valid():
      item_text = request.POST['text']
      Item.objects.create(text=item_text, list=list_)
      return redirect(list_)
  return render(request, 'list.html', {
    'list': list_,
    'form': form
  })

def new_list(request):
  form = ItemForm(data=request.POST)
  if form.is_valid():
    list_ = List.objects.create()
    new_item_text = request.POST['text']
    item = Item.objects.create(text=new_item_text, list=list_)
    return redirect(list_)
  return render(request, 'home.html', {'form': form})
  
