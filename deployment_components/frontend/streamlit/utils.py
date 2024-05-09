import structlog
import requests
import json
logger = structlog.getLogger(__name__)


def image_extractions(image):
    return ['image1', 'image2', 'image3']


def image_to_text(image):
    return ['image_text1', 'image_text2', 'image_text3']


def llm(image_text):
    return ['text1', 'text2', 'text3']


def run_process(image):
    image_process = []

    image_crops = image_extractions(image)  # image PIL
    logger.info('Image crops step is completed.')
    
    image_text = image_to_text(image_crops)  # str
    logger.info('Image-to-text step is completed.')
    
    text = llm(image_text)
    logger.info('LLM step is completed.')

    for image, text in zip(image_crops, text):
        data_dict = {'image': image, 'text': text}
        image_process.append(data_dict)

    logger.info('Image crops and text are stored in a dictionary.')
    return image_process

def call_backend()->list: 

    url = 'http://127.0.0.1:8000/run_process'

    # get request 

    headers = {
    'Accept': 'application/json',
    }

    r = requests.get(url = url, headers=headers)
    print(r)
    # make json 
    data = r.json()['result_list'] 

    return data