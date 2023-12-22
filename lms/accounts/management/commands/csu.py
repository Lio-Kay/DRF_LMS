from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):

        user = User.objects.create_superuser(
            email='admin@admin.com',
            first_name='Admin',
            last_name='Admin',
            phone='+1234567890',
        )
        user.set_password('1234')
        user.save()