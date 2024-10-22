# # Install necessary libraries

# import streamlit as st
# import PyPDF2
# from sentence_transformers import SentenceTransformer
# import faiss
# import numpy as np

# # Google API key (replace with your actual key)
# GOOGLE_API_KEY = "AIzaSyC_hpuvkEgTzHj1TR_QpCXA7dcFRGfin8A"  # Your Google API key

# # Function to extract text from PDF using PdfReader
# def extract_text_from_pdf(pdf_file):
#     pdf_reader = PyPDF2.PdfReader(pdf_file)
#     text = ""
#     for page_num in range(len(pdf_reader.pages)):
#         page = pdf_reader.pages[page_num]
#         text += page.extract_text()
#     return text

# # Function to create embeddings using a model and store them in FAISS index
# def create_faiss_index(text_chunks, model):
#     embeddings = model.encode(text_chunks)
#     dimension = embeddings.shape[1]
#     index = faiss.IndexFlatL2(dimension)
#     index.add(np.array(embeddings, dtype=np.float32))
#     return index, embeddings

# # Function to handle queries and return the best matching chunk
# def search_faiss_index(query, index, model, text_chunks):
#     query_vector = model.encode([query])
#     D, I = index.search(np.array(query_vector, dtype=np.float32), k=1)
#     return text_chunks[I[0][0]] if len(I) > 0 else "No relevant information found."

# # Streamlit app
# def main():
#     st.title("Chat with your PDF")
    
#     # Initialize session state for storing PDF embeddings and chat history
#     if 'index' not in st.session_state:
#         st.session_state.index = None
#         st.session_state.text_chunks = None
#         st.session_state.chat_history = []
    
#     # PDF upload
#     uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    
#     if uploaded_file is not None:
#         # Extract text from uploaded PDF
#         pdf_text = extract_text_from_pdf(uploaded_file)
#         text_chunks = [pdf_text[i:i+512] for i in range(0, len(pdf_text), 512)]
        
#         # Load embedding model
#         model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
#         # Create FAISS index
#         index, embeddings = create_faiss_index(text_chunks, model)
        
#         # Store index and text chunks in session state
#         st.session_state.index = index
#         st.session_state.text_chunks = text_chunks
        
#         st.success("PDF successfully processed and indexed.")
    
#     if st.session_state.index is not None:
#         # Input field for user question
#         user_question = st.text_input("Ask a question about the PDF:")
        
#         # Submit button to trigger query
#         if st.button("Submit"):
#             if user_question:
#                 # Search FAISS index for context
#                 relevant_context = search_faiss_index(user_question, st.session_state.index, model, st.session_state.text_chunks)
                
#                 # Add to chat history
#                 st.session_state.chat_history.append((user_question, relevant_context))
        
#         # Display the chat history
#         if st.session_state.chat_history:
#             st.write("### Chat History")
#             for question, pdf_response in st.session_state.chat_history:
#                 st.write(f"**You:** {question}")
#                 st.write(f"**From PDF:** {pdf_response}")
#                 st.write("---")

# if __name__ == "__main__":
#     main()


# Install necessary libraries

import streamlit as st
import PyPDF2
from sentence_transformers import SentenceTransformer 
import faiss
import numpy as np
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Load your Google API key from .env



# Function to extract text from PDF using PdfReader
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text



# Function to create embeddings using a model and store them in FAISS index
def create_faiss_index(text_chunks, model):
    embeddings = model.encode(text_chunks)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings, dtype=np.float32))
    return index, embeddings



# Function to handle queries and return the best matching chunk
def search_faiss_index(query, index, model, text_chunks):
    query_vector = model.encode([query])
    D, I = index.search(np.array(query_vector, dtype=np.float32), k=1)
    return text_chunks[I[0][0]] if len(I) > 0 else "No relevant information found."



# Streamlit app
def main():
    st.title("Chat with your PDF")
    
    # Initialize session state for storing PDF embeddings and chat history
    if 'index' not in st.session_state:
        st.session_state.index = None
        st.session_state.text_chunks = None
        st.session_state.chat_history = []
    
    # PDF upload
    uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from uploaded PDF
        pdf_text = extract_text_from_pdf(uploaded_file)
        text_chunks = [pdf_text[i:i+512] for i in range(0, len(pdf_text), 512)]
        
        # Load embedding model
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        
        # Create FAISS index
        index, embeddings = create_faiss_index(text_chunks, model)
        
        # Store index and text chunks in session state
        st.session_state.index = index
        st.session_state.text_chunks = text_chunks
        
        st.success("PDF successfully processed and indexed.")
    
    if st.session_state.index is not None:
        # Input field for user question
        user_question = st.text_input("Ask a question about the PDF:")
        
        # Submit button to trigger query
        if st.button("Submit"):
            if user_question:
                # Search FAISS index for context
                relevant_context = search_faiss_index(user_question, st.session_state.index, model, st.session_state.text_chunks)
                
                # Add to chat history
                st.session_state.chat_history.append((user_question, relevant_context))
        
        # Display the chat history
        if st.session_state.chat_history:
            st.write("### Chat History")
            for question, pdf_response in st.session_state.chat_history:
                st.write(f"**You:** {question}")
                st.write(f"**From PDF:** {pdf_response}")
                st.write("---")

if __name__ == "__main__":
    main()
