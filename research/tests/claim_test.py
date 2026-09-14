from django.test import TestCase
from research.models import Claim, Source, Document


class ClaimTest(TestCase):

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

        self.claim = Claim.objects.create(
            document = self.document,
            statement = "Yes it will erase the erath",
            confidence_score = 0.5
        )

    def test_can_create_claim(self):

        self.assertEqual(self.claim.id, 1)
        self.assertEqual(self.claim.statement, "Yes it will erase the erath")
        self.assertEqual(self.claim.confidence_score, 0.5)