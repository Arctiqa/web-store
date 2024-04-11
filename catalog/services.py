from django.core.cache import cache

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """Проверка на наличие продуктов в кэше"""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = 'products_list'
    product = cache.get(key)
    if product is not None:
        return product
    product = Product.objects.all()
    cache.set(key, product)
    return product


def get_categories_from_cache():
    """Проверка на наличие категорий в кэше"""
    if not CACHE_ENABLED:
        return Category.objects.all()
    key = 'categories_list'
    category = cache.get(key)
    if category is not None:
        return category
    category = Category.objects.all()
    cache.set(key, category)
    return category
