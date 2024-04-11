from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import MainConfig
from catalog.views import ProductListView, ProductDetailView, ContactsTemplateView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, MyProductsListView, CategoryListView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name='product'),
    path('create', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
    path('my_products/', MyProductsListView.as_view(), name='my_products'),
    path('categories/', cache_page(60)(CategoryListView.as_view()), name='categories')

]
