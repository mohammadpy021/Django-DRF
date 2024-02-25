from django.test import TestCase
from django.urls import reverse, resolve
from blog.views import ArticleListView

# class URLTestCase(TestCase):

#     def test_blog_index_url_resolve(self):
#         url = reverse('blog:article-list')
#         self.assertEqual(resolve(url).func.view_class, ArticleListView)


