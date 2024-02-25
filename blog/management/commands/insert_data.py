from io import StringIO
import random
from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from django.contrib.auth import get_user_model
from blog.models import Category, Articles
from django.db.utils import IntegrityError
category_list = ["category_1", "category_2", "category_3"]
slug_list = ["montgomery", "davis", "george-bruce"]	
class Command(BaseCommand):
    help = "Inserting dummy data"
    
    def __init__(self, *args, **kwargs) :
        super(Command, self).__init__(*args,  **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = get_user_model().objects.create_user(email =self.fake.email() ,password ="Mm@123456" )
        
        for number, title in enumerate(category_list):
            Category.objects.get_or_create(title=title, status=True, slug = slug_list[number])

        category = Category.objects.filter(title = random.choice(category_list))
        
        for _ in range(10):
            try:
                article = Articles.objects.create(
                    title=self.fake.paragraph(nb_sentences=1),
                    description= self.fake.paragraph(nb_sentences=5),
                    slug=self.fake.domain_word(),
                    author=user,
                    status = random.choice([True, False]),
                )
                article.categories.set(category)
                article.save()
            except IntegrityError:
                continue

'''
add()  works with get()  or :
            category = Category.objects.filter(title = random.choice(category_list))
            article.categories.add(*category)
set()  works with filter()
'''


        

            