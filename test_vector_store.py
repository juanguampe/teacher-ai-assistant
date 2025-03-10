"""
Test script for Vector Store
"""

import os
from dotenv import load_dotenv
from app.utils.document_loader import ingest_documents, query_vector_store

# Load environment variables
load_dotenv()

# Vector store directory
VECTOR_STORE_DIR = os.getenv("CHROMA_DB_DIR", "./chroma_db")
DOCUMENTS_DIR = "./documents/json"

def main():
    """Main function"""
    print("Testing Vector Store...")
    
    # Create Vector Store
    print(f"\n--- Creating Vector Store ---")
    print(f"Documents directory: {os.path.abspath(DOCUMENTS_DIR)}")
    print(f"Files in documents directory: {os.listdir(DOCUMENTS_DIR)}")
    print(f"Vector Store directory: {os.path.abspath(VECTOR_STORE_DIR)}")
    
    # Create Vector Store directory if it doesn't exist
    if not os.path.exists(VECTOR_STORE_DIR):
        print(f"Creating Vector Store directory: {VECTOR_STORE_DIR}")
        os.makedirs(VECTOR_STORE_DIR)
    
    # Ingest documents
    ingest_documents(
        documents_dir=DOCUMENTS_DIR,
        persist_dir=VECTOR_STORE_DIR,
        chunk_size=1000,
        chunk_overlap=200
    )
    
    # Test query
    print(f"\n--- Testing Query ---")
    query = "¿Qué es el Paradigma Pedagógico Ignaciano?"
    print(f"Query: {query}")
    
    results = query_vector_store(query, VECTOR_STORE_DIR, num_results=2)
    
    if results:
        print(f"Found {len(results)} results")
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Source: {doc.metadata.get('file_name', 'unknown')}")
            print(f"Content: {doc.page_content[:200]}...")
    else:
        print("No results found")

if __name__ == "__main__":
    main()
