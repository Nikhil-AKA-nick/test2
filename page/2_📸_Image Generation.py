import streamlit as st
import requests

# Set your Replicate API token
REPLICATE_API_TOKEN = "r8_A5xJBVGwT5R0qysSCLNihdPoLNoNju826uhLz"

# Function to generate image from text
def generate_image(prompt):
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }
    json_data = {
        "version": "c0d4f3fbb8b7ef9c484bdc6df40d5f7c4e1e77f1e0a9079b9e67d66544d98ff7",
        "input": {
            "prompt": prompt,
            "num_images": 1,  # Generate one image
        },
    }
    response = requests.post(
        "https://api.replicate.com/v1/predictions",
        headers=headers,
        json=json_data,
    )
    if response.status_code == 201:
        return response.json()["output"][0]  # Return the URL of the generated image
    else:
        st.error("Error generating image.")
        return None

# Streamlit app layout
st.title("Image Generator from Text")
st.write("Enter a prompt to generate an image:")

# Text input for the prompt
prompt = st.text_input("Prompt", "")

# Button to generate the image
if st.button("Generate Image"):
    if prompt:
        with st.spinner("Generating image..."):
            image_url = generate_image(prompt)
            if image_url:
                st.image(image_url, caption=prompt)
    else:
        st.warning("Please enter a prompt.")
