"""A streamlit dashboard of TrashMate."""
import streamlit as st
from PIL import Image
from utils import run_process, call_backend
import json
# # Configs
# configs = load_yaml_config(config_path=Path(__file__).parent / 'config.yaml')

# Page configs
st.set_page_config(
    page_icon='C:/Users/Varun Sai/EnviroMate_Assist/data/Logo.png',
    page_title='EnviroMate Assist v1.0',
    layout='centered',
    initial_sidebar_state='expanded',
    menu_items={
        'About': '# EnviroMate Assist \n Team **Happy**: Hanna, Fatemeh, Ameen, Sijia, Timur, Alexander',
    }
)

# Add a logo beside the title
logo_col, title_col = st.columns([3, 20])
logo_image = Image.open('C:/Users/Varun Sai/EnviroMate_Assist/data/Logo.png')
logo_width = 50  # Set the desired width for the logo
logo_col.image(logo_image, width=logo_width, use_column_width=False)

# Display the custom title
title_col.write("# EnviroMate Assist")

# Add text
st.text('This is a mock-up demo for the EnviroMate Assist Project.')

st.subheader('Instruction')
st.write('1. Upload your image by pressing the `Browse files` button or drag and drop the file to the area.\n',
         '2. Press the `Process image` button, and the results will show at the bottom.')

# App
st.subheader('App')
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image_width = 300
    image = st.image(uploaded_file, caption="Uploaded Picture", width=image_width)
    # Save image to data/input_images folder
    with open(f"../../../data/input_images/{uploaded_file.name}", "wb") as buffer:
        buffer.write(uploaded_file.read())

    if st.button("Process Image"):
        result = call_backend()

        colHead1, colHead2 = st.columns(2)

        with colHead1:
            st.write("Item")
        with colHead2:
            st.write("Instruction")
            
        for item in result:
            col1, col2 = st.columns(2)
            path_to_image = item['image']
            label = item['label']
            instruction = item['answer']

            try:
                with col1:
                    # st.image(pil_image, use_column_width=True)
                    image = Image.open(path_to_image)
                    st.image(image, caption=label, width=100)
                with col2:
                    st.write(instruction)
            except:
                with col1:
                    st.write("Error")
                with col2: 
                    st.write("Error")