from django.shortcuts import redirect, render
from django.http import HttpResponse

from lists.models import Item

def home(request):
  items = Item.objects.all()
  if request.method == 'POST':
    new_item_text = request.POST['item_text']
    Item.objects.create(text=new_item_text)
    return redirect('/')

  return render(request, 'home.html', {
    'items': items
  })
