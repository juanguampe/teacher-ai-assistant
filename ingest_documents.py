#!/usr/bin/env python3
"""
Document Ingestion Script for Magis XXI Educational Assistant

This script ingests JSON documents into the Vector Store (ChromaDB)
for the Teacher's AI Assistant application.
"""

import os
import argparse
from dotenv import load_dotenv
from app.utils.document_loader import ingest_documents

# Load environment variables
load_dotenv()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Ingest documents into the Vector Store (ChromaDB) for the Magis XXI Educational Assistant"
    )
    
    parser.add_argument(
        "--documents-dir",
        type=str,
        default="./documents/json",
        help="Directory containing JSON documents to ingest (default: ./documents/json)"
    )
    
    parser.add_argument(
        "--persist-dir",
        type=str,
        default=os.getenv("CHROMA_DB_DIR", "./chroma_db"),
        help="Directory to persist the vector store (default: from CHROMA_DB_DIR env var or ./chroma_db)"
    )
    
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Size of each document chunk (default: 1000)"
    )
    
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=200,
        help="Overlap between document chunks (default: 200)"
    )
    
    args = parser.parse_args()
    
    # Create documents directory if it doesn't exist
    if not os.path.exists(args.documents_dir):
        print(f"Creating documents directory: {args.documents_dir}")
        os.makedirs(args.documents_dir)
        print(f"Please add your JSON documents to {args.documents_dir} and run this script again.")
        return
    
    # Check if documents directory is empty
    if not os.listdir(args.documents_dir):
        print(f"Documents directory {args.documents_dir} is empty.")
        print(f"Please add your JSON documents to {args.documents_dir} and run this script again.")
        return
    
    # Create persist directory if it doesn't exist
    if not os.path.exists(args.persist_dir):
        print(f"Creating persist directory: {args.persist_dir}")
        os.makedirs(args.persist_dir)
    
    # Print debug information
    print(f"Documents directory: {os.path.abspath(args.documents_dir)}")
    print(f"Files in documents directory: {os.listdir(args.documents_dir)}")
    print(f"Persist directory: {os.path.abspath(args.persist_dir)}")
    
    # Ingest documents
    ingest_documents(
        documents_dir=args.documents_dir,
        persist_dir=args.persist_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    )
    
    print("\n✅ Document ingestion complete!")
    print(f"\nVector store created at: {os.path.abspath(args.persist_dir)}")
    print("\nYou can now use the AI assistant to query your documents.")

if __name__ == "__main__":
    main()
