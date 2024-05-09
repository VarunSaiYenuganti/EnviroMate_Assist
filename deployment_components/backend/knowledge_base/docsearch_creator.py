"""Docsearch creator class"""
import langchain.vectorstores.faiss
from langchain.vectorstores import FAISS 
from langchain.text_splitter import CharacterTextSplitter
from typing import Callable
class DocsearchCreator:
    def __init__(self):
        pass 

    def __split_text(self,text:str) -> list:
        text_splitter = CharacterTextSplitter(
                                separator="\n",
                                chunk_size=1000,
                                chunk_overlap=200,
                                length_function=len,
                            )
        return text_splitter.split_text(text)
    
    def create_docsearch(self, texts:str,embeddings:langchain.vectorstores.faiss.FAISS) -> langchain.vectorstores.faiss.FAISS:
        
        docsearch = FAISS.from_texts(self.__split_text(text=texts),embedding=embeddings)
        
        return docsearch