import os
import sys
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

# Load environment variables
load_dotenv()

# Environment Configurations - Decoupled and reusable
PDF_PATH = os.getenv("PDF_PATH")
DATABASE_URL = os.getenv("DATABASE_URL")
COLLECTION_NAME = os.getenv("PG_VECTOR_COLLECTION_NAME")
EMBEDDING_MODEL = os.getenv("GOOGLE_EMBEDDING_MODEL")

def get_embeddings_client():
    """
    Factory for Google Generative AI Embeddings.
    Encapsulates model configuration for better maintainability.
    """
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        task_type="retrieval_document"
    )

def ingest_pdf():
    """
    Main ingestion pipeline. 
    Implements document loading, text splitting, and vector storage.
    """
    try:
        # 1. Document Loading
        if not os.path.exists(PDF_PATH):
            raise FileNotFoundError(f"Source PDF not found at: {PDF_PATH}")
            
        print(f"[*] Loading document: {PDF_PATH}")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()

        # 2. Text Splitting (Strategic Overlap for Context Preservation - Requirement: 1000 chars, 150 overlap)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=150
        )
        chunks = text_splitter.split_documents(documents)
        print(f"[*] Total chunks created: {len(chunks)}")

        # 3. Vector Storage via PGVector
        print(f"[*] Generating embeddings and storing in collection: {COLLECTION_NAME}")
        embeddings = get_embeddings_client()
        
        PGVector.from_documents(
            embedding=embeddings,
            documents=chunks,
            collection_name=COLLECTION_NAME,
            connection=DATABASE_URL,
            use_jsonb=True,
        )
        
        print("[+] Ingestion process completed successfully.")

    except Exception as e:
        print(f"[!] Critical error during ingestion: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    ingest_pdf()