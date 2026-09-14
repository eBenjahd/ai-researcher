from django.test import TestCase
from research.models import Source
from django.db import IntegrityError


class SourceTest(TestCase):

    def setUp(self):
        
        self.source = Source.objects.create(
            name = "Prueba de testing con AI",
            url = "https://prueba-testing.com",
            source_type = "paper"
        )

    def test_source_is_created_correctly(self):

        self.assertEqual(self.source.name, "Prueba de testing con AI")
        self.assertEqual(self.source.url, "https://prueba-testing.com")
        self.assertEqual(self.source.source_type, "paper")

    def test_cannot_create_duplicated_url(self):

        repetead_source_data = {
            "name" : "Prueba de testing con AI 2",
            "url" : "https://prueba-testing.com",
            "source_type" : "news",
        }

        with self.assertRaises(IntegrityError):
            data = Source.objects.create(**repetead_source_data)
            