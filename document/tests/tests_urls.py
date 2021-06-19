from django.test import SimpleTestCase
from django.urls import reverse, resolve
from document.views import IndexClassView, DocDetailView, Search, Tag_view

class TestUrls(SimpleTestCase):
    def test_index_url(self):
        url = reverse('document:index')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, IndexClassView)

    def test_search_url(self):
        url = reverse('document:search_result')
        print(resolve(url))
        self.assertEqual(resolve(url).func.view_class, Search)