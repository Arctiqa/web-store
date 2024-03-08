from django.shortcuts import render
from datetime import datetime

from django.views.generic import ListView, DetailView, TemplateView

from catalog.models import Product, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['title'] = product.product_name
        return context


class IndexListView(ListView):
    model = Product
    template_name = 'catalog/index.html'
    context_object_name = 'object_list'
    extra_context = {
        'title': 'Главная',
        'latest_products': Product.objects.order_by('-created_at')[:5]
    }


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{datetime.now()} {name} ({phone}): {message}\n')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Контакты'
        return context


