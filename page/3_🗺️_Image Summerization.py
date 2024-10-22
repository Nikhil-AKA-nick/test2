import requests
from PIL import Image
import getpass
import os
from dotenv import load_dotenv
import streamlit as st
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import logging
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import traceback  # Import traceback to get detailed error info

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Check for Google API key
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Provide your Google API Key")

# Streamlit page configuration
st.set_page_config(
    page_title="Image Summarization",
    page_icon="🗺️",
)

# Load authentication config
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Authentication setup
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login()

if st.session_state["authentication_status"]:
        
    st.title("Image Summarization")

    # Input for the user's question related to the image
    image_question = st.text_input("Type your question here:")

    # Upload an image
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', width=300)

        # Save the uploaded image to disk to obtain a URL
        image_path = f"./static/{uploaded_file.name}"
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        image.save(image_path)

        # Placeholder for the image URL (replace with your server's URL)
        image_url = "https://your-server-url.com/static/" + uploaded_file.name
        
        logging.info(f"Image uploaded: {image_url}")
    else:
        # Use a placeholder image URL if none is uploaded
        image_url = "https://picsum.photos/300/300"
        logging.info("No image uploaded. Using a placeholder image.")

    # Ensure that a question is provided
    if image_question:
        try:
            # Log the image URL and question for debugging
            logging.info(f"Question: {image_question}, Image URL: {image_url}")
            
            # Use the Google Gemini model
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

            # Create the message content, including the question and the image URL
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": image_question,
                    },  
                    {
                        "type": "image_url", 
                        "image_url": image_url  # Pass the image URL here
                    }
                ]
            )

            # Get the response from the model
            response = llm.invoke([message]).content
            st.text_area("Chatbot Response:", response, height=200)
        except Exception as e:
            # Log the traceback for the error
            logging.error("An error occurred:")
            logging.error(traceback.format_exc())
            st.error("There was an error processing your request. Please check the logs for details.")
    else:
        st.text_area("Chatbot Response:", "Please type your question above", height=50)

    authenticator.logout()

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
