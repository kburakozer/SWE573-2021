# from django.test import TestCase, Client, SimpleTestCase
# from django.urls import reverse, resolve
# from document.views import DocDetailView, Search, Tag_view, register
# from document.models import Tag, Document
# from document.services import*
# import json

# # Create your tests here.

# #basic url request test
# class Test_url(TestCase):
#     def test_check_homepage(self):
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)
#     def test_check_search(self):
#         response = self.client.get('/search/')
#         self.assertEqual(response.status_code, 200)


# class viewTests(TestCase):

#     def test_detail_view(self):
#         self.client = Client()
#         response = self.client.get('/')
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, 'document/search_result.html')
    
    # def test_search_view(self):
    #     response = self.client.get(reverse('/search/'))
    #     self.assertEqual(response.status_code, 200)

    # def test_tag_view(self):
    #     response = self.client.get('/tag/')
    #     self.assertEqual(response.status_code, 200)





# class modelTests(TestCase):

#     # tests document creation
#     def setUp(self):
#         self.test_tag = Tag.objects.create(tag_name="brain")
#         self.test_tag2 = Tag.objects.create(tag_name="emotion")

#         doc_id = "34059051"
#         title = "Iranian superwomen's career experiences: a qualitative study."
#         author = ["Maryam Nosrati Beigzadeh", "Hossein Ghamari Givi", "Ali Rezaei Sharif", "Ali Sheykholeslami", "Leila Reisy, Hadi Hassankhani"]
#         year = "01.06.2021"st name "db
#         abstract = "Superwoman refers to the identity of a woman who performs several important roles simultaneously and full-time, such as being a wife, mother, and homemaker while holding a job."
#         doi = "10.1186/s12905-021-01369-3"


#         self.title = Document.objects.create(title=title, doc_id=doc_id, author=author, year=year,
#                                             abstract=abstract, doi=doi
#                                             )
#         self.title.tags.set([self.test_tag,self.test_tag2])

#     # test document str function
#     def test_doc_str(self):
#         self.assertEqual(str(self.title), "Iranian superwomen's career experiences: a qualitative study.")

#     # tests tag creation
#     def test_tag_str(self):
#         self.assertEqual(str(self.test_tag), "brain")
#         self.assertEqual(str(self.test_tag2), "emotion")

#     # tests many to many relationship between document and tag
#     def test_tag_doc(self):
#         self.assertEqual(self.title.tags.count(), 2)


# class serviceTest(TestCase):
