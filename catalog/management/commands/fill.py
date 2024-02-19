from django.core.management import BaseCommand
import json

from catalog.models import Product, Category


class Command(BaseCommand):
    @staticmethod
    def json_read_categories():
        with open('catalog.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        categories = [i for i in data if i['model'] == 'catalog.category']

        return categories

    @staticmethod
    def json_read_products():
        with open('catalog.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        products = [i for i in data if i['model'] == 'catalog.product']

        return products

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        category_for_create = []
        product_for_create = []

        for category in Command.json_read_categories():
            cat = Category.objects.create(category_name=category['fields']['category_name'],
                                          description=category['fields']['description'])
            category_for_create.append(cat)

            old_id = category['pk']

            for product in Command.json_read_products():
                if product['fields']['category'] == old_id:
                    product_for_create.append(
                        Product(
                            product_name=product['fields']['product_name'],
                            description=product['fields']['description'],
                            category=cat,
                            image=product['fields']['image'],
                            price=product['fields']['price'],
                        )
                    )
                else:
                    continue

        Product.objects.bulk_create(product_for_create)
