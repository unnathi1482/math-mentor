"""
RAG Indexer - Processes knowledge base documents and stores them in ChromaDB.

This script:
1. Reads all markdown files from knowledge_base folder
2. Splits them into smaller chunks
3. Creates embeddings for each chunk
4. Stores everything in ChromaDB vector database
"""

import os
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Import our config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import CHUNK_SIZE, CHUNK_OVERLAP, CHROMA_DB_PATH


def load_documents(knowledge_base_path: str) -> list:
    """
    Load all markdown files from the knowledge base folder.
    
    Args:
        knowledge_base_path: Path to the folder containing .md files
    
    Returns:
        List of loaded documents
    """
    print(f"📂 Loading documents from: {knowledge_base_path}")
    
    loader = DirectoryLoader(
        knowledge_base_path,
        glob="**/*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    
    documents = loader.load()
    print(f"✅ Loaded {len(documents)} documents")
    
    return documents


def split_documents(documents: list) -> list:
    """
    Split documents into smaller chunks for better retrieval.
    
    Args:
        documents: List of loaded documents
    
    Returns:
        List of document chunks
    """
    print(f"✂️ Splitting documents into chunks...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n## ", "\n### ", "\n---", "\n\n", "\n", " ", ""]
    )
    
    chunks = splitter.split_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    return chunks


def create_vector_store(chunks: list, persist_directory: str) -> Chroma:
    """
    Create embeddings and store in ChromaDB.
    
    Args:
        chunks: List of document chunks
        persist_directory: Where to save the database
    
    Returns:
        ChromaDB vector store
    """
    print(f"🧠 Creating embeddings and storing in ChromaDB...")
    
    # Create embeddings using HuggingFace (free, runs locally)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Create and persist vector store
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"✅ Vector store created at: {persist_directory}")
    
    return vector_store


def build_index():
    """
    Main function to build the entire RAG index.
    Run this once to create the vector database.
    """
    # Get paths
    current_dir = Path(__file__).parent
    knowledge_base_path = current_dir / "knowledge_base"
    persist_directory = current_dir / "chroma_store"
    
    # Check if knowledge base exists
    if not knowledge_base_path.exists():
        print(f"❌ Knowledge base folder not found: {knowledge_base_path}")
        return None
    
    # Load documents
    documents = load_documents(str(knowledge_base_path))
    
    if not documents:
        print("❌ No documents found in knowledge base")
        return None
    
    # Split into chunks
    chunks = split_documents(documents)
    
    # Create vector store
    vector_store = create_vector_store(chunks, str(persist_directory))
    
    print("\n🎉 RAG Index built successfully!")
    print(f"   Documents: {len(documents)}")
    print(f"   Chunks: {len(chunks)}")
    print(f"   Location: {persist_directory}")
    
    return vector_store


def get_vector_store() -> Chroma:
    """
    Load existing vector store from disk.
    Use this when the index is already built.
    
    Returns:
        ChromaDB vector store
    """
    current_dir = Path(__file__).parent
    persist_directory = current_dir / "chroma_store"
    
    if not persist_directory.exists():
        print("⚠️ Vector store not found. Building index...")
        return build_index()
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    vector_store = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=embeddings
    )
    
    return vector_store


# Run this file directly to build the index
if __name__ == "__main__":
    print("=" * 50)
    print("🔨 Building RAG Index")
    print("=" * 50)
    build_index()