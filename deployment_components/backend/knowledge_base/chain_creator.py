from langchain.chains.question_answering import load_qa_chain
from langchain.llms import AzureOpenAI,OpenAI
import langchain.vectorstores.faiss
from typing import Type
from knowledge_base.docsearch_creator import DocsearchCreator
import pydantic
import os 
from dotenv import load_dotenv

class ChainCreator:

    def __init__(self,deployment:str,docsearch:langchain.vectorstores.faiss.FAISS)->None:
        self.__load_env()

        self.chain = load_qa_chain(OpenAI(temperature=0,
                                          api_type='openai',
                                          openai_api_key=self.OPENAI_API_KEY,
                                          openai_api_base=self.OPENAI_API_BASE,
                                          model=deployment,
                                          max_tokens=1500),
                                   chain_type="stuff")
        print(self.chain)
        self.docsearch=docsearch

    def __load_env(self) -> None:
        load_dotenv(".env")
        self.OPENAI_API_TYPE=os.getenv('OPEN_API_TYPE')
        self.OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
        self.OPENAI_API_BASE=os.getenv('OPENAI_API_BASE')
        self.OPENAI_API_VERSION=os.getenv('OPENAI_API_VERSION')
        
    def query(self,query:str) -> str:
        
       docs = self.docsearch.similarity_search(query=query)

       result = self.chain.run(input_documents=docs,question=query)

       return result

       