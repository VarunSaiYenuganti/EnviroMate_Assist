import requests
from pathlib import Path
import os 
from dotenv import load_dotenv

def query(filename: Path) -> str:
    load_dotenv()
    API_URL = os.getenv('IMAGE_TO_TEXT_API_URL')
    key = os.getenv('IMAGE_TO_TEXT_KEY')
    headers = {'Authorization': f'Bearer {key}'}
    with open(filename, "rb") as f:
        data = f.read()

    response = requests.post(API_URL, headers=headers, data=data)
    return response.json()[0]['generated_text']

