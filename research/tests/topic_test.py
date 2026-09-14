from django.test import TestCase
from research.models import Topic, DocumentTopic, Document, Source
from django.db import IntegrityError


class TopicTest(TestCase):

    def setUp(self):
        
        self.topic_1 = Topic.objects.create(
            name = "Ai will destroy accountants?",
            description = "Idk probably yes the not worthies"
        )

    def test_unique_topic(self):

        with self.assertRaises(IntegrityError):
            Topic.objects.create(
                name = "Ai will destroy accountants?",
            )


class DocumentTopicTest(TestCase):

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
        
        self.topic = Topic.objects.create(
            name = "Ai will destroying developers",
            description = "Idk probably not."
        )

        self.document_topic = DocumentTopic.objects.create(
            document = self.document,
            topic = self.topic,
            relevance_score = 0.85
        )

    def test_can_create_relation(self):

        self.assertEqual(self.document_topic.document, self.document)
        self.assertEqual(self.document_topic.topic, self.topic)
        self.assertEqual(self.document_topic.relevance_score, 0.85)

    def test_cannot_duplicate_document_topic(self):

        with self.assertRaises(IntegrityError):

            DocumentTopic.objects.create(
                document=self.document,
                topic=self.topic,
                relevance_score=0.90,
            )

    def test_ondelete_document_cascade(self):

        document_topic_id = self.document_topic.id

        self.document.delete()

        document_topic_exists = DocumentTopic.objects.filter(
            id=document_topic_id
        ).exists()

        self.assertFalse(document_topic_exists)