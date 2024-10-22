import openai
import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key here (either from .env file or user input)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your OpenAI API Key", type="password")

# Configure OpenAI with your API key
openai.api_key = api_key

# Set up Streamlit page config
st.set_page_config(page_title="Text to Image Generator", page_icon="🎨")

# Title of the app
st.title("DALL·E Image Generation")

# Input prompt from user
prompt = st.text_input("Enter a prompt to generate an image:")

# Generate the image from text prompt
if st.button("Generate Image"):
    if prompt:
        with st.spinner("Generating image..."):
            try:
                # Call OpenAI API for image generation (DALL·E)
                response = openai.Image.create(
                    prompt=prompt,
                    n=1,  # Number of images to generate
                    size="1024x1024"  # Image size
                )

                # Extract image URL from response
                image_url = response['data'][0]['url']

                # Display the generated image
                st.image(image_url, caption="Generated Image", use_column_width=True)

                # Option to download the image
                st.markdown(f"[Download the image]({image_url})")

            except Exception as e:
                st.error(f"Error generating image: {e}")
    else:
        st.warning("Please enter a prompt to generate an image.")
