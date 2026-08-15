"""
Memory module - Vector database integration for Ultron Agent Kernel.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from abc import ABC, abstractmethod

from ultron.config import UltronConfig, MemoryBackend
from ultron.utils.errors import MemoryException
from ultron.utils.logger import setup_logger


class VectorStore(ABC):
    """Abstract base class for vector stores."""
    
    @abstractmethod
    def add(self, texts: List[str], metadata: List[Dict[str, Any]]) -> List[str]:
        pass
    
    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def delete(self, ids: List[str]) -> None:
        pass


class ChromaVectorStore(VectorStore):
    """Chroma vector store implementation."""
    
    def __init__(self, collection_name: str = "ultron"):
        try:
            import chromadb
            self.client = chromadb.Client()
            self.collection = self.client.get_or_create_collection(name=collection_name)
        except ImportError:
            raise MemoryException("chromadb package not installed")
    
    def add(self, texts: List[str], metadata: List[Dict[str, Any]]) -> List[str]:
        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]
        self.collection.add(documents=texts, metadatas=metadata, ids=ids)
        return ids
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        results = self.collection.query(query_texts=[query], n_results=k)
        return results
    
    def delete(self, ids: List[str]) -> None:
        self.collection.delete(ids=ids)


class Memory:
    """Memory module - Knowledge storage and retrieval."""
    
    def __init__(self, config: UltronConfig):
        self.config = config
        self.logger = setup_logger(
            "ultron.memory",
            level=config.log_level,
            log_file=config.log_file,
            enable_file_logging=config.enable_file_logging
        )
        
        self._initialize_store()
        self.embeddings_cache = {}
        self.logger.info(f"Memory initialized with {config.memory_backend.value} backend")
    
    def _initialize_store(self) -> None:
        if self.config.memory_backend == MemoryBackend.CHROMA:
            self.store = ChromaVectorStore()
        else:
            self.store = ChromaVectorStore()
    
    def remember(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        try:
            if metadata is None:
                metadata = {}
            
            metadata["timestamp"] = datetime.now().isoformat()
            
            ids = self.store.add([content], [metadata])
            self.logger.debug(f"Remembered content with ID: {ids[0]}")
            return ids[0]
        except Exception as e:
            self.logger.error(f"Failed to remember: {str(e)}")
            raise MemoryException(f"Failed to store memory: {str(e)}")
    
    def recall(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        try:
            results = self.store.search(query, k=k)
            self.logger.debug(f"Recalled {len(results)} memories for query: {query}")
            return results
        except Exception as e:
            self.logger.error(f"Failed to recall: {str(e)}")
            raise MemoryException(f"Failed to retrieve memories: {str(e)}")
    
    def forget(self, memory_ids: List[str]) -> None:
        try:
            self.store.delete(memory_ids)
            self.logger.info(f"Forgot {len(memory_ids)} memories")
        except Exception as e:
            self.logger.error(f"Failed to forget: {str(e)}")
            raise MemoryException(f"Failed to delete memories: {str(e)}")