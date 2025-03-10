"""
Document Loader Utility for Step 2

This script is used to load documents into the Vector Store (ChromaDB)
for the Teacher's AI Assistant application.
"""

import os
import json
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    UnstructuredExcelLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.document_loaders.base import BaseLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

# Load environment variables
load_dotenv()

# Define document loaders for different file types
LOADER_MAPPING = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".xls": UnstructuredExcelLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".doc": UnstructuredWordDocumentLoader,
}

class JSONLoader(BaseLoader):
    """Custom loader for JSON files"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load(self) -> List[Document]:
        """Load and process JSON file"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        documents = []
        
        # Process the JSON data based on its structure
        # Assuming the JSON contains an array of objects with text content
        if isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    # Extract text content from the item
                    # Adjust this based on your JSON structure
                    content = self._extract_text_from_dict(item)
                    if content:
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": self.file_path,
                                "index": i,
                                "file_name": os.path.basename(self.file_path)
                            }
                        )
                        documents.append(doc)
        elif isinstance(data, dict):
            # If the JSON is a single object
            content = self._extract_text_from_dict(data)
            if content:
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": self.file_path,
                        "file_name": os.path.basename(self.file_path)
                    }
                )
                documents.append(doc)
        
        return documents
    
    def _extract_text_from_dict(self, item: Dict[str, Any]) -> str:
        """Extract text content from a dictionary"""
        # Adjust this method based on your JSON structure
        texts = []
        
        # Recursively extract text from nested dictionaries and lists
        for key, value in item.items():
            if isinstance(value, str):
                texts.append(f"{key}: {value}")
            elif isinstance(value, (int, float, bool)):
                texts.append(f"{key}: {str(value)}")
            elif isinstance(value, dict):
                nested_text = self._extract_text_from_dict(value)
                if nested_text:
                    texts.append(f"{key}: {nested_text}")
            elif isinstance(value, list):
                for i, list_item in enumerate(value):
                    if isinstance(list_item, str):
                        texts.append(f"{key}[{i}]: {list_item}")
                    elif isinstance(list_item, dict):
                        nested_text = self._extract_text_from_dict(list_item)
                        if nested_text:
                            texts.append(f"{key}[{i}]: {nested_text}")
        
        return "\n".join(texts)

# Add JSON loader to the mapping
LOADER_MAPPING[".json"] = JSONLoader

def load_documents(directory_path: str) -> List[Document]:
    """
    Load documents from a directory
    
    Args:
        directory_path: Path to the directory containing documents
        
    Returns:
        List of loaded documents
    """
    documents = []
    
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"Directory {directory_path} does not exist.")
        return documents
    
    # Walk through directory
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1].lower()
            
            # Skip files with unsupported extensions
            if file_extension not in LOADER_MAPPING:
                continue
            
            # Load document using appropriate loader
            loader_class = LOADER_MAPPING[file_extension]
            try:
                loader = loader_class(file_path)
                documents.extend(loader.load())
                print(f"Loaded {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
    
    return documents

def split_documents(documents: List[Document], chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Split documents into chunks
    
    Args:
        documents: List of documents to split
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of document chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    
    return text_splitter.split_documents(documents)

def create_openai_embeddings():
    """
    Create OpenAI embeddings with direct API access
    
    Returns:
        OpenAI embeddings
    """
    import requests
    from langchain_core.embeddings import Embeddings
    
    class DirectOpenAIEmbeddings(Embeddings):
        """OpenAI embeddings using direct API access"""
        
        def __init__(self, api_key=None):
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key is required")
        
        def embed_documents(self, texts):
            """Embed documents using OpenAI API"""
            results = []
            # Process in batches to avoid API limits
            batch_size = 16
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                batch_results = self._embed_batch(batch)
                results.extend(batch_results)
            return results
        
        def embed_query(self, text):
            """Embed query using OpenAI API"""
            return self._embed_batch([text])[0]
        
        def _embed_batch(self, texts):
            """Embed a batch of texts using OpenAI API"""
            url = "https://api.openai.com/v1/embeddings"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            data = {
                "model": "text-embedding-ada-002",
                "input": texts
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            return [item["embedding"] for item in result["data"]]
    
    return DirectOpenAIEmbeddings()

def create_vector_store(documents: List[Document], persist_directory: Optional[str] = None) -> Chroma:
    """
    Create a vector store from documents
    
    Args:
        documents: List of documents to add to the vector store
        persist_directory: Directory to persist the vector store
        
    Returns:
        Chroma vector store
    """
    # Get embeddings using direct API access
    embeddings = create_openai_embeddings()
    
    # Create vector store
    if persist_directory:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        # Persist the vector store
        vector_store.persist()
    else:
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=embeddings
        )
    
    return vector_store

def get_vector_store(persist_directory: str) -> Optional[Chroma]:
    """
    Get an existing vector store
    
    Args:
        persist_directory: Directory where the vector store is persisted
        
    Returns:
        Chroma vector store or None if it doesn't exist
    """
    if not os.path.exists(persist_directory):
        return None
    
    try:
        # Get embeddings using direct API access
        embeddings = create_openai_embeddings()
        
        # Load the vector store
        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
        
        return vector_store
    except Exception as e:
        print(f"Error loading vector store: {str(e)}")
        return None

def query_vector_store(query: str, persist_directory: str, num_results: int = 5) -> List[Document]:
    """
    Query the vector store for relevant documents
    
    Args:
        query: The query string
        persist_directory: Directory where the vector store is persisted
        num_results: Number of results to return
        
    Returns:
        List of relevant documents
    """
    vector_store = get_vector_store(persist_directory)
    if not vector_store:
        print(f"Vector store not found at {persist_directory}")
        return []
    
    try:
        # Query the vector store
        results = vector_store.similarity_search(query, k=num_results)
        return results
    except Exception as e:
        print(f"Error querying vector store: {str(e)}")
        return []

def ingest_documents(documents_dir: str, persist_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> None:
    """
    Ingest documents into the vector store
    
    Args:
        documents_dir: Directory containing documents to ingest
        persist_dir: Directory to persist the vector store
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
    """
    print(f"Loading documents from {documents_dir}...")
    documents = load_documents(documents_dir)
    
    if not documents:
        print("No documents found.")
        return
    
    print(f"Loaded {len(documents)} documents.")
    
    print("Splitting documents into chunks...")
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    print(f"Split into {len(chunks)} chunks.")
    
    print("Creating vector store...")
    create_vector_store(chunks, persist_dir)
    print(f"Vector store created and persisted to {persist_dir}.")

if __name__ == "__main__":
    # Example usage:
    # ingest_documents("./documents/json", "./chroma_db")
    pass
