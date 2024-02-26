from django.shortcuts import render
from datetime import datetime

from catalog.models import Product, Category


def index(request):
    products = Product.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:5]

    context = {
        'object_list': products,
        'title':  'Главная',
        'latest_products': latest_products
    }

    return render(request, 'catalog/index.html',  context)


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} {name} ({phone}): {message}\n')

    context = {
        'title': 'Контакты',
    }

    return render(request, 'catalog/contacts.html', context)


def product(request, pk):

    product_item = Product.objects.get(pk=pk)

    context = {
        'product': product_item,
        'title': product_item.product_name

    }
    return render(request, 'catalog/product.html', context)
