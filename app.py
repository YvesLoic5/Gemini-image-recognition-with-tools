from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# read the document
document = Path('document.txt').read_text()
# configuring api key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# function to load gemini pro 

def get_gemini_response(input,image):
    # loading the gemini model
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,image[0]])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # read file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

# initialize our streamlit app

st.set_page_config(page_title="Gemini Image Demo")

st.header("Gemini application")
uploaded_file= st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image= ""

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True )

submit = st.button("Help ME")

input_prompt = f"""
Vous êtes un expert en conseille sinistre dans une assurance.
Veuillez répondre à l'utilisateur de façon court et précis en se basant à cet document:
{document}
"""

#if submit button is clicked

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data)

    st.subheader("Réponse : ")
    st.write(response)