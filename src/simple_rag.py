import json
import os
import numpy as np
from typing import Dict, List
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class SimpleRAG:
    def __init__(self, knowledge_base_path: str = "data/mock_docs.json"):
        """Initialize simple RAG system"""
        self.knowledge_base_path = knowledge_base_path
        self.model = None
        self.knowledge_base = {}
        self.document_embeddings = {}
        self.documents_list = {}
        
        self._initialize()
    
    def _initialize(self):
        """Initialize model and load knowledge base"""
        try:
            print("🤖 Loading sentence transformer model...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("✅ Model loaded successfully")
            
            self._load_knowledge_base()
            self._create_embeddings()
            
        except Exception as e:
            print(f"❌ Error initializing RAG: {e}")
            self.model = None
    
    def _load_knowledge_base(self):
        """Load knowledge base from JSON"""
        if not os.path.exists(self.knowledge_base_path):
            print(f"❌ Knowledge base not found: {self.knowledge_base_path}")
            return
        
        try:
            with open(self.knowledge_base_path, 'r') as f:
                self.knowledge_base = json.load(f)
            print(f"✅ Loaded knowledge base: {list(self.knowledge_base.keys())}")
        except Exception as e:
            print(f"❌ Error loading knowledge base: {e}")
    
    def _create_embeddings(self):
        """Create embeddings for all documents"""
        if not self.model or not self.knowledge_base:
            return
        
        try:
            print("🔄 Creating embeddings...")
            for category, documents in self.knowledge_base.items():
                if documents:
                    embeddings = self.model.encode(documents)
                    self.document_embeddings[category] = embeddings
                    self.documents_list[category] = documents
                    print(f"✅ {category}: {len(documents)} documents")
        except Exception as e:
            print(f"❌ Error creating embeddings: {e}")
    
    def retrieve_documents(self, query: str, category: str, top_k: int = 3) -> List[Dict]:
        """Retrieve relevant documents"""
        if not self.model:
            return []
        
        # Convert category to lowercase for matching
        category_lower = category.lower()
        
        # Try exact match first, then partial match
        matched_category = None
        for cat in self.document_embeddings.keys():
            if cat.lower() == category_lower:
                matched_category = cat
                break
            elif category_lower in cat.lower() or cat.lower() in category_lower:
                matched_category = cat
                break
        
        if not matched_category:
            print(f"❌ Category '{category}' not found")
            return []
        
        try:
            query_embedding = self.model.encode([query])
            doc_embeddings = self.document_embeddings[matched_category]
            documents = self.documents_list[matched_category]
            
            similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum threshold
                    results.append({
                        'content': documents[idx],
                        'similarity': float(similarities[idx]),
                        'category': matched_category
                    })
            
            print(f"🔍 Found {len(results)} documents for '{query}' in {matched_category}")
            return results
            
        except Exception as e:
            print(f"❌ Retrieval error: {e}")
            return []
    
    def format_context(self, retrieved_docs: List[Dict], query: str) -> str:
        """Format retrieved documents as context"""
        if not retrieved_docs:
            return f"No relevant documentation found for: '{query}'"
        
        context_parts = [
            "=== RELEVANT KNOWLEDGE BASE ===",
            f"Query: {query}",
            ""
        ]
        
        for doc in retrieved_docs:
            similarity_pct = doc['similarity'] * 100
            context_parts.extend([
                f"[{doc['category'].upper()} - {similarity_pct:.1f}% relevant]",
                doc['content'],
                ""
            ])
        
        context_parts.append("=== END KNOWLEDGE BASE ===")
        return "\n".join(context_parts)

# Global instance
_rag_instance = None

def get_rag_system():
    global _rag_instance
    if _rag_instance is None:
        _rag_instance = SimpleRAG()
    return _rag_instance