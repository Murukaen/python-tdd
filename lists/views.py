from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text = request.POST.get('item_text', ''))
        return redirect('/lists/some-list')

    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
