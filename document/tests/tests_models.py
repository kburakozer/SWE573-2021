from document.models import Document
from django.test.testcases import TestCase
from document.models import Document, Tag
import requests


class Test_models(TestCase):
    def setUp(self):
        self.test_tag = Tag.objects.create(tag_name="brain")
        self.test_tag2 = Tag.objects.create(tag_name="emotion")
        self.test_tag3 = Tag.objects.create(tag_name="emotion")
        self.wiki_api = "https://www.wikidata.org/w/api.php"
        self.query = "emotion"

        doc_id = "34059051"
        title = "Iranian superwomen's career experiences: a qualitative study."
        author = ["Maryam Nosrati Beigzadeh", "Hossein Ghamari Givi", "Ali Rezaei Sharif", "Ali Sheykholeslami", "Leila Reisy, Hadi Hassankhani"]
        year = "01.06.2021"
        abstract = "Superwoman refers to the identity of a woman who performs several important roles simultaneously and full-time, such as being a wife, mother, and homemaker while holding a job."
        doi = "10.1186/s12905-021-01369-3"


        self.document = Document.objects.create(title=title, doc_id=doc_id, author=author, year=year,
                                            abstract=abstract, doi=doi
                                            )
        self.document.tags.set([self.test_tag,self.test_tag2])


    # test document str function
    def test_doc_str(self):
        
        self.assertEqual(str(self.document), "Iranian superwomen's career experiences: a qualitative study.")

    # tests tag creation
    def test_tag_str(self):
        self.assertEqual(str(self.test_tag), "brain")
        self.assertEqual(str(self.test_tag2), "emotion")

    # tests many to many relationship between document and tag
    def test_tag_doc(self):
        self.assertEqual(self.document.tags.count(), 2)

    # tests autocompletion
    def test_tag_suggestion(self):
                

        params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': self.query
        }

        self.result = requests.get(self.wiki_api, params = params)
        self.suggested_tags = []
        try:
            result_json = self.result.json()['search']
            for item in result_json:
                tag = item.get("id") + ' - ' + item.get("label") + ' - ' + item.get("description")
                self.suggested_tags.append(tag)
        except:
            pass
        self.assertGreater(len(self.suggested_tags), 0)