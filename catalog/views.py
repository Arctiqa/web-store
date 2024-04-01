from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.urls import reverse

from datetime import datetime

from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_success_url(self):
        return reverse('catalog:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        version_form = context_data['formset']
        self.object = form.save()
        if version_form.is_valid():
            version_form.instance = self.object
            version_form.save()
        return super().form_valid(form)

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user or user.is_superuser:
            return ProductForm
        elif user.has_perm('catalog.change_description') and user.has_perm('catalog.change_category'):
            return ProductModeratorForm
        raise Http404


class ProductDeleteView(LoginRequiredMixin, DeleteView):
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


class MyProductsListView(ListView):
    model = Product
    template_name = 'catalog/my_product_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Мои продукты'
        products = context['object_list']

        for product in products:
            current_version = product.version_set.filter(is_current_version=True).order_by('-id').first()
            product.current_version = current_version

            if current_version is None:
                continue
            else:
                product.version = current_version.version
                product.version_name = product.current_version.version_name

        return context

    def get_queryset(self):

        user = self.request.user
        queryset = Product.objects.filter(owner=user)
        return queryset
