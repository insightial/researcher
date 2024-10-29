import unittest
import os
from langchain.docstore.document import Document
from researcher.store.vectorstore import Store
from langchain_community.vectorstores import PGEmbedding
from researcher.embeddings import Embeddings
from dotenv import load_dotenv

load_dotenv()


class TestPGEmbeddingVectorStore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connection string from environment variable
        connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        if not connection_string:
            raise EnvironmentError(
                "POSTGRES_CONNECTION_STRING is not set in the environment."
            )

        # Initialize PGEmbedding with connection string and embedding function
        embeddings = Embeddings(
            embedding_provider="openai", model="text-embedding-3-small"
        ).get_embeddings()
        cls.vector_store = PGEmbedding(
            connection_string=connection_string,
            embedding_function=embeddings,
            collection_name="test_collection",
            pre_delete_collection=True,  # Ensures a fresh test collection each time
        )

        # Sample documents for semantic similarity tests
        cls.documents = [
            {
                "raw_content": "Introduction to artificial intelligence and its applications.",
                "url": "http://example.com/doc1",
            },
            {
                "raw_content": "Deep learning models are used in natural language processing.",
                "url": "http://example.com/doc2",
            },
            {
                "raw_content": "Data science basics can enhance understanding of AI tools.",
                "url": "http://example.com/doc3",
            },
            {
                "raw_content": "Neural networks play a significant role in modern AI advancements.",
                "url": "http://example.com/doc4",
            },
            {
                "raw_content": "Cooking recipes: How to prepare a perfect Italian pasta.",
                "url": "http://example.com/doc5",
            },
            {
                "raw_content": "Travel tips for exploring beautiful destinations in Europe.",
                "url": "http://example.com/doc6",
            },
            {
                "raw_content": "Exploring the principles of quantum physics.",
                "url": "http://example.com/doc7",
            },
            {
                "raw_content": "Recent advancements in AI and machine learning applications.",
                "url": "http://example.com/doc8",
            },
            {
                "raw_content": "Different data analysis methods in machine learning.",
                "url": "http://example.com/doc9",
            },
            {
                "raw_content": "AI-driven tools are transforming industries worldwide.",
                "url": "http://example.com/doc10",
            },
        ]

        cls.query = "Applications of artificial intelligence in modern technology"

    def setUp(self):
        # Initialize Store with PGEmbedding
        self.store = Store(vector_store_type="pg", vector_store=self.vector_store)

    def test_load_documents_with_pgembedding(self):
        """Test loading documents into PGEmbedding VectorStore."""
        self.store.load(self.documents)  # Load sample documents

        # Perform a sample search to confirm documents are loaded
        loaded_docs = self.store.vector_store.similarity_search(self.query, k=5)
        self.assertGreater(len(loaded_docs), 0)

    def test_semantic_similarity_search_with_pgembedding(self):
        """Test semantic similarity search with PGEmbedding VectorStore."""
        self.store.load(self.documents)  # Load sample documents

        # Perform semantic similarity search
        results = self.store.vector_store.similarity_search(self.query, k=5)
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
