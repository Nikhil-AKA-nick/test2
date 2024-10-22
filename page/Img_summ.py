import requests
from PIL import Image
import os
from dotenv import load_dotenv
import streamlit as st
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import yaml
from yaml.loader import SafeLoader
import base64

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit page config
st.set_page_config(
    page_title="Image Summarization",
    page_icon="🗺️",
)

# Ensure Google API key is set
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = st.text_input("Provide your Google API Key", type="password")

# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Title of the app
st.title("Image Summarization")

# User inputs question for the image
image_question = st.text_input("Type your question here:")

# Upload local image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

# Convert image to base64
def image_to_base64(image_file):
    buffered = BytesIO()
    image_file.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"

# Handle the uploaded image or default sample image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    # Convert the uploaded image to a base64 string
    image_base64 = image_to_base64(image)
else:
    # Fallback to a sample image
    image = Image.open("./static/sample_image.jpeg")
    st.image(image, caption='Sample Image', use_column_width=True)
    image_base64 = image_to_base64(image)

# Initialize Google Generative AI model with the new 'gemini-1.5-flash' model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Check if the user has entered a question
if image_question and uploaded_file is not None:
    # Construct the message for the LLM
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": image_question,
            },
            {"type": "image_url", "image_url": image_base64},  # Pass the base64 encoded image
        ]
    )

    # Invoke the LLM with the message
    try:
        response = llm.invoke([message]).content
        st.text_area("Chatbot Response:", response, height=200)
    except Exception as e:
        st.error(f"Error generating response: {e}")
else:
    st.text_area("Chatbot Response:", "Please upload an image and type your question.", height=100)
