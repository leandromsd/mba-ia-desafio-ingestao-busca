import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter

import settings
from logger import logger
from providers import BaseProvider, get_provider_choice


def ingest_pdf() -> None:
    try:
        settings.validate_environment()
        provider = get_provider_choice()

        logger.info("Starting PDF ingestion process")
        embeddings = provider.get_embeddings()
        documents = process_documents(settings.PDF_PATH)
        store_documents(documents, embeddings, provider)

        logger.info("PDF ingestion completed successfully!")

    except Exception as e:
        logger.error(f"Error during PDF ingestion: {e}")
        raise


def process_documents(pdf_path: str) -> List[Document]:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    logger.info(f"Loading PDF from: {pdf_path}")
    documents = PyPDFLoader(pdf_path).load()

    chunks = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, add_start_index=False
    ).split_documents(documents)

    if not chunks:
        raise ValueError("No document chunks were created")

    logger.info(f"Created {len(chunks)} document chunks")
    return [
        Document(
            page_content=doc.page_content,
            metadata={k: v for k, v in doc.metadata.items() if v not in ("", None)},
        )
        for doc in chunks
    ]


def store_documents(
    documents: List[Document], embeddings: Embeddings, provider: BaseProvider
) -> None:
    total_tokens = sum(provider.count_tokens(doc.page_content) for doc in documents)
    logger.info(f"Total tokens to embed (estimated): {total_tokens:,}")

    vector_store = PGVector(
        embeddings=embeddings,
        collection_name=settings.PG_VECTOR_COLLECTION_NAME,
        connection=settings.DATABASE_URL,
        use_jsonb=True,
    )

    logger.info(f"Storing {len(documents)} documents in vector database...")
    vector_store.add_documents(documents=documents)
    logger.info("Documents stored successfully.")


if __name__ == "__main__":
    ingest_pdf()
