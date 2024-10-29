from typing import List, Dict, Union, Optional
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS, PGEmbedding
from langchain.text_splitter import RecursiveCharacterTextSplitter
from researcher.embeddings import Embeddings


class Store:
    """
    A Wrapper for Langchain VectorStore and PGEmbedding to handle GPT-Researcher Document Type.
    If no vector_store is provided, a default FAISS VectorStore will be created lazily in load method.
    """

    def __init__(
        self,
        vector_store_type: str = "default",
        vector_store: Optional[Union[FAISS, PGEmbedding]] = None,
    ):
        self.vector_store_type = vector_store_type
        self.vector_store = vector_store
        self.embeddings = Embeddings(
            embedding_provider="openai", model="text-embedding-3-small"
        ).get_embeddings()

    def load(self, documents: List[Dict[str, str]]):
        """
        Load documents into the vector store.
        Translates to Langchain document type, splits to chunks, then loads.
        """
        langchain_documents = self._create_langchain_documents(documents)
        splitted_documents = self._split_documents(langchain_documents)

        # Lazily initialize FAISS if vector_store is None
        if self.vector_store is None:
            texts = [doc.page_content for doc in splitted_documents]
            metadatas = [doc.metadata for doc in splitted_documents]
            self.vector_store = FAISS.from_texts(
                texts=texts, embedding=self.embeddings, metadatas=metadatas
            )
        elif isinstance(self.vector_store, PGEmbedding):
            texts = [doc.page_content for doc in splitted_documents]
            metadatas = [doc.metadata for doc in splitted_documents]
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
        else:
            self.vector_store.add_documents(splitted_documents)

    def _create_langchain_documents(self, data: List[Dict[str, str]]) -> List[Document]:
        """Convert GPT Researcher Document to Langchain Document format."""
        return [
            Document(page_content=item["raw_content"], metadata={"source": item["url"]})
            for item in data
        ]

    def _split_documents(
        self,
        documents: List[Document],
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ) -> List[Document]:
        """
        Split documents into smaller chunks for more efficient vector storage.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        return text_splitter.split_documents(documents)

    async def asimilarity_search(
        self, query: str, k: int = 4, filter: Optional[dict] = None
    ):
        """
        Perform similarity search. Handles both PGEmbedding and default VectorStore types.
        """
        if isinstance(self.vector_store, PGEmbedding):
            results = await self.vector_store.similarity_search_with_score(
                query=query, k=k, filter=filter
            )
        else:
            results = self.vector_store.similarity_search(
                query=query, k=k, filter=filter
            )

        return results
