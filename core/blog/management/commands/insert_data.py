from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from blog.models import Post, Catgory
import random
from datetime import datetime

class Command(BaseCommand):
    help = "Inserting fake data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        catgory_names = ['fun', 'it', 'ict']

        # Create user
        user = User.objects.create_user(
            email=self.fake.email(),
            password="1234567@65421"
        )

        # Create profile
        profile = Profile(user=user)
        profile.name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.save()

        # Create or get categories
        categories = []
        for name in catgory_names:
            category, _ = Catgory.objects.get_or_create(name=name)
            categories.append(category)

        # Create fake posts
        for _ in range(10):
            Post.objects.create(
                author=profile,
                title=self.fake.paragraph(nb_sentences=1),
                content=self.fake.paragraph(nb_sentences=10),
                status=random.choice([True, False]),
                catgory=random.choice(categories),
                published_date=datetime.now()
            )

        self.stdout.write(self.style.SUCCESS("Fake user, profile, categories and posts created successfully."))
