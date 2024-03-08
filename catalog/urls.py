from django.urls import path

from catalog.apps import MainConfig
from catalog.views import IndexListView, ProductDetailView, ContactsTemplateView

app_name = MainConfig.name

urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product')

]
