"""Text embedder class"""
import os
from typing import Callable, Type
import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from knowledge_base.document_reader_interface import DocumentReaderInterface
from dotenv import load_dotenv
class OpenAITextEmbedder:
    "Text embedder class"

    def __init__(
            self,
            deployment: str,
    ) -> None:
        """Text embedder constructor

        :param deployment: OpenAI deployment to utilize 
        :param document_reader: class that provides text retrieval from document 
        """

        self.deployment = deployment
    
    def __load_env(self) -> None:
        load_dotenv()
        self.OPENAI_API_TYPE=os.getenv('OPEN_API_TYPE')
        self.OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
        self.OPENAI_API_BASE=os.getenv('OPENAI_API_BASE')
        self.OPENAI_API_VERSION=os.getenv('OPENAI_API_VERSION')

    def embed_document(self) -> langchain.embeddings.openai.OpenAIEmbeddings:
        #Method for embedding document to query against
    
        self.__load_env()

        self.embeddings: OpenAIEmbeddings = OpenAIEmbeddings(
            openai_api_base= self.OPENAI_API_BASE,
            openai_api_type='openai', #TODO: fix this to get from .env
            deployment=self.deployment,
            openai_api_key=self.OPENAI_API_KEY,
            chunk_size=1,
        )
        print(f"API Base URL: {self.OPENAI_API_BASE}")
        print(f"API Key: {self.OPENAI_API_KEY}")
        print(f"API Version: {self.OPENAI_API_VERSION}")
        print(f"API Type: {self.OPENAI_API_TYPE}")
        print(f"Deployment: {self.deployment}")
        return self.embeddings