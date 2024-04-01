from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='категория')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f'{self.category_name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='цена', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')
    is_published = models.BooleanField(default=False, verbose_name='опубликовать')

    objects = models.Manager()

    def __str__(self):
        return f'{self.product_name}, Категория: {self.category}, Цена: {self.price}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('product_name',)
        permissions = [
            ('change_description', 'Can change product description'),
            ('change_category', 'Can change product category'),
            ('change_published_status', 'Can change published status')
        ]


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='продукт')
    version = models.IntegerField(verbose_name='версия')
    version_name = models.CharField(max_length=150, verbose_name='название версии')
    is_current_version = models.BooleanField(default=False, **NULLABLE, verbose_name='текущая версия')

    def __str__(self):
        return f'{self.product}: {self.version}, {self.version_name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
