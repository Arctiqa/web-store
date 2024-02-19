from django.shortcuts import render
from datetime import datetime

from catalog.models import Product


def index(request):
    latest_products = Product.objects.order_by('-created_at')[:5]

    return render(request, 'catalog/index.html',  {'latest_products': latest_products})


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} {name} ({phone}): {message}\n')

    return render(request, 'catalog/contacts.html')
