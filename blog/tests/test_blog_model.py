from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Articles

# class ModelTestCase(TestCase) : 
    
#     def setUp(self):
#         self.user = get_user_model().objects.create(email="adminTest@gmail.com", password="Moh@mm@d021")

#     def test_create_post_with_valid_data(self):
#         article = Articles.objects.create(title="post with test",
#                                           slug="test slug",
#                                           author=self.user,
#                                           status=True)
#         self.assertEqual(article.title, "post with test")