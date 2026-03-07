"""
RAG Retriever - Searches the vector database for relevant content.

This module:
1. Takes a user query (math problem)
2. Finds the most relevant chunks from the knowledge base
3. Returns the context to help solve the problem
"""

from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Import our config
import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import TOP_K_RESULTS


class MathRetriever:
    """
    Retriever class for finding relevant math content.
    """
    
    def __init__(self):
        """Initialize the retriever with the vector store."""
        self.vector_store = None
        self.embeddings = None
        self._load_vector_store()
    
    def _load_vector_store(self):
        """Load the vector store from disk."""
        current_dir = Path(__file__).parent
        persist_directory = current_dir / "chroma_store"
        
        # Create embeddings using HuggingFace (free, runs locally)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Check if vector store exists
        if not persist_directory.exists():
            print("⚠️ Vector store not found. Please run indexer.py first.")
            self.vector_store = None
            return
        
        # Load vector store
        self.vector_store = Chroma(
            persist_directory=str(persist_directory),
            embedding_function=self.embeddings
        )
        
        print("✅ Vector store loaded successfully")
    
    def retrieve(self, query: str, top_k: int = None) -> list:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: The math problem or question
            top_k: Number of results to return (default from config)
        
        Returns:
            List of dictionaries with 'content' and 'source' keys
        """
        if self.vector_store is None:
            return []
        
        if top_k is None:
            top_k = TOP_K_RESULTS
        
        # Search the vector store
        results = self.vector_store.similarity_search_with_score(query, k=top_k)
        
        # Format results
        retrieved_docs = []
        for doc, score in results:
            retrieved_docs.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "relevance_score": round(1 - score, 3)  # Convert distance to similarity
            })
        
        return retrieved_docs
    
    def retrieve_as_context(self, query: str, top_k: int = None) -> str:
        """
        Retrieve documents and format as a single context string.
        
        Args:
            query: The math problem or question
            top_k: Number of results to return
        
        Returns:
            Formatted context string
        """
        docs = self.retrieve(query, top_k)
        
        if not docs:
            return "No relevant context found in knowledge base."
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source_name = Path(doc["source"]).stem if doc["source"] != "Unknown" else "Unknown"
            context_parts.append(
                f"--- Source {i}: {source_name} (relevance: {doc['relevance_score']}) ---\n"
                f"{doc['content']}"
            )
        
        return "\n\n".join(context_parts)
    
    def retrieve_by_topic(self, query: str, topic: str, top_k: int = None) -> list:
        """
        Retrieve documents filtered by topic.
        
        Args:
            query: The math problem or question
            topic: Topic to filter by (algebra, calculus, probability, linear_algebra)
            top_k: Number of results to return
        
        Returns:
            List of relevant documents
        """
        # First get more results than needed
        all_docs = self.retrieve(query, top_k=10)
        
        # Filter by topic
        filtered_docs = [
            doc for doc in all_docs
            if topic.lower() in doc["source"].lower()
        ]
        
        # If not enough topic-specific results, include general ones
        if len(filtered_docs) < (top_k or TOP_K_RESULTS):
            for doc in all_docs:
                if doc not in filtered_docs:
                    filtered_docs.append(doc)
                if len(filtered_docs) >= (top_k or TOP_K_RESULTS):
                    break
        
        return filtered_docs[:top_k or TOP_K_RESULTS]


def test_retriever():
    """Test the retriever with a sample query."""
    print("=" * 50)
    print("🧪 Testing RAG Retriever")
    print("=" * 50)
    
    retriever = MathRetriever()
    
    # Test queries
    test_queries = [
        "How do I solve a quadratic equation?",
        "What is the derivative of sin(x)?",
        "How do I calculate probability of two events?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        print("-" * 40)
        
        results = retriever.retrieve(query, top_k=2)
        
        if results:
            for i, doc in enumerate(results, 1):
                print(f"\n🔍 Result {i} (relevance: {doc['relevance_score']}):")
                print(f"   Source: {doc['source']}")
                print(f"   Content: {doc['content'][:200]}...")
        else:
            print("   No results found")


# Run this file directly to test the retriever
if __name__ == "__main__":
    test_retriever()