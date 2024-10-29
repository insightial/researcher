import unittest
from langchain.docstore.document import Document
from researcher.store.vectorstore import Store  # Adjust based on actual path


class TestDefaultVectorStore(unittest.TestCase):

    def setUp(self):
        # Sample documents with semantically diverse content
        self.documents = [
            {
                "raw_content": "This is an introduction to machine learning and artificial intelligence.",
                "url": "http://example.com/doc1",
            },
            {
                "raw_content": "Deep learning techniques are used to process natural language.",
                "url": "http://example.com/doc2",
            },
            {
                "raw_content": "Understanding the basics of data science can help you leverage AI tools effectively.",
                "url": "http://example.com/doc3",
            },
            {
                "raw_content": "This document discusses the importance of neural networks in modern AI applications.",
                "url": "http://example.com/doc4",
            },
            {
                "raw_content": "Cooking recipes: How to make a delicious pasta dish.",
                "url": "http://example.com/doc5",
            },
            {
                "raw_content": "Travel guide: Top destinations to visit in Europe this summer.",
                "url": "http://example.com/doc6",
            },
            {
                "raw_content": "Quantum physics explores the fundamental principles of particles and waves.",
                "url": "http://example.com/doc7",
            },
            {
                "raw_content": "An analysis of recent advancements in artificial intelligence and its applications.",
                "url": "http://example.com/doc8",
            },
            {
                "raw_content": "Exploring data analysis methods in AI and machine learning.",
                "url": "http://example.com/doc9",
            },
            {
                "raw_content": "AI-driven language models are transforming how we process and generate text.",
                "url": "http://example.com/doc10",
            },
        ]

        # Query focused on artificial intelligence and its applications
        self.query = "Applications of artificial intelligence in modern technology"

    def test_initialization_with_default_vector_store(self):
        """Test Store initializes with default VectorStore if no vector_store is provided."""
        store = Store()  # Initialize without passing a vector_store
        store.load(self.documents)  # Call load to initialize FAISS
        self.assertIsNotNone(store.vector_store)  # Verify vector store is initialized

    def test_load_documents_with_default_vector_store(self):
        """Test loading documents into the default VectorStore."""
        store = Store()
        store.load(self.documents)  # Load sample documents

        # Check if documents are loaded by performing a similarity search
        loaded_docs = store.vector_store.similarity_search(self.query, k=5)
        self.assertGreater(len(loaded_docs), 0)

    def test_semantic_similarity_search_with_default_vector_store(self):
        """Test semantic similarity search with default VectorStore."""
        store = Store()
        store.load(self.documents)  # Load sample documents

        # Perform similarity search
        results = store.vector_store.similarity_search(self.query, k=5)
        self.assertIsInstance(results, list)
        self.assertGreaterEqual(len(results), 1)

        # Expected documents that are semantically related to AI
        expected_urls = {
            "http://example.com/doc1",
            "http://example.com/doc2",
            "http://example.com/doc4",
            "http://example.com/doc8",
            "http://example.com/doc9",
            "http://example.com/doc10",
        }

        # Check that returned documents are semantically relevant
        for result in results:
            self.assertIsInstance(result, Document)
            source = result.metadata.get("source")
            if source:
                self.assertIn(source, expected_urls)


if __name__ == "__main__":
    unittest.main()
