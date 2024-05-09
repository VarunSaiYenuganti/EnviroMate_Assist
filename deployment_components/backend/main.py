import os
from pathlib import Path
from typing import Type
from contextlib import asynccontextmanager
import requests
from fastapi import FastAPI, UploadFile,HTTPException

from knowledge_base.chain_creator import ChainCreator
from knowledge_base.document_reader_interface import DocumentReaderInterface
from knowledge_base.local_text_reader import LocalTextReader
from knowledge_base.openai_text_emedder import OpenAITextEmbedder
from knowledge_base.docsearch_creator import DocsearchCreator
from langchain.llms import OpenAI,AzureOpenAI
from segment_image import segment_images
from PIL import Image

import json

from pydantic import BaseModel
# Uncomment this for server

class FileName(BaseModel):
    filename: str

class QuestionPrompt(BaseModel):
    question: str



server_resources = {}
server_resources_images = {}
@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
     #startup
     server_resources['qna_obj'], server_resources['qna_filename'],server_resources['qna_filepath'] = qna_create('C:/Users/Varun Sai/EnviroMate_Assist/data/waste_info')
     #delete any .jpg in ../../data/input_images
     for image in Path('C:/Users/Varun Sai/EnviroMate_Assist/data/input_images').iterdir():
        if image.suffix == ".jpg":
            os.remove(image)
        else: 
            pass
     server_resources_images['segmented_images'] = [] 
     print(f"Server resources: \n ")
     for i in range(0,len(server_resources['qna_filename'])):
         print(server_resources["qna_filename"][i])
     yield
     #shutdown
     # delete any .png in ../../data/segmented_images
     for image in Path('C:/Users/Varun Sai/EnviroMate_Assist/data/segmented_images').iterdir():
        if image.suffix == ".png":
            os.remove(image)
        else: 
            pass
         
     server_resources.clear()

app = FastAPI(lifespan=lifespan)

@app.post('/ask_document/{doc_id}')
async def ask_doc(doc_id,payload: QuestionPrompt):
    return {"Answer": f"{server_resources['qna_obj'][int(doc_id)].ask(payload.question)}"}
     
# # app.post that takes in an image from streamlit and saves it to the data/input_images folder
# @app.post('/upload_image')
# async def upload_image(file: UploadFile = File(...)):
#     # Save the image to the input_images folder
#     with open(f"C:/Users/User/Vasudha/EcoSage/data/input_images/{file.filename}", "wb") as buffer:
#         buffer.write(file.file.read())
#     # Return the filename
#     return {"filename": file.filename}

@app.post('/segment_image')
async def segment_image():
    # Call the segment_images function
    list_of_images = segment_images()
    # Return the list of segmented images
    return {"list_of_images": list_of_images}

@app.get('/run_process')
async def run_process():
    #run the pipeline
    result_list = run_pipeline()

    return {"result_list": result_list}

class QnAdoc:

    def __init__(self,file_path:str)->None:
        self.file_path = file_path
        self.text_reader = LocalTextReader(rooth_path=file_path)
        self.raw_text = self.text_reader.load_document()

        self.text_embedder = OpenAITextEmbedder(deployment='text-embedding-ada-002')
        self.doc_embeddings = self.text_embedder.embed_document()
        self.docsearch = DocsearchCreator().create_docsearch(self.raw_text,embeddings=self.doc_embeddings)
        self.chain = ChainCreator(deployment="gpt-3.5-turbo-instruct",docsearch=self.docsearch)
    
    def ask(self,question:str):

        return self.chain.query(query=question)



def qna_create(txt_dir:str):

    #All txts:
    txt_dir = Path(txt_dir)
    qna_obj = []
    qna_filename = []
    qna_filepath = []
    for i,txt in enumerate(txt_dir.iterdir()):
 
        qna_obj.append(QnAdoc(file_path=str(txt)))
        qna_filepath.append(txt)
        qna_filename.append(str(txt).split('/')[-1])
        

    return qna_obj,qna_filename,qna_filepath

def run_pipeline(): 
    # First get the path of the image in folder ./data/input_images/ 
    print("Inside run pipeline")
    result_list = []
    image_dir = "C:/Users/Varun Sai/EnviroMate_Assist/data/input_images"
    segment_images_dir = "C:/Users/Varun Sai/EnviroMate_Assist/data/segmented_images"
    image_path = ''
    for image in Path(image_dir).iterdir():
        #check if image is jpg png or jpeg
        if image.suffix == ".jpg" or image.suffix == ".png" or image.suffix == ".jpeg":
            image_path = str(image)
        else: 
            pass
    if image_path == '':
        raise HTTPException(status_code=400, detail="No image found in the input_images folder")

    
    # Call the segment_images function 
    list_of_images= segment_images(image_path=image_path,segment_images_dir=segment_images_dir)
    # For each image, call the ask_doc function
    for image_path in Path(segment_images_dir).iterdir():
        # Get image label from get_label()
        if image_path.suffix == ".png":
            # Load image as PIL image
            image_label = get_label(image_path=image_path)
            # Call the ask_doc function
            question = f"""
            You are a sustainability advisor. You are looking at a picture. The caption of the image is: {image_label}. Where/how should the objects in the caption be disposed, or recycled? Provide a concise and clear instructions, to the best of your ability.
            """
            answer = server_resources['qna_obj'][0].ask(question)
            result_list.append({"image": str(image_path),"label":image_label, "answer": answer})
    return result_list

def get_label(image_path:str)->str:
    
    # Get the image label from the image
    print("Inside get label")
    image_label = ''

    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    #API_URL = "https://huggingface.co/Salesforce/blip-image-captioning-large"
    headers = {"Authorization": "Bearer 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"}
    with open(image_path, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=headers, data=data)
    if response.status_code == 200:
        try:
            generated_text = response.json()[0]['generated_text']
            return generated_text
        except (KeyError, IndexError) as e:
            print(f"Error processing response JSON: {e}")
            return "Error: Invalid response format"
    else:
        print(f"Error: Request failed with status code {response.status_code}")
        return "Error: Request failed"
    

