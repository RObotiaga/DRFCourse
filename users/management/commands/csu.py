from django.core.management import BaseCommand

from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = CustomUser.objects.create(
            user_id=936853523,
            is_staff=True,
            is_superuser=True
        )

        user.set_password('Canavakill1')
        user.save()
