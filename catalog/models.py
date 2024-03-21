from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name='категория')
    description = models.TextField(verbose_name='описание', **NULLABLE)

    objects = models.Manager()

    def __str__(self):
        return f'{self.category_name}: {self.description}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('category_name',)


class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name='цена', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения')

    objects = models.Manager()

    def __str__(self):
        return (f'{self.product_name} {self.description} {self.image} {self.category} {self.price} '
                f'{self.created_at} {self.updated_at}')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('product_name',)


class Version(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='продукт')
    version = models.IntegerField(verbose_name='версия')
    version_name = models.CharField(max_length=150, verbose_name='название версии')
    is_current_version = models.BooleanField(default=False, **NULLABLE, verbose_name='текущая версия')

    def __str__(self):
        return f'{self.product}: {self.version}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
