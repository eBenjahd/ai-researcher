from research.models import DocumentChunk
from .embeddings import generate_embedding


def embed_document_chunk(chunk: DocumentChunk) -> DocumentChunk:
    
    embedding = generate_embedding(chunk.content)

    chunk.embedding = embedding
    chunk.save(update_fields=["embedding"])

    return chunk