# utils/document_loader.py

import logging
from typing import List
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    UnstructuredCSVLoader,
    UnstructuredExcelLoader,
    UnstructuredMarkdownLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

logger = logging.getLogger(__name__)


class DocumentLoader:
    def __init__(self, path: str, source: str):
        """
        Initializes the DocumentLoader with a file path and source URL.
        :param path: Path of the file to load.
        :param source: The source URL or identifier of the file for metadata.
        """
        self.path = path
        self.source = source

    async def load(self) -> List[dict]:
        """
        Asynchronously loads documents from the given file path.
        :return: A list of loaded documents with content and metadata.
        """
        file_extension = self.path.split(".")[-1].lower()
        logger.info(f"Loading document with extension: {file_extension}")

        documents = await self._load_document(file_extension)

        docs = []
        for page in documents:
            if page.page_content:
                docs.append(
                    {
                        "raw_content": page.page_content,
                        "url": self.source,
                    }
                )

        if not docs:
            logger.error("No content was loaded from the document.")
            raise ValueError("🤷 Failed to load any documents!")

        return docs

    async def _load_document(self, file_extension: str) -> list:
        """
        Helper method to load a document based on its file extension.
        :param file_extension: Extension of the document file.
        :return: A list of document pages.
        """
        loader_dict = {
            "pdf": PyMuPDFLoader,
            "txt": TextLoader,
            "doc": UnstructuredWordDocumentLoader,
            "docx": UnstructuredWordDocumentLoader,
            "pptx": UnstructuredPowerPointLoader,
            "csv": UnstructuredCSVLoader,
            "xls": UnstructuredExcelLoader,
            "xlsx": UnstructuredExcelLoader,
            "md": UnstructuredMarkdownLoader,
        }

        loader_class = loader_dict.get(file_extension)
        if loader_class is None:
            raise ValueError(f"Unsupported file extension: {file_extension}")

        logger.info(
            f"Using loader {loader_class.__name__} for file extension: {file_extension}"
        )

        # Load content from the file path
        try:
            loader = loader_class(self.path)
            documents = loader.load()
            if not documents:
                logger.error("Loader returned no documents.")
            return documents
        except Exception as e:
            logger.error(
                f"Failed to load document {self.path} with loader {loader_class.__name__}: {e}"
            )
            raise ValueError(f"Failed to load document: {e}")
