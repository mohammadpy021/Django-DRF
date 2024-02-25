from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Articles
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
# class ViewTestCase(TestCase):

#     def setUp(self):
#         self.client = Client()
        # self.user = get_user_model().objects.create(email="adminTest@gmail.com", password=make_password("Moh@mm@d021"))
#         self.article = Articles.objects.create(title="post with test",
#                                           slug="test slug",
#                                           author=self.user,
#                                           status=True)

#     def test_blog_index_url_successful(self):
#         response = self.client.get(reverse('blog:article-list'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'blog/articles_list.html')

#     def test_blog_index_loggedin_response(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('blog:article-detail', kwargs= {'pk' : self.article.pk}))
#         self.assertEqual(response.status_code, 200)

#     def test_blog_index_anonymous_response(self):
#         response = self.client.get(reverse('blog:article-detail', kwargs= {'pk' : self.article.pk}))
        # self.assertEqual(response.status_code, 302)


   
