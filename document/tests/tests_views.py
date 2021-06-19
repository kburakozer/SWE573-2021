from django.test import TestCase, Client
from django.urls import reverse
from document.models import Document, Tag
import json


class Test_views(TestCase):

    def setUp(self):
        self.client = Client()
        self.index_url = reverse('document:index')
        self.search_url = reverse('document:search_result')
        self.detail_url = reverse('document:detail', args=[1])

        # create a document to test detail view
        self.document1 = Document.objects.create(pk=1, doc_id = 123)
        self.tag_url = reverse('document:tag', args=[1])

    def test_check_homepage(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='document/document.html')

    def test_check_search(self):
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='document/search_result.html')

    def test_check_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,template_name='document/detail.html')

    def test_check_tag_post(self):
        response = self.client.post(self.tag_url, {
            'pk':1,
            'tag_name' : "amygdala"
        })

        self.assertEqual(response.status_code, 302 )
        #self.assertEqual(self.document1.tags.first().tag_name, 'amygdala')



