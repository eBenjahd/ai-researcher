from django.test import TestCase
from research.models import Document, Source
from django.db import IntegrityError


class DocumentTest(TestCase):

    def setUp(self):
        
        self.source = Source.objects.create(
            name = "Prueba de testing con AI",
            url = "https://prueba-testing.com",
            source_type = "paper"
        )

        self.document = Document.objects.create(
            source = self.source,
            title = "Ai will replace developers?",
            url = "https://prueba-document1.com",
            content = "Yes asap, worry about your future!",
            summary = "Nothing is replacable"
        )

    def test_fk_relation_works(self):

        self.assertEqual(self.document.source, self.source)


    def test_source_can_have_many_document(self):

        document_data = {
            "source" : self.source,
            "title" : "Ai will replace developers?",
            "url" : "https://prueba-document2.com",
            "content" : "Yes asap, worry about your future!",
            "summary" : "Nothing is replacable"
        }

        Document.objects.create(**document_data)

        count_documents = self.source.documents.count()

        self.assertEqual(count_documents, 2)

    def test_cannot_register_duplicated_urls(self):

        repeated_url = {
            "source" : self.source,
            "title" : "Ai will replace developers?",
            "url" : "https://prueba-document1.com",
            "content" : "Yes asap, worry about your future!",
            "summary" : "Nothing is replacable"
        }

        with self.assertRaises(IntegrityError):

            Document.objects.create(**repeated_url)

    def test_ondelete_cascade(self):

        source_id = self.source.id

        count_before = self.source.documents.count()
        
        self.source.delete()

        count_after = Document.objects.filter(source_id=source_id).count()

        self.assertEqual(count_before, 1)
        self.assertEqual(count_after, 0)

