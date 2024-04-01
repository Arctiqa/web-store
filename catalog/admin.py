from django.contrib import admin

from catalog.models import Product, Category, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name', 'description')
    list_filter = ('category_name',)
    search_fields = ('category_name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product_name', 'description',)

    # fieldsets = (
    #     (None, {
    #         'fields': ('product_name', 'price', 'category', 'image', 'description', 'is_published')
    #     }),
    # )


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'version', 'version_name', 'is_current_version')
    list_filter = ('version_name',)
