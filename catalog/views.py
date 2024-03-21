from django.shortcuts import render
from django.urls import reverse

from datetime import datetime

from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Version


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['title'] = product.product_name

        active_version = Version.objects.filter(product=product, is_current_version=True).order_by('-id').first()
        if active_version is None:
            context['active_version'] = 'Отсутствует'
        else:
            context['active_version'] = active_version.version

        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Главная'
        context['latest_products'] = Product.objects.order_by('-created_at')[:5]

        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:index')


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:index')


class ProductDeleteView(DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('catalog:index')


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
