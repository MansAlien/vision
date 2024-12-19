from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

class Command(BaseCommand):
    help = 'Generate 1000 fake users'

    def handle(self, *args, **kwargs):
        faker = Faker()
        users = []

        for _ in range(1000):
            username = faker.unique.user_name()
            email = faker.unique.email()
            password = faker.password(length=10)
            
            users.append(User(username=username, email=email))
        
        # Bulk create for better performance
        User.objects.bulk_create(users, batch_size=100)

        self.stdout.write(self.style.SUCCESS("Successfully created 1000 users!"))

