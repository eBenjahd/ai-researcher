from .chunking import split_document
from research.models import DocumentChunk


def create_document_chunks(document):
    chunks = split_document(document.content)

    document_chunks = []

    for index, chunk in enumerate(chunks):
        document_chunks.append(
            DocumentChunk(
                document=document,
                content=chunk,
                chunk_index=index,
            )
        )

    DocumentChunk.objects.bulk_create(document_chunks)

    return document_chunks