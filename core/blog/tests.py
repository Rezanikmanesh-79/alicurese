from django.test import TestCase
from django.urls import reverse, resolve
from blog.views import PostlistView


class UrlsTest(TestCase):

    def test_blog_post_list_url_resolves(self):
        url = reverse("blog:post-list")
        resolver = resolve(url)
        self.assertEqual(resolver.func.view_class, PostlistView)
