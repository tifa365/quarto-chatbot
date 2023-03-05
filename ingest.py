"""Load html from files, clean up, split, ingest into Weaviate."""
import pickle
import json
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from typing import List


class QuartoLoader(BaseLoader):
    """Load Quarto search.json files."""

    def __init__(self, file_path: str):
        """Initialize with file path."""
        self.file_path = file_path

    def load(self) -> List[Document]:
        """Load json from file path."""
        with open(self.file_path) as f:
            index = json.loads(f.read())
        
        docs = []
        for doc in index:
            metadata = {k: doc[k] for k in ("objectID", "href", "section")}
            docs.append(Document(page_content=doc["text"], metadata=metadata))
        return docs


def ingest_docs():
    """Get documents from web pages."""
    loader = QuartoLoader("search.json")
    raw_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(raw_documents)
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    return vectorstore


if __name__ == "__main__":
    ingest_docs()
