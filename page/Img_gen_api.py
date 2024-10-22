import streamlit as st
from monsterapi import client
from PIL import Image
import requests
from io import BytesIO

# Initialize the Monster API client with your API key
api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjQxMmZjNDJhODRmM2RjYTU5OTMyM2IxZmRhYjcwM2JjIiwiY3JlYXRlZF9hdCI6IjIwMjQtMTAtMjFUMTI6MzQ6MjguMjI1NjcwIn0.uVJY7oFT_vIRZmm_ajaeP32mBw29pC5fM8D1alwC-Do'  # Replace 'your-api-key' with your actual Monster API key
monster_client = client(api_key)

# Streamlit app title
st.title("Image Generator with MonsterAPI")

# Input prompt from the user
prompt = st.text_input("Enter a prompt for the image generation:")

# Generate image on button click
if st.button("Generate Image"):
    if prompt:
        # Define the input data with user-provided prompt
        input_data = {
            'prompt': prompt,
            # You can add additional parameters here if needed
        }
        # Call the Monster API to generate the image
        result = monster_client.generate('txt2img', input_data)
        
        # Get the image URL from the result
        if 'output' in result and result['output']:
            image_url = result['output'][0]
            st.write("Generated Image:")
            
            # Display the image in the Streamlit app
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            st.image(img, caption="Generated Image", use_column_width=True)
        else:
            st.error("Failed to generate image.")
    else:
        st.warning("Please enter a prompt.")
