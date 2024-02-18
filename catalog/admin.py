from django.contrib import admin

from catalog.models import Product, Category

# admin.site.register(Category, Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description',)
    list_filter = ('category_name',)
    search_fields = ('category_name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'description', 'price', 'created_at', 'updated_at',)
    list_filter = ('price',)
    search_fields = ('product_name', 'description', 'created_at', 'updated_at',)
