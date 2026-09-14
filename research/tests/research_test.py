from django.test import TestCase
from research.models import Research, ResearchDocument, Document, Source
from django.db import IntegrityError


class ResearchTest(TestCase):

    def setUp(self):
        self.research = Research.objects.create(
            question="Will AI replace software developers?",
        )

    def test_can_create_research(self):
        self.assertEqual(
            self.research.question,
            "Will AI replace software developers?"
        )

    def test_default_status_is_pending(self):
        self.assertEqual(
            self.research.status,
            "pending"
        )

    def test_completed_at_is_none_when_research_is_created(self):
        self.assertIsNone(
            self.research.completed_at
        )

    def test_can_update_research_status(self):
        self.research.status = "running"
        self.research.save()

        self.research.refresh_from_db()

        self.assertEqual(
            self.research.status,
            "running"
        )

    def test_can_complete_research(self):
        self.research.status = "completed"
        self.research.save()

        self.research.refresh_from_db()

        self.assertEqual(
            self.research.status,
            "completed"
        )

    def test_can_mark_research_as_failed(self):
        self.research.status = "failed"
        self.research.save()

        self.research.refresh_from_db()

        self.assertEqual(
            self.research.status,
            "failed"
        )

    def test_created_at_is_set_automatically(self):
        self.assertIsNotNone(
            self.research.created_at
        )


class ResearchDocumentTest(TestCase):

    def setUp(self):

        self.source = Source.objects.create(

            name="Prueba de testing con AI",

            url="https://prueba-testing.com",

            source_type="paper",

        )

        self.document = Document.objects.create(

            source=self.source,

            title="AI and Software Development",

            url="https://prueba-document1.com",

            content="AI is changing software development.",

            summary="AI impact on software developers.",

        )

        self.research = Research.objects.create(

            question="Will AI replace software developers?",

        )

        self.research_document = ResearchDocument.objects.create(

            research=self.research,

            document=self.document,

            relevance_score=0.85,

        )

    def test_can_create_research_document(self):

        self.assertEqual(

            self.research_document.research,

            self.research,

        )

        self.assertEqual(

            self.research_document.document,

            self.document,

        )

        self.assertEqual(

            self.research_document.relevance_score,

            0.85,

        )

    def test_research_can_have_many_documents(self):

        second_document = Document.objects.create(

            source=self.source,

            title="AI Research Paper",

            url="https://prueba-document2.com",

            content="Another document about AI.",

            summary="Another AI document.",

        )

        ResearchDocument.objects.create(

            research=self.research,

            document=second_document,

            relevance_score=0.90,

        )

        count_documents = self.research.research_documents.count()

        self.assertEqual(

            count_documents,

            2,

        )

    def test_document_can_belong_to_many_researches(self):

        second_research = Research.objects.create(
            question="How will AI affect the job market?",
        )

        ResearchDocument.objects.create(
            research=second_research,
            document=self.document,
            relevance_score=0.75,
        )

        count_researches = self.document.researches.count()

        self.assertEqual(count_researches, 2)

    def test_cannot_duplicate_research_document_relation(self):

        with self.assertRaises(IntegrityError):

            ResearchDocument.objects.create(
                research=self.research,
                document=self.document,
                relevance_score=0.90,
            )

    def test_relevance_score_can_be_none(self):

        second_research = Research.objects.create(
            question="How will AI affect the job market?",
        )

        research_document = ResearchDocument.objects.create(
            research=second_research,
            document=self.document,
        )

        self.assertIsNone(research_document.relevance_score)

    def test_delete_research_cascades_to_research_document(self):

        research_document_id = self.research_document.id

        self.research.delete()

        relation_exists = ResearchDocument.objects.filter(
            id=research_document_id
        ).exists()

        self.assertFalse(relation_exists)

    def test_delete_document_cascades_to_research_document(self):

        research_document_id = self.research_document.id

        self.document.delete()

        relation_exists = ResearchDocument.objects.filter(
            id=research_document_id
        ).exists()
        self.assertFalse(
            relation_exists
        )