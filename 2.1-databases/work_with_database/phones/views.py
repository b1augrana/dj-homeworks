from django.shortcuts import render, redirect
from .models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort', 'name')
    if 'min_price' in sort:
        sort = 'price'
    if 'max_price' in sort:
        sort = '-price'    
    phones = Phone.objects.all().order_by(sort)    
    context = {'phones' : phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone' : phone}
    return render(request, template, context)
