from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='Sinitro@yandex.ru',
            first_name='Roman',
            last_name='Sinitsyn',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('123456789')
        user.save()
