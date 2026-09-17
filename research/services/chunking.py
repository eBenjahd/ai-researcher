from llama_index.core.node_parser import SentenceSplitter


def split_document(text: str) -> list[str]:
    
    splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=50,
    )

    return splitter.split_text(text)